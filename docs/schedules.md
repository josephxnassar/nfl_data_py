# `Schedules` Class

The [`Schedules`](../core/schedules.py) class provides functionality for importing and organizing NFL schedule data. It extracts regular season matchups, and partitions them by team..

---

## Table of Contents

- [Initialization](#initialization)
- [Methods](#methods)
  - [`_get_master_schedule() -> pd.DataFrame`](#_get_master_schedule---pddataframe)
  - [`_get_weeks() -> int`](#_get_weeks---int)
  - [`_partition_schedules() -> dict[str, pd.DataFrame]`](#_partition_schedules---dictstr-pddataframe)
  - [`_get_bye_weeks(df: pd.DataFrame) -> pd.DataFrame`](#_get_bye_weeksdf-pddataframe---pddataframe)
  - [`get_schedules() -> dict[str, pd.DataFrame]`](#get_schedules---dictstr-pddataframe)
- [Example Usage](#example-usage)

---

## Initialization

```python
Schedules(seasons: List[int])
```

### Parameters:
- `seasons` (`list[int]`): List of years to import schedules for (e.g., `[2023, 2024]`).

### Raises:
- `HTTPError`: If the API call fails when retrieving schedules.

---

## Methods

### `_get_master_schedule() -> pd.DataFrame`

Fetches regular season schedules using `import_schedules()` from the `nfl_data_py` API. Filters the data to include only regular season games (`game_type == 'REG'`), and selects the relevant columns: `week`, `away_team`, and `home_team`.

#### Returns:
- `pd.DataFrame`: A DataFrame of regular season matchups.

#### Raises:
- `HTTPError`: If the API call fails. The error is printed and the program exits.

---

### `_get_weeks() -> int`

Calculates the total number of unique weeks in the schedule.

#### Returns:
- `int`: The number of weeks in the season.

---

### `_partition_schedules() -> dict[str, pd.DataFrame]`

Partitions the full schedule by team. For each game, both the home and away teams are added to a dictionary that maps teams to their opponents per week.

- Each team's data is converted into a DataFrame indexed by week.
- The index is named after the team and sorted by week.

#### Returns:
- `dict`: A dictionary mapping team abbreviations to their opponent schedules in DataFrame form.

---

### `_get_bye_weeks(df: pd.DataFrame) -> pd.DataFrame`

Inserts any missing weeks into each team's DataFrame as a bye week.

#### Parameters:
- `df` (`pd.DataFrame`): A DataFrame of a team's schedule indexed by week.

#### Returns:
- `pd.DataFrame`: A DataFrame with all weeks from 1 to `self.weeks`, including BYEs where applicable.

---

### `get_schedules() -> dict[str, pd.DataFrame]`

Constructs full schedules for each team, including bye weeks. Combines `_partition_schedules()` and `_get_bye_weeks()` to produce the final result.

#### Returns:
- `dict`: A dictionary where each key is a team abbreviation and the value is a complete schedule DataFrame.

---

## Example Usage

```python
from core import Schedules
from core import Excel

schedule = Schedules([2024])
excel = Excel("output_file.xlsm")
excel.output_dfs(schedule.get_schedules(), "output_sheet")
excel.close()
```

---