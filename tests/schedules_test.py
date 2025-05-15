import pytest
from pytest_mock import MockerFixture

import pandas as pd

from source.schedules import Schedules

@pytest.fixture
def sample_schedule():
    return pd.DataFrame({'week': [1, 1, 2],
                         'game_type': ['REG', 'REG', 'REG'],
                         'away_team': ['BUF', 'KC', 'MIA'],
                         'home_team': ['NYJ', 'CIN', 'NE']})

def test_get_master_schedule_filters_regular_season(mocker: MockerFixture, sample_schedule: pd.DataFrame):
    mocker.patch("source.schedules.nfl.import_schedules", return_value=sample_schedule)
    schedules = Schedules([2021])
    df = schedules.master_schedule
    assert all(df.columns == ['week', 'away_team', 'home_team'])
    assert len(df) == 3

def test_get_weeks_counts_unique_weeks(mocker: MockerFixture, sample_schedule: pd.DataFrame):
    mocker.patch("source.schedules.nfl.import_schedules", return_value=sample_schedule)
    schedules = Schedules([2021])
    assert schedules.weeks == 2

def test_partition_schedules_structure(mocker: MockerFixture, sample_schedule: pd.DataFrame):
    mocker.patch("source.schedules.nfl.import_schedules", return_value=sample_schedule)
    schedules = Schedules([2021])
    result = schedules._partition_schedules()
    assert isinstance(result, dict)
    assert 'BUF' in result or 'NYJ' in result
    team_df = next(iter(result.values()))
    assert isinstance(team_df, pd.DataFrame)
    assert 'Opponent' in team_df.columns

def test_get_bye_weeks_fills_missing_weeks(mocker: MockerFixture, sample_schedule: pd.DataFrame):
    mocker.patch("source.schedules.nfl.import_schedules", return_value=sample_schedule)
    schedules = Schedules([2021])
    team_df = pd.DataFrame({ 'Opponent': ['BUF'] }, index=pd.Index([1], name='NYJ'))
    filled_df = schedules._get_bye_weeks(team_df)
    assert len(filled_df) == schedules.weeks
    assert 'BYE' in filled_df['Opponent'].values

def test_get_schedules_pipeline(mocker: MockerFixture, sample_schedule: pd.DataFrame):
    mocker.patch("source.schedules.nfl.import_schedules", return_value=sample_schedule)
    schedules = Schedules([2021])
    result = schedules.get_schedules()
    assert isinstance(result, dict)
    for team, df in result.items():
        assert isinstance(df, pd.DataFrame)
        assert df.shape[0] == schedules.weeks