import pytest
from pytest_mock import MockerFixture

import pandas as pd

from bs4 import BeautifulSoup

from core.espndepthchart import ESPNDepthChart

@pytest.fixture
def fake_soup():
    html = '''
    <html>
        <body>
            <table>
                <tr><td>QB</td></tr>
                <tr><td>RB</td></tr>
            </table>
            <table>
                <tbody>
                    <tr><td>Player A</td></tr>
                    <tr><td>Player B</td></tr>
                    <tr><td>Player C</td></tr>
                    <tr><td>Player D</td></tr>
                    <tr><td>Player E</td></tr>
                    <tr><td>Player F</td></tr>
                    <tr><td>Player G</td></tr>
                    <tr><td>Player H</td></tr>
                </tbody>
            </table>
        </body>
    </html>
    '''
    return BeautifulSoup(html, 'html.parser')

def test_parse_soup_extracts_positions_and_players(fake_soup: BeautifulSoup):
    e = ESPNDepthChart()
    positions, players = e._parse_soup(fake_soup)
    assert positions == ['QB', 'RB']
    assert 'Player A' in players
    assert len(players) == 8

def test_create_depth_chart_structure():
    e = ESPNDepthChart()
    positions = ['QB', 'RB']
    players = ['Player A', 'Player B', 'Player C', 'Player D',
               'Player E', 'Player F', 'Player G', 'Player H']
    df = e._create_depth_chart(positions, players)
    assert isinstance(df, pd.DataFrame)
    assert 'Starter' in df.columns
    assert '2nd' in df.columns
    assert '3rd' in df.columns
    assert df.index.name == 'Position'
    assert 'QB' in df.index or 'RB' in df.index


def test_get_depth_charts_single_team(mocker: MockerFixture, fake_soup: BeautifulSoup):
    mocker.patch.object(ESPNDepthChart, '_get_soup', return_value=fake_soup)
    mocker.patch('time.sleep')  # skip delays
    chart = ESPNDepthChart()
    chart.teams = ['FAKE']
    result = chart.get_depth_charts()
    assert isinstance(result, dict)
    assert 'FAKE' in result
    assert isinstance(result['FAKE'], pd.DataFrame)