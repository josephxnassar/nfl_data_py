# NFL Data Analysis Tool

This project provides a suite of tools to collect, process, and analyze NFL player depth charts and statistics from multiple sources. It integrates data from **nfl_data_py**, ESPN, and performs rating calculations via ridge regression. It also provides the ability to export processed data to Excel.

---

## 📂 Modules

### 1. [`Statistics`](./core/statistics.py)
Processes NFL seasonal data by organizing into position and running a regression algorithm.

### 2. [`Regression`](./core/regression.py)
Handles the ridge regression model used to calculate player or team ratings based on statistical input data.

### 3. [`Schedules`](./core/schedules.py)
Processes NFL schedule data by inserting bye weeks where games are missing from the schedule.

### 4. [`NDPDepthChart`](./core/ndpdepthchart.py)
Retrieves offensive player depth charts from `nfl_data_py`.  
> ⚠️ This data is programmatically accessible and can be run frequently but may not be up-to-date.

### 5. [`ESPNDepthChart`](./core/espndepthchart.py)
Scrapes player depth chart information directly from ESPN’s website.  
> ⚠️ More up-to-date, but web scraping is less stable and slower due to rate limiting.

### 6. [`Excel`](./core/excel.py)
Handles structured output of pandas DataFrames to formatted Excel files using the `xlwings` library.

---

## ▶️ Running the Program

To successfully run the project, follow these steps:

### 1. 📦 Install Dependencies
Install required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

Ensure the following are included with the correct versions stated inside requirements.txt:
- `pandas`
- `xlwings`
- `scikit-learn`
- `beautifulsoup4`
- `requests`
- `nfl_data_py`

Additionally, `xlwings` may require Microsoft Excel to be installed locally.

### 2. 🧩 Structure the Codebase

Your codebase should be structured something like:

```
project-core/
├── regression.py
├── excel.py
├── schedules.py
├── ndpdepthchart.py
├── espndepthchart.py
main.py
```

### 3. 🚀 Example Execution

To pull and output depth charts from ESPN:

```python
from core import ESPNDepthChart
from core import Excel

espn = ESPNDepthChart()
excel = Excel("output_file.xlsm")
excel.output_dfs(espn.get_depth_charts(), "output_sheet")
excel.close()
```

To calculate nnd sort statistics by rating:

```python
from core import Statistics

stats = Statistics([2024])
excel = Excel("output_file.xlsm")
excel.output_dfs(stats.get_statistics(), "output_sheet")
excel.close()
```

---

## 📘 Documentation

Each module's documentation can be found in the respective Markdown files:

- [`regression.md`](./docs/regression.md)
- [`excel.md`](./docs/excel.md)
- [`schedules.md`](./docs/schedules.md)
- [`ndpdepthchart.md`](./docs/ndpdepthchart.md)
- [`espndepthchart.md`](./docs/espndepthchart.md)

---

## 🛠️ Notes

- The `ESPNDepthChart` class introduces random delays between requests to avoid being blocked.
- The `NDPDepthChart` class gracefully exits on HTTP errors.
- You must handle missing data carefully during regression and when creating depth charts.

---

## 👨‍💻 Author

Created by Joseph Nassar, 2025  
