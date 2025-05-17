import pandas as pd

from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class Regression:
    def __init__(self, X: pd.DataFrame, y: pd.Series):
        self.X = X
        self.y = y
        self.weights = self._get_weights()
    
    def _train_ridge_regression(self) -> tuple:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(self.X)
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, self.y, test_size=0.2, shuffle=True)
        
        ridge = Ridge(alpha=1.0)
        ridge.fit(X_train, y_train)
        
        score = ridge.score(X_test, y_test)
        
        return ridge, score
    
    def _get_weights(self) -> dict:
        ridge, _ = self._train_ridge_regression()
        return {col: weight for col, weight in zip(self.X.columns, ridge.coef_)}
    
    def _calculate_rating(self) -> pd.Series:
        return self.X.apply(lambda row: sum(row[col] * self.weights[col] for col in row.index if col in self.weights), axis=1)
    
    def execute(self):
        self.X['rating'] = self._calculate_rating()
        return self.X.sort_values(by='rating', ascending=False)