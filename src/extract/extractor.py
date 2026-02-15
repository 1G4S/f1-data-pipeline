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
