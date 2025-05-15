import pytest
from pytest_mock import MockerFixture

import pandas as pd

from core.ndpdepthchart import NDPDepthChart

@pytest.fixture
def sample_depth_chart():
    return pd.DataFrame({'week': [1, 1, 1, 1],
                         'formation': ['Offense', 'Offense', 'Offense', 'Offense'],
                         'football_name': ['John', 'Mike', 'Chris', 'James'],
                         'last_name': ['Doe', 'Smith', 'Johnson', 'Brown'],
                         'club_code': ['BUF', 'BUF', 'BUF', 'KC'],
                         'depth_team': [1, 1, 1, 1],
                         'position': ['QB', 'RB', 'WR', 'TE']})

def test_get_master_depth_chart_filters_and_renames(mocker: MockerFixture, sample_depth_chart: pd.DataFrame):
    mocker.patch("core.ndpdepthchart.nfl.import_depth_charts", return_value = sample_depth_chart)
    chart = NDPDepthChart([2021], week=1)
    df = chart.master_depth_chart
    assert 'full_name' in df.columns
    assert all(df['full_name'].str.contains(' '))
    assert set(df['position']).issubset({'QB', 'RB', 'WR', 'TE'})

def test_partition_teams_returns_dict_of_dataframes(mocker: MockerFixture, sample_depth_chart: pd.DataFrame):
    mocker.patch("core.ndpdepthchart.nfl.import_depth_charts", return_value = sample_depth_chart)
    chart = NDPDepthChart([2021], week=1)
    partitions = chart._partition_teams()
    assert isinstance(partitions, dict)
    assert 'BUF' in partitions
    assert isinstance(partitions['BUF'], pd.DataFrame)

def test_create_depth_chart_structure():
    chart = NDPDepthChart.__new__(NDPDepthChart)
    df = pd.DataFrame({'position': ['QB', 'RB', 'RB', 'WR', 'TE', 'TE'],
                       'full_name': ['A', 'B', 'C', 'D', 'E', 'F']})
    result = chart._create_depth_chart(df)
    assert isinstance(result, pd.DataFrame)
    assert result.index.name == 'Position'
    assert 'Starter' in result.columns
    assert '2nd' in result.columns
    assert '3rd' in result.columns
    assert result.loc['RB', '2nd'] == 'C'

def test_get_depth_charts_pipeline(mocker: MockerFixture, sample_depth_chart: pd.DataFrame):
    mocker.patch("core.ndpdepthchart.nfl.import_depth_charts", return_value = sample_depth_chart)
    chart = NDPDepthChart([2021], week=1)
    result = chart.get_depth_charts()
    assert isinstance(result, dict)
    for team, df in result.items():
        assert isinstance(df, pd.DataFrame)
        assert df.index.name == team