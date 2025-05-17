import pandas as pd

import requests
from bs4 import BeautifulSoup

import logging
import traceback

logger = logging.getLogger(__name__)

class ESPNDepthChart:
    def __init__(self):
        self.teams = ["ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE", "DAL", "DEN", "DET", "GB", "HOU", "IND", "JAX", "KC", "LV", "LAC", "LAR", "MIA", "MIN", "NE", "NO", "NYG", "NYJ", "PHI", "PIT", "SF", "SEA", "TB", "TEN", "WSH"]

    def _get_soup(self, team: str):
        url = f"https://www.espn.com/nfl/team/depth/_/name/{team}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    def _parse_soup(self, soup: BeautifulSoup) -> tuple:
        position_table = soup.find_all("table")[0]
        player_table = soup.find_all("table")[1]

        positions = []
        for td in position_table.find_all("td"):
            text = td.get_text(strip=True)
            if text:
                positions.append(text)
        
        players = []
        tbody = player_table.find("tbody")
        if tbody:
            for td in tbody.find_all("td"):
                players.append(td.get_text(strip=True))

        return positions, players

    def _create_depth_chart(self, positions: list, players: list) -> pd.DataFrame:
        roster = {}
        for idx, pos in enumerate(positions):
            if pos in ['QB', 'RB', 'WR', 'TE']:
                start_idx = idx * 4
                group = players[start_idx:start_idx + 4]
                if pos not in roster:
                    roster[pos] = []
                roster[pos].append(group)
                
        rows = []
        for pos, position_group in roster.items():
            for g in position_group:
                rows.append({'Position': pos,
                             'Starter':  g[0] if len(g) > 0 else None,
                             '2nd':      g[1] if len(g) > 1 else None,
                             '3rd':      g[2] if len(g) > 2 else None,
                             '4th':      g[3] if len(g) > 3 else None})

        return pd.DataFrame(rows).set_index("Position").replace(r'(Q|D|O|IR|PUP|NFI|SUS)$', '', regex=True)

    def execute(self) -> dict:
        rosters = {}
        for team in self.teams:
            try:
                soup = self._get_soup(team)
                positions, players = self._parse_soup(soup)
                rosters[team] = self._create_depth_chart(positions, players).rename_axis(team)
            except Exception as e:
                tb = traceback.format_exc(limit=1)
                logger.warning(f"[execute] {team} failed: {type(e).__name__} - {e}\nContext: {tb}")
        return rosters