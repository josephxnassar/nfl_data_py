import pytest
from unittest.mock import MagicMock

import pandas as pd

from core.excel import Excel

filename = "dummy.xlsm"

@pytest.fixture
def dfs():
    return {"Sheet1": pd.DataFrame({"A": [1, 2], "B": [3, 4]}),
            "Sheet2": pd.DataFrame({"X": [5, 6], "Y": [7, 8]})}

def test_excel_init_with_existing_file(mocker):
    mock_exists = mocker.patch("core.excel.os.path.exists", return_value = True)
    mock_book = mocker.patch("core.excel.xw.Book")
    Excel(filename)
    mock_exists.assert_called_once_with(filename)
    mock_book.assert_called_once_with(filename)

def test_excel_init_without_existing_file(mocker):
    mock_exists = mocker.patch("core.excel.os.path.exists", return_value = False)
    mock_book = mocker.patch("core.excel.xw.Book")
    mock_instance = MagicMock()
    mock_book.return_value = mock_instance
    Excel(filename)
    mock_exists.assert_called_once_with(filename)
    mock_instance.save.assert_called_once_with(filename)

def test_find_next_column():
    e = Excel.__new__(Excel)
    assert e._find_next_column("A", 1) == "B"
    assert e._find_next_column("Z", 1) == "AA"
    assert e._find_next_column("AZ", 1) == "BA"

def test_generate_lookup(dfs):
    e = Excel.__new__(Excel)
    lookup = e._generate_lookup(dfs)
    assert "Sheet1" in lookup and "Sheet2" in lookup
    assert isinstance(lookup['Sheet1'], str)

def test_output_dfs(mocker, dfs):
    mock_book = mocker.patch("core.excel.xw.Book")
    mock_sheet = MagicMock()
    mock_sheet.name = "MySheet"
    mock_sheet.used_range.columns = [MagicMock()]
    mock_sheet.used_range.api = MagicMock()
    mock_sheet.cells.clear = MagicMock()
    mock_wb = MagicMock()
    mock_sheets = MagicMock()
    mock_sheets.__getitem__.return_value = mock_sheet
    mock_sheets.add.return_value = mock_sheet
    mock_wb.sheets = mock_sheets
    mock_book.return_value = mock_wb
    e = Excel(filename)
    e._generate_lookup = MagicMock(return_value={"Sheet1": "B2", "Sheet2": "B6"})
    e._output_table = MagicMock()
    e.output_dfs(dfs, "MySheet")
    assert e._output_table.call_count == 2
    mock_sheet.cells.clear.assert_called_once()

def test_close(mocker):
    mock_book = mocker.patch("core.excel.xw.Book")
    mock_instance = MagicMock()
    mock_book.return_value = mock_instance
    e = Excel(filename)
    e.close()
    mock_instance.close.assert_called_once_with()