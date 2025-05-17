import nfl_data_py as nfl
import pandas as pd

from collections import defaultdict

from .regression import Regression

import logging
import traceback

logger = logging.getLogger(__name__)

class Statistics:
    def __init__(self, seasons: list):
        self.seasons = seasons
        self.key = self._create_key()
        self.seasonal_data = self._load()

    def _create_key(self) -> dict:
        sr = nfl.import_seasonal_rosters(self.seasons, columns=['player_id', 'player_name', 'depth_chart_position'])
        return {row.player_id: (row.player_name, row.depth_chart_position) for row in sr.itertuples(index=False)}

    def _load(self) -> pd.DataFrame:
        sd = nfl.import_seasonal_data(self.seasons)
        return sd.drop(columns=['season', 'season_type']).groupby('player_id').mean().reset_index().dropna()

    def _partition(self) -> dict:
        cols = ['player_name'] + self.seasonal_data.columns.tolist()[1:]
        position_data = defaultdict(list)
        for _, row in self.seasonal_data.iterrows():
            player_name, position = self.key[row.player_id]
            if position in ['QB', 'RB', 'WR', 'TE'] and player_name is not None:
                position_data[position].append([player_name] + row.tolist()[1:])
        return {pos: pd.DataFrame(data, columns=cols).set_index('player_name') for pos, data in position_data.items()}

    def _filter_df(self, df: pd.DataFrame) -> pd.DataFrame:
        threshold = 0.1 * len(df)
        return df.loc[:, (df != 0).sum() > threshold]

    def _create_ratings(self, df: pd.DataFrame) -> pd.DataFrame:
        y = df["fantasy_points_ppr"]
        X = df.drop(columns=["fantasy_points", "fantasy_points_ppr"])
        return Regression(X, y).execute()

    def get_statistics(self) -> dict:
        return {pos: self._create_ratings(self._filter_df(df)) for pos, df in self._partition().items()}