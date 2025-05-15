# `NDPDepthChart` Class

The [`NDPDepthChart`](../source/ndpdepthchart.py) class provides functionality for importing and organizing NFL depth chart data for a given week of the season. Unlike `ESPNDepthChart`, it can be run more frequently but may not reflect the most up-to-date information.

---

## Table of Contents

- [Initialization](#initialization)
- [Methods](#methods)
  - [`_get_master_depth_chart() -> pd.DataFrame`](#_get_master_depth_chart---pddataframe)
  - [`_partition_teams() -> dict`](#_partition_teams---dict)
  - [`_create_depth_chart(team_df: pd.DataFrame) -> pd.DataFrame`](#_create_depth_chartteam_df-pddataframe---pddataframe)
  - [`get_depth_charts() -> dict`](#get_depth_charts---dict)
- [Example Usage](#example-usage)

---

## Initialization

```python
NDPDepthChart(seasons: list, week: int)
```

### Parameters:
- `seasons` (`list`): A list of seasons (e.g., `[2023]`) to retrieve depth chart data for.
- `week` (`int`): The specific week of the season for which to fetch offensive depth charts.

---

## Methods

### `_get_master_depth_chart() -> pd.DataFrame`

Retrieves the offensive depth chart data for the given seasons and filters it by the specified week and formation ("Offense").

#### Returns:
- `pd.DataFrame`: A cleaned and sorted DataFrame of offensive depth chart entries with full player names.

#### Raises:
- Exits the program if an `HTTPError` occurs during data retrieval.

---

### `_partition_teams() -> dict`

Partitions the master depth chart into a dictionary of DataFrames keyed by team code.

#### Returns:
- `dict`: Dictionary mapping team codes to their respective depth chart DataFrames.

---

### `_create_depth_chart(team_df: pd.DataFrame) -> pd.DataFrame`

Creates a structured depth chart DataFrame for a single team, listing players by position and depth.

#### Parameters:
- `team_df` (`pd.DataFrame`): DataFrame containing player entries for a single team.

#### Returns:
- `pd.DataFrame`: A DataFrame indexed by position with columns for the starter, 2nd, and 3rd string players.

---

### `get_depth_charts() -> dict`

Builds depth charts for all teams based on the master depth chart.

#### Returns:
- `dict`: Dictionary mapping each team to its formatted depth chart DataFrame, with the index labeled by team code.

---

## Example Usage

```python
from source import NDPDepthChart
from source import Excel

ndp = NDPDepthChart([2023], 1)
excel = Excel("output_file.xlsm")
excel.output_dfs(ndp.get_depth_charts(), "output_sheet")
excel.close()
```

---
