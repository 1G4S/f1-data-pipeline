import pandas as pd
import pytest
from src.extract.extractor import F1DataExtractor
from datetime import date


@pytest.fixture
def extractor():
    return F1DataExtractor()


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
