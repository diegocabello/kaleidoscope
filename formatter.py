import subprocess

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side

initial_bit_color = "7A808C"          # light grey
alternate_bit_color = "1E1F21"        # dark grey 
ignore_color = "2A4225"               # green-grey  

def format_prompts(book_name=None):

    if not book_name:
        book_name = 'pride and prejudice'
    workbook = openpyxl.load_workbook(f'texts\\{book_name}.xlsx')

    list_of_keys = []
    dicto_change = {}
    dicto_values = {}

    list_of_prompts = []
    list_of_bits = []

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
        
        bit_counter = 1
        bit_color = initial_bit_color
        bit_values = {key: None for key in dicto_values} 
        return_string = f'**chapter {sheet_counter + 1} bit {bit_counter}**\n'

        for row in sheet.iter_rows(min_row = 3):

            for cell_counter, cell in enumerate(row):
                
                if cell_counter == 0:
                    prev_bit_color = bit_color 
                    bit_color = cell.fill.start_color.rgb[2:]

                    if prev_bit_color != bit_color:                      # formats and resets everything at the end of each bit   
                        bit_counter += 1

                        if bit_values['frame'] == 'speaker':
                            return_string = return_string + f'{bit_values["speaker"]} is speaking to {bit_values["spoken to"]} in {bit_values["setting"]}\n\
                                  {"also present are" + bit_values["also present"] if bit_values["also present"] != None else "" if "also present" in bit_values else ""}\n\
                                      style: {bit_values["style"]}'

                        else:
                            for value in bit_values:
                                if bit_values[value] != None:
                                    return_string = return_string + f'{value}: {bit_values[value]} \n'

                        list_of_prompts.append(return_string)
                        with open(f'prompts\\{book_name} prompts.txt', 'a') as filer:
                            filer.write(return_string + '\n\n')

                        return_string = f'**chapter {sheet_counter + 1} bit {bit_counter}**\n' # resets each bit
                        bit_values = {key: None for key in dicto_values} 


                elif cell.fill.start_color.rgb[2:] != ignore_color:

                    cell_value = str(cell.value).strip() if cell.value != None else None
                    category = list_of_keys[cell_counter]

                    one_shot_bool = dicto_change[category] == 'one shot'            # isnt either/or, there are other options 
                    until_changed_bool = dicto_change[category] == 'until changed'   
                    isnt_none_bool = cell_value is not None  

                    if until_changed_bool and isnt_none_bool:
                        bit_values[category] = cell_value
                        dicto_values[category] = cell_value
                    elif (one_shot_bool or category == 'sentence') and isnt_none_bool:
                        bit_values[category] = bit_values[category] + cell_value if bit_values[category] != None else cell_value
                    elif until_changed_bool and not isnt_none_bool:      # so if it is none
                        bit_values[category] = dicto_values[category] 
                        #return_string = return_string + f'{category}: {bit_category_value} \n'            

                    

        dicto_values = {key: None for key in dicto_values} # resets at the end of each sheet
        print(f'did sheet {str(sheet_counter + 1)} ')

    subprocess.run(f'start notepad prompts\\{book_name} prompts.txt', shell=True)

    return {'prompts': list_of_prompts, 'bits': list_of_bits}

if __name__ == "__main__":
    format_prompts()

