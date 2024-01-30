import openpyxl

test_workbook = 'C:\\Users\\augus\\Documents\\python\\babel\\kaleidoscope\\texts\\pride and prejudice.xlsx'
workbook = openpyxl.load_workbook(test_workbook)

for row in range(3, 14):
    workbook["1"]["E" + str(row)].value = None
    print(f"Cleared cell {workbook['1']['E' + str(row)]}")

workbook["1"]["E3"].value = "asdfghjkl;"
workbook["1"]["E8"].value = "qwertyuiop"

dicto = {}
'''for sheet in workbook: 
    for col, cell in enumerate(sheet[1], start=1):
        dicto[f'{cell.value}'] = sheet.cell(row=2, column=col).value
    for col in sheet.iter_cols():
        if (col[1].value == "until changed"):
            value_to_copy = None
            for row, cell in enumerate(col[2:], start=3):
                if value_to_copy is not None:
                    if cell.value is None or cell.value.isspace():
                        print(f"changing {cell} value to {value_to_copy}")
                        cell.value = value_to_copy
                    else:
                        value_to_copy = cell.value
                        print(f'new  value to copy: {value_to_copy}')
                elif cell.value is not None and not cell.value.isspace():
                    value_to_copy = cell.value'''

for sheet in workbook: 
    for col, cell in enumerate(sheet[1], start=1):
        dicto[f'{cell.value}'] = sheet.cell(row=2, column=col).value
    for col in sheet.iter_cols():
        if (col[1].value == "until changed"):
            value_to_copy = None
            for cell in col[2:]:
                if cell.value is None or cell.value.isspace():
                    if value_to_copy is not None:
                        print(f"changing {cell} value to {value_to_copy}")
                        cell.value = value_to_copy
                else:
                    value_to_copy = cell.value
                    print(f'new value to copy: {value_to_copy}')
                

for row in workbook["1"]:
    for cell in row:
        print(cell.value)

print(dicto)

'''[sheet.cell(row=counter+3, column=i).value if (i <= 4 and i is not None and i.isspace() and j == 'until changed') else "" for i, j in enumerate(list(dicto.values())[4:], start=5)]'''