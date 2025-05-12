import pytest

import pandas as pd

from core.regression import Regression

@pytest.fixture
def sample_data():
    X = pd.DataFrame({'stat1': [1.0, 2.0, 3.0, 4.0, 5.0],
                      'stat2': [2.0, 3.0, 4.0, 5.0, 6.0],
                      'stat3': [3.0, 4.0, 5.0, 6.0, 7.0]})
    y = pd.Series([10, 20, 30, 40, 50])
    return X, y

def test_train_ridge_regression_returns_model_and_score(sample_data: tuple):
    X, y = sample_data

    reg = Regression(X, y)
    model, score = reg._train_ridge_regression()

    assert hasattr(model, 'coef_')
    assert isinstance(score, float)

def test_weights_are_computed_correctly(sample_data: tuple):
    X, y = sample_data

    reg = Regression(X, y)
    weights = reg.weights

    assert isinstance(weights, dict)
    assert all(col in weights for col in X.columns)

def test_calculate_rating_outputs_series(sample_data: tuple):
    X, y = sample_data

    reg = Regression(X, y)
    rating_series = reg._calculate_rating()

    assert isinstance(rating_series, pd.Series)
    assert len(rating_series) == len(X)

def test_get_ratings_adds_rating_column(sample_data: tuple):
    X, y = sample_data

    reg = Regression(X.copy(), y)
    rated_df = reg.get_ratings()

    assert 'rating' in rated_df.columns
    assert rated_df['rating'].is_monotonic_decreasing or rated_df['rating'].is_monotonic_increasing