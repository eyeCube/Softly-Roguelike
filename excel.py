import xlsxwriter as xl
import data as d

wb = xl.Workbook("weapons.xlsx")
sheet = wb.add_worksheet()

row = 0
col = 1

for name, data in d.WEAPONS.items():
    sheet.write(row, col, name)
    sheet.write(row, col, data[0])
    sheet.write(row, col, data[1])
    sheet.write(row, col, data[2])
    sheet.write(row, col, data[3])
    sheet.write(row, col, data[4])
    sheet.write(row, col, data[5])
    sheet.write(row, col, data[6][0])
    sheet.write(row, col, data[6][1])
    sheet.write(row, col, data[6][2])
    sheet.write(row, col, data[6][3])
    sheet.write(row, col, data[6][4])
    sheet.write(row, col, data[6][5])
    sheet.write(row, col, data[6][6])
    sheet.write(row, col, data[6][7])
    sheet.write(row, col, data[6][8])
    sheet.write(row, col, data[6][9])
    sheet.write(row, col, data[6][10])
    sheet.write(row, col, data[7])
    sheet.write(row, col, data[8])
