import pandas as pd
import pytest
from src.extract.extractor import F1DataExtractor
from datetime import date


def test_get_events_schedule_type_error_year_from():
    f1_extractor = F1DataExtractor()
    with pytest.raises(TypeError, match='Variables should be integers!'):
        f1_extractor.get_events_schedule(year_from='1234')


def test_get_events_schedule_type_error_year_to():
    f1_extractor = F1DataExtractor()
    with pytest.raises(TypeError, match='Variables should be integers!'):
        f1_extractor.get_events_schedule(year_from=2020, year_to='2020')


def test_get_events_schedule_value_error_year_from_less_than_2018():
    f1_extractor = F1DataExtractor()
    with pytest.raises(ValueError, match='Year_from value is not correct!'):
        f1_extractor.get_events_schedule(year_from=2017)


def test_get_events_schedule_value_error_year_from_bigger_than_year_to():
    f1_extractor = F1DataExtractor()
    with pytest.raises(ValueError, match='Year_from value is not correct!'):
        current_year = date.today().year
        f1_extractor.get_events_schedule(year_from=current_year + 1)


def test_get_events_schedule_value_error_year_to():
    f1_extractor = F1DataExtractor()
    with pytest.raises(ValueError, match='Year_to is greater than current year!'):
        current_year = date.today().year
        f1_extractor.get_events_schedule(year_from=2019, year_to=current_year + 1)


def test_get_events_schedule():
    f1_extractor = F1DataExtractor()

    result = f1_extractor.get_events_schedule(year_from=2021, year_to=2021)

    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert 'Season' in result.columns
    assert (result['Season'] == 2021).all()
