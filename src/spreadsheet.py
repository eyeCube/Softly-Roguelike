'''
    speadsheet.py
    Softly Into the Night, a sci-fi/Lovecraftian roguelike
    Copyright (C) 2020 Jacob Wharton.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>
'''

import xlrd
import os

class SSheet:
        
    @classmethod
    def getData(cls,file):
        loc = os.path.join(os.curdir, file)

        try:
            wb = xlrd.open_workbook(loc)
        except:
            print("failed to open spreadsheet '", file, "'.")
        try:
            sheet = wb.sheet_by_index(0)
        except:
            print("failed to open spreadsheet '", file, "': sheet index 0.")

        print("successfully loaded spreadsheet '", file, "'. Reading...")
        
        cols = [] #headers; determine order of row data
        for i in range(sheet.ncols):
            val = sheet.cell_value(0, i)
            cols.append(val)
        rows = []
        for i in range(sheet.nrows-1): #ignore top row (column headers)
            item = []
            for j in range(sheet.ncols):
                val = sheet.cell_value(i+1, j)
                item.append(val)
            rows.append(item)
            
        print("successfully read spreadsheet '", file, "'.")
        return (cols, rows,)
    #













            
