import openpyxl

def main():
    test_workbook = 'C:\\Users\\augus\\Documents\\python\\babel\\kaleidoscope\\texts\\pride and prejudice.xlsx'
    workbook = openpyxl.load_workbook(test_workbook)

    dicto = {}

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
                    
    workbook.save(test_workbook)

if __name__ == "__main__":
    main()

'''[sheet.cell(row=counter+3, column=i).value if (i <= 4 and i is not None and i.isspace() and j == 'until changed') else "" for i, j in enumerate(list(dicto.values())[4:], start=5)]'''