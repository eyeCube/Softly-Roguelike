'''
speadsheet.py
functions to get metadata from spreadsheets and load it into the game
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













            
