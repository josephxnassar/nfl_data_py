import nfl_data_py as nfl
import pandas as pd

from collections import defaultdict

import logging
import traceback

logger = logging.getLogger(__name__)

class NDPDepthChart:
    def __init__(self, seasons: list, week: int):
        self.seasons = seasons
        self.week = week
        self.master_depth_chart = self._load()

    def _load(self) -> pd.DataFrame:
        dc = nfl.import_depth_charts(self.seasons)
        return dc[(dc['week'] == self.week) & (dc['formation'] == 'Offense')].assign(full_name=lambda x: x['football_name'].str.cat(x['last_name'], sep=' ')).sort_values(by=['club_code', 'depth_team', 'position'])[['club_code', 'depth_team', 'position', 'full_name']]

    def get_depth_charts(self) -> dict[str, pd.DataFrame]:
        depth_charts = {}
        for team, group in self._load().groupby('club_code'):
            position_players = defaultdict(list)
            for _, row in group.iterrows():
                position_players[row['position']].append(row['full_name'])
            rows = []
            for pos in ['QB', 'RB', 'WR', 'TE']:
                rows.append({'Position': pos,
                            'Starter':  position_players[pos][0] if len(position_players[pos]) > 0 else None,
                            '2nd':      position_players[pos][1] if len(position_players[pos]) > 1 else None,
                            '3rd':      position_players[pos][2] if len(position_players[pos]) > 2 else None})
            depth_charts[team] = pd.DataFrame(rows).set_index('Position').rename_axis(team)
        return depth_charts