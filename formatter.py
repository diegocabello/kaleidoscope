import openpyxl
import subprocess

def format_prompts(book_name=None):

    if not book_name:
        book_name = 'alice in wonderland'
    workbook = openpyxl.load_workbook(f'texts\\{book_name}.xlsx')

    list_of_keys = []
    dicto_change = {}
    dicto_values = {}

    list_of_prompts = []

    with open(f'prompts\\{book_name} prompts.txt', 'w') as filer:
        filer.write('')

    initialize_flag = True
    for sheet_counter, sheet in enumerate(workbook): 
        if initialize_flag:
            for col, cell in enumerate(sheet[1], start=1):
                dicto_change[f'{str(cell.value)}'] = sheet.cell(row=2, column=col).value
                dicto_values[f'{str(cell.value)}'] = None
                list_of_keys.append(str(cell.value))
            for col, cell in enumerate(sheet[2], start=1): 
                dicto_change[list_of_keys[col - 1]] = str(cell.value) if cell.value != None else None
            print(dicto_change)
            print(list_of_keys)
            initialize_flag = False
        
        for row_counter, row in enumerate(sheet.iter_rows(min_row = 3)):
            return_string = f'**chapter {sheet_counter + 1} row {row_counter + 3}**\n'
            for cell_counter, cell in enumerate(row):

                stringer = str(cell.value).strip() if cell.value != None else None
                category = list_of_keys[cell_counter]
                one_shot_bool = dicto_change[category] == 'one shot'
                until_changed_bool = dicto_change[category] == 'until changed'   # until_changed_bool = True if dicto_change[category] == 'until changed' else False
                isnt_none_bool = stringer is not None  # isnt_none_bool = True if stringer != None else False

                if until_changed_bool and isnt_none_bool:
                    dicto_values[category] = stringer
                    return_string = return_string + f'{category}: {stringer} \n'
                elif (one_shot_bool or category == 'sentence') and isnt_none_bool:
                    return_string = return_string + f'{category}: {stringer} \n'
                elif until_changed_bool and not isnt_none_bool and dicto_values[category] is not None:
                    return_string = return_string + f'{category}: {dicto_values[category]} \n'            

            with open(f'prompts\\{book_name} prompts.txt', 'a') as filer:
                filer.write(return_string + '\n\n')

        dicto_values = {key: None for key in dicto_values} # resets at the end of each sheet
        print(f'did sheet {str(sheet_counter + 1)} ')

    subprocess.run(f'start notepad prompts\\{book_name} prompts.txt', shell=True)

    return list_of_prompts

if __name__ == "__main__":
    format_prompts()

