import pandas as pd
import pytest

from src.extract.extractor import F1DataExtractor
from datetime import date


@pytest.fixture
def extractor(tmp_path):
    temp_cache_dir = tmp_path / 'cache'
    temp_cache_dir.mkdir()
    return F1DataExtractor(cache_dir=str(temp_cache_dir))


def test_get_events_schedule_type_error_year_from(extractor):
    with pytest.raises(TypeError, match='Variables should be integers!'):
        extractor.get_events_schedule(year_from='1234')


def test_get_events_schedule_type_error_year_to(extractor):
    with pytest.raises(TypeError, match='Variables should be integers!'):
        extractor.get_events_schedule(year_from=2020, year_to='2020')


def test_get_events_schedule_value_error_year_from_less_than_2018(extractor):
    with pytest.raises(ValueError, match='Year_from value is not correct!'):
        extractor.get_events_schedule(year_from=2017)


def test_get_events_schedule_value_error_year_from_bigger_than_year_to(extractor):
    with pytest.raises(ValueError, match='Year_from value is not correct!'):
        current_year = date.today().year
        extractor.get_events_schedule(year_from=current_year + 1)


def test_get_events_schedule_value_error_year_to(extractor):
    with pytest.raises(ValueError, match='Year_to is greater than current year!'):
        current_year = date.today().year
        extractor.get_events_schedule(year_from=2019, year_to=current_year + 1)


def test_get_events_schedule(extractor, mocker):
    mock_get = mocker.patch('src.extract.extractor.fastf1.get_event_schedule')

    mock_get.return_value = pd.DataFrame({'RoundNumber': [12, 30, 31],
                                          'Country': ['Bahrain', 'Italy', 'Portugal']})

    result = extractor.get_events_schedule(year_from=2021, year_to=2021)

    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert 'RoundNumber' in result.columns
    assert 'Country' in result.columns
    assert 'Season' in result.columns
    assert (result['Season'] == 2021).all()
    assert len(result) == 3


def test_get_session_results_type_error_year(extractor):
    with pytest.raises(TypeError,
                       match='Variables year, round_number should be integers and session_type should be str.'):
        extractor.get_session_results('2020', 1, 'Race')


def test_get_session_results_type_error_round_number(extractor):
    with pytest.raises(TypeError,
                       match='Variables year, round_number should be integers and session_type should be str.'):
        extractor.get_session_results(2020, '1', 'Race')


def test_get_session_results_type_error_session_type(extractor):
    with pytest.raises(TypeError,
                       match='Variables year, round_number should be integers and session_type should be str.'):
        extractor.get_session_results(2020, 1, 5)


def test_get_session_results_value_error_session_type(extractor):
    with pytest.raises(ValueError,
                       match='Incorrect session_type, session_type should be FP1, FP2, FP3, Qualifying or Race.'):
        extractor.get_session_results(2023, 2, 'Qualification')


def test_get_session_results_value_error_year_to_small(extractor):
    with pytest.raises(ValueError,
                       match=f'Value year should be at least 2018 and smaller or equal current year: {date.today().year}'):
        extractor.get_session_results(2011, 2, 'Race')


def test_get_session_results_value_error_year_bigger(extractor):
    with pytest.raises(ValueError,
                       match=f'Value year should be at least 2018 and smaller or equal current year: {date.today().year}'):
        year = date.today().year
        extractor.get_session_results(year + 2, 2, 'Race')


def test_get_session_results(extractor, mocker):
    mock_session = mocker.MagicMock()
    mock_session.results = {'DriverNumber': [81, 1], 'Abbreviation': ['PIA', 'VER']}

    mock_get = mocker.patch('src.extract.extractor.fastf1.get_session', return_value=mock_session)
    result = extractor.get_session_results(2023, 1, 'Race')

    assert isinstance(result, pd.DataFrame)
    assert 'Year' in result.columns
    assert 'RoundNumber' in result.columns
    assert 'SessionType' in result.columns
    assert 'DriverNumber' in result.columns
    assert (result['RoundNumber'] == 1).all()
    assert (result['Year'] == 2023).all()
    assert len(result) == 2

    mock_session.load.assert_called_once_with(
        laps=False, telemetry=False, weather=False, messages=False
    )
