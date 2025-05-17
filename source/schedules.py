import nfl_data_py as nfl
import pandas as pd

import logging
import traceback

logger = logging.getLogger(__name__)

class Schedules:
    def __init__(self, seasons: list[int]):
        self.seasons = seasons
        self.master_schedule = self._load()
        self.weeks = self.master_schedule['week'].nunique()

    def _load(self) -> pd.DataFrame:
        df = nfl.import_schedules(self.seasons)
        return df[df['game_type'] == 'REG'][['week', 'away_team', 'home_team']]

    def _split_schedules_by_team(self) -> dict[str, pd.DataFrame]:
        home_games = self.master_schedule.rename(columns={'away_team': 'Opponent', 'home_team': 'Team'})
        away_games = self.master_schedule.rename(columns={'home_team': 'Opponent', 'away_team': 'Team'})
        combined = pd.concat([home_games, away_games], ignore_index=True)
        grouped = combined.groupby('Team')
        return {team: group.drop(columns='Team').set_index('week').sort_index().rename_axis(team) for team, group in grouped}

    def _fill_bye_weeks(self, df: pd.DataFrame, team: str) -> pd.DataFrame:
        all_weeks = pd.Index(range(1, self.weeks + 1), name=team)
        return df.reindex(all_weeks, fill_value="BYE").sort_index()

    def get_team_schedules(self) -> dict[str, pd.DataFrame]:
        team_games = self._split_schedules_by_team()
        return {team: self._fill_bye_weeks(df, team) for team, df in team_games.items()}