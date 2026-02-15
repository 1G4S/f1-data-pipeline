import logging
import os
import pandas as pd
import fastf1
from datetime import date


class F1DataExtractor:
    def __init__(self, cache_dir: str = 'cache'):
        self.logger = logging.getLogger(__name__)

        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
            self.logger.info(f'Created cache directory at {cache_dir}')

        fastf1.Cache.enable_cache(cache_dir)
        self.logger.info('FastF1 cache enabled.')

    def get_events_schedule(self, year_from: int, year_to: int = None) -> pd.DataFrame:
        """
        Get schedule of events for chosen year.

        :param year_from: Minimal year that events will be fetched from.
        :param year_to: Maximal year that events will be fetched from.
        :return Schedule of events for chosen years scope.

        :raises
            TypeError: Variables should be integers.
            ValueError: Year from should be at least 2018 and shouldn't be bigger than year to.
            ValueError: Year to shouldn't be bigger than current year.
            Exception: If errors during fetching data occurs.
        """
        current_year = date.today().year
        if year_to is None:
            year_to = current_year

        if not all(isinstance(year, int) for year in [year_from, year_to]):
            raise TypeError('Variables should be integers!')

        if (year_from < 2018) or (year_from > year_to):
            raise ValueError('Year_from value is not correct!')

        if year_to > date.today().year:
            raise ValueError('Year_to is greater than current year!')

        events = []
        for year in range(year_from, year_to + 1):
            self.logger.info(f'Fetching events schedule for {year} year.')
            try:
                df = pd.DataFrame(fastf1.get_event_schedule(year))
                df['Season'] = year
                events.append(df)
            except Exception as e:
                self.logger.exception(f'Error during fetching data from {year}: {e}')

        if not events: return pd.DataFrame()
        result = pd.concat(events, ignore_index=True)
        self.logger.info('Fetching events schedule performed successfully!')
        return result

    def get_session_results(self, year: int, round_number: int, session_type: str = 'Race') -> pd.DataFrame:
        """
        Get results from wanted session.

        :param year: Year that session happened in.
        :param round_number: Round number of wanted session.
        :param session_type: Type of wanted session (Race, Qualifying etc.).
        :return: results of chosen session (Dataframe)
        :raises
            TypeError: year and round_number should be integers. Session_type should be string.
            ValueError: session_type should be FP1, FP2, FP3, Qualifying or Race.
            ValueError: Year should be at least 2018 and shouldn't be bigger than current year.
            Exception: If errors during fetching data occurs.
        """

        if not isinstance(year, int) or not isinstance(round_number, int) or not isinstance(session_type, str):
            raise TypeError('Variables year, round_number should be integers and session_type should be str.')

        session_types = ['Race', 'Qualifying', 'FP1', 'FP2', 'FP3', 'SQ', 'Sprint']
        if session_type not in session_types:
            raise ValueError('Incorrect session_type, session_type should be FP1, FP2, FP3, Qualifying or Race.')

        if year < 2018 or year > date.today().year:
            raise ValueError(
                f'Value year should be at least 2018 and smaller or equal current year: {date.today().year}')

        try:
            self.logger.info(
                f'Fetching results from session: year: {year}, round_number: {round_number}, session_type: {session_type}')
            session = fastf1.get_session(year=year, gp=round_number, identifier=session_type)
            session.load(laps=False, telemetry=False, weather=False, messages=False)
            results = pd.DataFrame(session.results)
            results['Year'] = year
            results['RoundNumber'] = round_number
            results['SessionType'] = session_type
            self.logger.info(f'Fetching data for chosen session performed successfully.')
            return results

        except Exception as e:
            self.logger.exception(
                f'Error during fetching results for session: year: {year}, round_number: {round_number}, session_type: {session_type}. Exception: {e}')
            raise
