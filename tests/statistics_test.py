import pytest
from pytest_mock import MockerFixture

import pandas as pd

from collections import defaultdict

from source.statistics import Statistics

@pytest.fixture
def mock_nfl_imports(mocker: MockerFixture):
    mocker.patch("source.statistics.nfl.import_seasonal_rosters")
    mocker.patch("source.statistics.nfl.import_seasonal_data")
    mocker.patch("source.statistics.nfl.import_snap_counts")
    return mocker

@pytest.fixture
def sample_roster():
    return pd.DataFrame({'player_id': ['id1', 'id2'],
                         'pfr_id': ['pfr1', 'pfr2'],
                         'player_name': ['Player One', 'Player Two'],
                         'depth_chart_position': ['QB', 'RB']})

@pytest.fixture
def sample_seasonal():
    return pd.DataFrame({'player_id': ['id1', 'id2'],
                         'season': [2021, 2021],
                         'season_type': ['REG', 'REG'],
                         'fantasy_points': [200, 150],
                         'fantasy_points_ppr': [220, 170],
                         'stat_x': [10, 20]})

@pytest.fixture
def sample_snaps():
    return pd.DataFrame({'pfr_player_id': ['pfr1', 'pfr2'],
                         'offense_snaps': [500, 400],
                         'offense_pct': [75.0, 65.0]})

def test_create_key(mock_nfl_imports: MockerFixture, sample_roster: pd.DataFrame):
    mock_nfl_imports.patch("source.statistics.nfl.import_seasonal_rosters", return_value=sample_roster)
    stats = Statistics([2021])
    assert stats.key['id1'] == ('Player One', 'QB')
    assert stats.player_to_pfr['id2'] == 'pfr2'

def test_get_seasonal_data(mock_nfl_imports: MockerFixture, sample_seasonal: pd.DataFrame):
    mock_nfl_imports.patch("source.statistics.nfl.import_seasonal_data", return_value=sample_seasonal)
    stats = Statistics.__new__(Statistics)
    stats.seasons = [2021]
    df = stats._get_seasonal_data()
    assert 'player_id' in df.columns

def test_get_snap_counts(mock_nfl_imports: MockerFixture, sample_snaps: pd.DataFrame):
    mock_nfl_imports.patch("source.statistics.nfl.import_snap_counts", return_value=sample_snaps)
    stats = Statistics.__new__(Statistics)
    stats.seasons = [2021]
    df = stats._get_snap_counts()
    assert 'offense_pct' in df.columns

def test_merge_creates_correct_df(mocker: MockerFixture, sample_seasonal: pd.DataFrame, sample_snaps: pd.DataFrame):
    stats = Statistics.__new__(Statistics)
    stats.seasonal_data = sample_seasonal.drop(columns=['season', 'season_type']).groupby('player_id').mean().reset_index()
    stats.snap_counts = sample_snaps.groupby('pfr_player_id').mean().reset_index()
    stats.player_to_pfr = defaultdict(lambda: None, {'id1': 'pfr1', 'id2': 'pfr2'})
    df = stats._merge()
    assert 'offense_pct' in df.columns

def test_partition_groups_by_position():
    stats = Statistics.__new__(Statistics)
    stats.key = defaultdict(lambda: None, {'id1': ('Player One', 'QB'), 'id2': ('Player Two', 'RB')})
    df = pd.DataFrame({'player_id': ['id1', 'id2'],
                       'fantasy_points': [200, 150],
                       'fantasy_points_ppr': [220, 170]})
    df = df.set_index('player_id').reset_index()
    result = stats._partition(df)
    assert 'QB' in result
    assert 'RB' in result
    assert 'Player One' in result['QB'].index

def test_filter_df_filters_columns():
    stats = Statistics.__new__(Statistics)
    df = pd.DataFrame({'stat1': [0, 0, 0],
                       'stat2': [1, 2, 3],
                       'stat3': [0, 0, 1]})
    result = stats._filter_df(df)
    assert 'stat1' not in result.columns
    assert 'stat2' in result.columns

def test_create_ratings_calls_regression(mocker: MockerFixture):
    mock_regression = mocker.patch("source.statistics.Regression")
    instance = mock_regression.return_value
    instance.get_ratings.return_value = pd.DataFrame({'player_name': ['a'], 'rating': [1.0]})
    stats = Statistics.__new__(Statistics)
    df = pd.DataFrame({'fantasy_points': [100, 200],
                       'fantasy_points_ppr': [110, 210],
                       'stat1': [5, 10]}, index = ['Player A', 'Player B'])
    result = stats._create_ratings(df)
    assert 'rating' in result.columns
    mock_regression.assert_called_once()

def test_get_statistics_pipeline(mocker: MockerFixture, sample_roster: pd.DataFrame, sample_seasonal: pd.DataFrame, sample_snaps: pd.DataFrame):
    mocker.patch("source.statistics.nfl.import_seasonal_rosters", return_value = sample_roster)
    mocker.patch("source.statistics.nfl.import_seasonal_data", return_value = sample_seasonal)
    mocker.patch("source.statistics.nfl.import_snap_counts", return_value = sample_snaps)
    mock_regression = mocker.patch("source.statistics.Regression")
    mock_instance = mock_regression.return_value
    mock_instance.get_ratings.return_value = pd.DataFrame({'player_name': ['Player One', 'Player Two'],
                                                           'rating': [1.0, 0.5]}).set_index('player_name')
    stats = Statistics([2021])
    result = stats.get_statistics()
    assert 'QB' in result or 'RB' in result