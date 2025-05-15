# `Statistics` Class

The [`Statistics`](../core/statistics.py) class provides functionality for importing, processing, and analyzing NFL seasonal data. It performs key operations such as merging player data, filtering for relevant statistics, partitioning by player positions, and creating player ratings based on fantasy points.

---

## Table of Contents

- [Initialization](#initialization)
- [Methods](#methods)
  - [`_create_key() -> tuple[dict, dict]`](#_create_key---tupledict-dict)
  - [`_get_seasonal_data() -> pd.DataFrame`](#_get_seasonal_data---pddataframe)
  - [`_get_snap_counts() -> pd.DataFrame`](#_get_snap_counts---pddataframe)
  - [`_merge() -> pd.DataFrame`](#_merge---pddataframe)
  - [`_partition(df: pd.DataFrame) -> dict[str, pd.DataFrame]`](#_partitiondf-pddataframe---dictstr-pddataframe)
  - [`_filter_df(df: pd.DataFrame) -> pd.DataFrame`](#_filter_dfdf-pddataframe---pddataframe)
  - [`_create_ratings(df: pd.DataFrame) -> pd.DataFrame`](#_create_ratingsdf-pddataframe---pddataframe)
  - [`get_statistics() -> dict[str, pd.DataFrame]`](#get_statistics---dictstr-pddataframe)
- [Example Usage](#example-usage)
---

## Initialization

```python
Statistics(year: List[int])
```

### Parameters:
- `year` (`list[int]`): List of years to import data for (e.g., `[2023, 2024]`).

### Raises:
- `HTTPError`: If the API call fails.

---

## Methods

### `_create_key() -> tuple[dict, dict]`

Loads seasonal rosters from `import_seasonal_rosters()` into a DataFrame with the columns: `player_id`, `pfr_id`, `player_name`, and `depth_chart_position`.

Creates two dictionaries using `defaultdict`:
- One mapping `player_id` to a tuple of `(player_name, depth_chart_position)`.
- Another mapping `player_id` to `pfr_id`, if `pfr_id` is available.

Iterates through each row of the seasonal roster DataFrame to populate both dictionaries.

#### Returns:
- `dict`: A dictionary mapping `player_id` to `(player_name, depth_chart_position)`.
- `dict`: A dictionary mapping `player_id` to `pfr_id`.

#### Raises:
- `HTTPError`: If the API call fails (specifically exits on a 404).

---

### `_get_seasonal_data() -> pd.DataFrame`

Loads seasonal data from `import_seasonal_data()` into a DataFrame.

Drops the `season` and `season_type` columns, groups the data by `player_id`, calculates the mean when multiple entries exist for a player, and then resets the index.

#### Returns:
- `pd.DataFrame`: A DataFrame containing seasonal data for the given year.

#### Raises:
- `HTTPError`: If the API call fails (specifically exits on a 404).

---

### `_get_snap_counts() -> pd.DataFrame`

Loads snap count data from `import_snap_counts()` into a DataFrame.

Selects the relevant columns (`pfr_player_id`, `offense_snaps`, `offense_pct`), groups the data by `pfr_player_id`, calculates the mean when multiple entries exist for a player, and then resets the index.

#### Returns:
- `pd.DataFrame`: A DataFrame containing averaged snap counts for the given year.

#### Raises:
- `HTTPError`: If the API call fails (specifically exits on a 404).

---

### `_merge() -> pd.DataFrame`

Merges the `seasonal_data` DataFrame with the `snap_counts` DataFrame based on the `pfr_id` column.

- Adds a `pfr_id` column to `seasonal_data` by mapping `player_id` to `pfr_id` using the `player_to_pfr` dictionary.
- Renames the `pfr_player_id` column in `snap_counts` to `pfr_id` to ensure the correct join.
- Merges the two DataFrames on the `pfr_id` column using a left join.
- Drops the `pfr_id` column after the merge and removes any rows with missing data.

#### Returns:
- `pd.DataFrame`: A DataFrame containing both `seasonal_data` and `snap_counts`.

---

### `_partition(df: pd.DataFrame) -> dict[str, pd.DataFrame]`

Partitions the provided `df` DataFrame by player position, organizing data for each position into separate DataFrames.

- Creates a list of columns starting with `player_name` followed by all other columns in `df`, excluding the first column which is `player_id`.
- Initializes a `defaultdict` of DataFrames, with each DataFrame corresponding to a position (QB, RB, WR, TE).
- Iterates through the rows of `df` and maps player stats to the corresponding player using `self.key`.
- For players with a position of 'QB', 'RB', 'WR', or 'TE', appends their data to the appropriate position's DataFrame.
- Sets `player_name` as the index for each position DataFrame in the final result.

#### Returns:
- `dict`: A dictionary where the keys are player positions ('QB', 'RB', 'WR', 'TE'), and the values are DataFrames containing the corresponding player stats, indexed by `player_name`.

---

### `_filter_df(df: pd.DataFrame) -> pd.DataFrame`

Filters out columns from the `df` DataFrame where more than 10% of the rows have zero values. Only columns with more than 10% non-zero values are retained.

#### Returns:
- `pd.DataFrame`: A DataFrame with only columns that have more than 10% non-zero values.

---

### `_create_ratings(df: pd.DataFrame) -> pd.DataFrame`

Creates ratings based on the `fantasy_points_ppr` column in the `df` DataFrame. This function uses regression to compute ratings by training on the `fantasy_points_ppr` as the target variable and other columns as features.

#### Returns:
- `pd.DataFrame`: A DataFrame with the computed ratings.

---

### `get_statistics() -> dict[str, pd.DataFrame]`

Merges and partitions the seasonal data into position-specific DataFrames. For each position's DataFrame:
- Filters out columns with more than 10% zero values using `_filter_df`.
- Creates ratings for the data using `_create_ratings`.

#### Returns:
- `dict`: A dictionary containing position-specific DataFrames with filtered columns and computed ratings for each player.


## Example Usage

```python
from core import Statistics
from core import Excel

stats = Statistics([2024])
excel = Excel("output_file.xlsm")
excel.output_dfs(s.get_statistics(), "output_sheet")
excel.close()
```

---