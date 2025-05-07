import nfl_data_py as nfl
import pandas as pd

from collections import defaultdict

from urllib.error import HTTPError
import inspect
import sys

class Schedules:
    def __init__(self, seasons: list):
        self.seasons = seasons
        self.master_schedule = self._get_master_schedule()
        self.weeks = self._get_weeks()

    def _get_master_schedule(self) -> pd.DataFrame:
        try:
            s = nfl.import_schedules(self.seasons)
            return s[s['game_type'] == 'REG'][['week', 'away_team', 'home_team']]
        except HTTPError as e:
            function_name = inspect.currentframe().f_code.co_name
            print(f"Exception in {function_name}: {e}")
            sys.exit(1)

    def _get_weeks(self) -> int:
        return self.master_schedule['week'].nunique()

    def _partition_schedules(self) -> dict:
        team_dataframes = defaultdict(list)
        for _, row in self.master_schedule.iterrows():
            week, away, home = row['week'], row['away_team'], row['home_team']
            team_dataframes[home].append((week, away))
            team_dataframes[away].append((week, home))
        return {team: pd.DataFrame(games, columns=['week', 'Opponent']).set_index('week').rename_axis(team).sort_index() for team, games in team_dataframes.items()}

    def _get_bye_weeks(self, df: pd.DataFrame) -> pd.DataFrame:
        all_weeks = pd.Index(range(1, self.weeks + 1), name=df.index.name)
        return df.reindex(all_weeks, fill_value="BYE").sort_index()

    def get_schedules(self) -> dict:
        team_dfs = self._partition_schedules()
        schedules = {}
        for team, df in team_dfs.items():
            schedules[team] = self._get_bye_weeks(df)
        return schedules