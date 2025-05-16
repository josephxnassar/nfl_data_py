import nfl_data_py as nfl
import pandas as pd

from collections import defaultdict

import logging

logger = logging.getLogger(__name__)

class NDPDepthChart:
    def __init__(self, seasons: list, week: int):
        self.seasons = seasons
        self.week = week
        self.master_depth_chart = self._get_master_depth_chart()

    def _get_master_depth_chart(self) -> pd.DataFrame:
        dc = nfl.import_depth_charts(self.seasons)
        return dc[(dc['week'] == self.week) & (dc['formation'] == 'Offense')].assign(full_name=lambda x: x['football_name'].str.cat(x['last_name'], sep=' ')).sort_values(by=['club_code', 'depth_team', 'position'])[['club_code', 'depth_team', 'position', 'full_name']]

    def _partition_teams(self) -> dict:
        team_dataframes = defaultdict(list)
        for _, row in self.master_depth_chart.iterrows():
            team_dataframes[row['club_code']].append(row)
        return {team: pd.DataFrame(rows) for team, rows in team_dataframes.items()}

    def _create_depth_chart(self, team_df: pd.DataFrame) -> pd.DataFrame:
        rows = []
        for pos in ['QB', 'RB', 'WR', 'TE']:
            players = team_df[team_df['position'] == pos]['full_name'].tolist()
            rows.append({'Position': pos,
                         'Starter':  players[0] if len(players) > 0 else None,
                         '2nd':      players[1] if len(players) > 1 else None,
                         '3rd':      players[2] if len(players) > 2 else None})

        return pd.DataFrame(rows).set_index('Position')

    def get_depth_charts(self) -> dict:
        dfs = self._partition_teams()
        depth_charts = {}
        for team, df in dfs.items():
            depth_charts[team] = self._create_depth_chart(df).rename_axis(team)
        return depth_charts