import nfl_data_py as nfl
import pandas as pd

from collections import defaultdict

from .regression import Regression

import logging

logger = logging.getLogger(__name__)

class Statistics:
    def __init__(self, seasons: list):
        self.seasons = seasons
        self.key, self.player_to_pfr = self._create_key()
        self.seasonal_data = self._get_seasonal_data()
        self.snap_counts = self._get_snap_counts()

    def _create_key(self) -> dict:
        sr = nfl.import_seasonal_rosters(self.seasons, columns=['player_id', 'pfr_id', 'player_name', 'depth_chart_position'])

        key = defaultdict(lambda: None)
        player_to_pfr = defaultdict(lambda: None)
        for row in sr.itertuples(index=False):
            key[row.player_id] = (row.player_name, row.depth_chart_position)
            if row.pfr_id:
                player_to_pfr[row.player_id] = row.pfr_id
        return key, player_to_pfr
    
    def _get_seasonal_data(self) -> pd.DataFrame:
        sd = nfl.import_seasonal_data(self.seasons)
        return sd.drop(columns=['season', 'season_type']).groupby('player_id').mean().reset_index()

    def _get_snap_counts(self) -> pd.DataFrame:
        sc = nfl.import_snap_counts(self.seasons)
        return sc[['pfr_player_id', 'offense_snaps', 'offense_pct']].groupby('pfr_player_id').mean().reset_index()
 
    def _merge(self) -> pd.DataFrame:
        self.seasonal_data['pfr_id'] = self.seasonal_data['player_id'].map(self.player_to_pfr)
        return pd.merge(self.seasonal_data, self.snap_counts.rename(columns={'pfr_player_id': 'pfr_id'}), on='pfr_id', how='left').drop(columns=['pfr_id']).dropna()
        
    def _partition(self, df: pd.DataFrame) -> dict:
        cols = ['player_name'] + df.columns.tolist()[1:]
        position_dataframes = defaultdict(lambda: pd.DataFrame(columns=cols))
        for _, row in df.iterrows():
            player_stats = row.tolist()
            player = self.key[player_stats[0]]
            if player[1] in ['QB', 'RB', 'WR', 'TE']:
                ref_df = position_dataframes[player[1]]
                ref_df.loc[len(ref_df.index)] = [player[0]] + player_stats[1:]
        return {pos: df.set_index('player_name') for pos, df in position_dataframes.items()}
    
    def _filter_df(self, df: pd.DataFrame) -> pd.DataFrame:
        return df[[col for col in df.columns if (df[col] != 0).sum() > 0.1 * len(df)]]
    
    def _create_ratings(self, df: pd.DataFrame) -> pd.DataFrame:
        y = df["fantasy_points_ppr"]
        X = df.drop(columns=["fantasy_points", "fantasy_points_ppr"])
        return Regression(X, y).execute()
    
    def execute(self) -> dict:
        df = self._merge()
        dfs = self._partition(df)
        for pos in dfs.keys():
            dfs[pos] = self._filter_df(dfs[pos])
            dfs[pos] = self._create_ratings(dfs[pos])
        return dfs