# `Excel` Class

The [`Excel`](../core/excel.py) provides a class to output dataframes to an excel workbook using the `xlwings` library.  Each instance of this class should represent one excel file.

---

## Table of Contents

- [Initialization](#initialization)
- [Methods](#methods)
  - [`_find_next_column(old_column: str, length: int) -> str`](#_find_next_columnold_column-str-length-int---str)
  - [`_generate_lookup(dfs: dict) -> dict[str, str]`](#_generate_lookupdfs-dict---dictstr-str)
  - [`_output_table(sheet: xw.Sheet, df: pd.DataFrame, name: str, coordinate: str) -> None`](#_output_tablesheet-xwsheet-df-pddataframe-name-str-coordinate-str---none)
  - [`output_dfs(dfs: dict, sheet_name: str) -> None`](#output_dfsdfs-dict-sheet_name-str---none)
  - [`close() -> None`](#close---none)
- [Example Usage](#example-usage)

---

## Initialization

```python
Excel(filename: str)
```

### Parameters:
- `filename` (`str`): The path to the Excel file. If the file exists, it is opened. Otherwise, a new file is created and saved.

---

## Methods

### `_find_next_column(old_column: str, length: int) -> str`

Calculates the next Excel column label based on a starting column and offset length.

#### Parameters:
- `old_column` (`str`): Starting column label (e.g., `"B"`).
- `length` (`int`): Number of columns to move forward.

#### Returns:
- `str`: New Excel column label.

---

### `_generate_lookup(dfs: dict) -> dict[str, str]`

Generates a mapping of DataFrame keys to Excel cell coordinates for output placement.

#### Parameters:
- `dfs` (`dict`): Dictionary where keys are table names and values are pandas DataFrames.

#### Returns:
- `dict`: Dictionary mapping each key to its cell coordinate in the Excel sheet.

---

### `_output_table(sheet: xw.Sheet, df: pd.DataFrame, name: str, coordinate: str) -> None`

Outputs a single DataFrame as a formatted Excel table starting at the specified cell.

#### Parameters:
- `sheet` (`xw.Sheet`): Excel sheet to write to.
- `df` (`pd.DataFrame`): DataFrame to output.
- `name` (`str`): Table name.
- `coordinate` (`str`): Starting cell location (e.g., `"B2"`).

#### Side Effects:
- Writes the DataFrame to the sheet.
- Formats the data as a table with fixed number formatting and no filters.

---

### `output_dfs(dfs: dict, sheet_name: str) -> None`

Writes multiple DataFrames to an Excel worksheet in a structured grid layout.

#### Parameters:
- `dfs` (`dict`): Dictionary of table names and DataFrames.
- `sheet_name` (`str`): Name of the worksheet to write to. The sheet is cleared before writing.

#### Side Effects:
- Adds or clears the specified sheet.
- Auto-resizes columns and aligns text left.

---

### `close() -> None`

Closes the Excel workbook.

---

## Example Usage

```python
from core import Excel

excel = Excel("output_file.xlsm")
excel.output_dfs(dataframes_dict, "output_sheet")
excel.close()
```

---
