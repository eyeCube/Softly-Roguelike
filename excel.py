import xlsxwriter as xl
import data

wb = xl.Workbook("weapons.xlsx")
sheet = wb.add_worksheet()

row = 0
col = 1

sheet.write(0, 0, "name")
sheet.write(0, 1, "value")
sheet.write(0, 2, "hp")
sheet.write(0, 3, "material")
sheet.write(0, 4, "strength")
sheet.write(0, 5, "dexterity")
sheet.write(0, 6, "atk")
sheet.write(0, 7, "dmg")
sheet.write(0, 8, "pen")
sheet.write(0, 9, "dfn")
sheet.write(0, 10, "arm")
sheet.write(0, 11, "pro")
sheet.write(0, 12, "asp")
sheet.write(0, 13, "enc")
sheet.write(0, 14, "gra")
sheet.write(0, 15, "ctr")
sheet.write(0, 16, "stamina") # stamina cost
sheet.write(0, 17, "skill")
sheet.write(0, 18, "script")

for name, datum in data.WEAPONS.items():
    sheet.write(row, col, name)
    sheet.write(row, col, datum[0])
    sheet.write(row, col, datum[1])
    sheet.write(row, col, datum[2])
    sheet.write(row, col, datum[3])
    sheet.write(row, col, datum[4])
    sheet.write(row, col, datum[5])
    sheet.write(row, col, datum[6][0])
    sheet.write(row, col, datum[6][1])
    sheet.write(row, col, datum[6][2])
    sheet.write(row, col, datum[6][3])
    sheet.write(row, col, datum[6][4])
    sheet.write(row, col, datum[6][5])
    sheet.write(row, col, datum[6][6])
    sheet.write(row, col, datum[6][7])
    sheet.write(row, col, datum[6][8])
    sheet.write(row, col, datum[6][9])
    sheet.write(row, col, datum[6][10])
    sheet.write(row, col, datum[7])
    sheet.write(row, col, datum[8])

wb.close()

