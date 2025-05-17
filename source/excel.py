import pandas as pd

import os
import xlwings as xw

import logging
import traceback

logger = logging.getLogger(__name__)

class Excel:
    def __init__(self, filename: str):
        if os.path.exists(filename):
            self.wb = xw.Book(filename)
        else:
            self.wb = xw.Book()
            self.wb.save(filename)

    def _find_next_column(self, old_column: str, length: int) -> str:
        old_index = sum((ord(char.upper()) - ord('A') + 1) * 26 ** i for i, char in enumerate(reversed(old_column)))
        next_index = old_index + length
        next_column = ""
        while next_index > 0:
            next_index, remainder = divmod(next_index - 1, 26)
            next_column = chr(remainder + ord('A')) + next_column
        return next_column
    
    def _generate_lookup(self, dfs: dict) -> dict:
        lookup = {}
        col = "B"
        row = 2
        for idx, (key, df) in enumerate(dfs.items()):
            if idx % 4 == 0 and idx != 0:
                row = 2
                col = self._find_next_column('B', (idx // 4) * (len(df.columns) + 2))
            lookup[key] = f"{col}{row}"
            row += len(df) + 2
        return lookup
    
    def _output_table(self, sheet: xw.Sheet, df: pd.DataFrame, name: str, coordinate: str) -> None:
        sheet.range(coordinate).value = df
        data_range = sheet.range(coordinate).expand()
        table = sheet.api.ListObjects.Add(1, data_range.api, 0, 1, None)
        table.Name = name
        table.ShowAutoFilter = False
        data_range.number_format = '0.'+('0'*1)
    
    def output_dfs(self, dfs: dict, sheet_name: str) -> None:
        lookup = self._generate_lookup(dfs)
        if sheet_name in [s.name for s in self.wb.sheets]:
            sheet = self.wb.sheets[sheet_name]
        else:
            sheet = self.wb.sheets.add(sheet_name)
        sheet.cells.clear()
        for key, df in dfs.items():
            self._output_table(sheet, df, key, lookup[key])
        for c in sheet.used_range.columns:
            c.column_width = 20
        sheet.used_range.api.HorizontalAlignment = xw.constants.HAlign.xlHAlignLeft

    def close(self) -> None:
        self.wb.close()

    # wb.macro('Module2.FindReplaceInHighlightedRanges').run()