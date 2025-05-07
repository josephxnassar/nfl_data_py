# `Regression` Class

The `Regression` class is designed to perform ridge regression on a given dataset and use the resulting model coefficients to calculate a custom rating for each row in the feature set.

---

## Table of Contents

- [Initialization](#initialization)
- [Methods](#methods)
  - [`_train_ridge_regression() -> tuple[Ridge, float]`](#_train_ridge_regression---tupleridge-float)
  - [`_get_weights() -> dict[str, float]`](#_get_weights---dictstr-float)
  - [`_calculate_rating() -> pd.Series`](#_calculate_rating---pdseries)
  - [`get_ratings() -> pd.DataFrame`](#get_ratings---pddataframe)
- [Example Usage](#example-usage)

---

## Initialization

```python
Regression(X: pd.DataFrame, y: pd.Series)
```

### Parameters:
- `X` (`pd.DataFrame`): The input feature matrix.
- `y` (`pd.Series`): The target variable.

---

## Methods

### `_train_ridge_regression() -> tuple[Ridge, float]`

Scales the input features using `StandardScaler`, splits the dataset into training and testing subsets, and fits a ridge regression model.

#### Returns:
- `tuple`: A tuple containing the trained `Ridge` model and its R² score on the test set.

---

### `_get_weights() -> dict[str, float]`

Trains a ridge regression model and extracts the learned weights for each feature.

#### Returns:
- `dict`: A dictionary mapping feature names to their corresponding model coefficients.

---

### `_calculate_rating() -> pd.Series`

Calculates a custom rating for each row in the feature set by taking the weighted sum of the features using the model coefficients.

#### Returns:
- `pd.Series`: A series of calculated ratings indexed the same as the input DataFrame.

---

### `get_ratings() -> pd.DataFrame`

Adds a `rating` column to the feature DataFrame based on the computed ratings and returns the DataFrame sorted by rating in descending order.

#### Returns:
- `pd.DataFrame`: A DataFrame with an additional `rating` column, sorted by rating.

---

## Example Usage

```python
from core import Regression
import xlwings as xw

# Single df
ratings = Regression(X, y)

wb = xw.Book("output_file.xlsm")
sheet = self.wb.sheets["output_sheet"]
sheet.cells.clear()
sheet.range('B2').value = ratings.get_ratings()
wb.close()
```

---