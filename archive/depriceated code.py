"""
        # TURN INTO LIST MATRIX IS A LIST OF ROWS
        parent_row_list = []
        for sentence in sentence_list:
            sub_column_list = {'sentence': sentence}
            for x in columns[1:]:
                sub_column_list[x] = None
            parent_row_list.append(sub_column_list)


        # TURN INTO DATAFRAME
        dataframe_list = []
        for sentence in sentence_list:
            to_append = [sentence]
            for x in range(len(columns) - 1):
                to_append.extend([None])
            dataframe_list.append(to_append)
        df = pd.DataFrame(dataframe_list, columns=columns)

        # PUT TEMP WB SHEET INTO MAIN WB 
        if count != 0:
            source_sheet = temp_wb["SheetF"]
            destination_sheet = main_wb.create_sheet(sheet_name)
            for row in source_sheet.iter_rows(values_only=True):
                destination_sheet.append(row)
            del temp_wb['SheetF']
            temp_wb.save(temp_wb_path)
            main_wb.save(main_wb_path)
            main_wb.close()
            temp_wb.close()


        # PUT DATAFRAME INTO TEMP WB 
        with pd.ExcelWriter(temp_wb_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name="SheetF", index=False)

            
        #data_list = [[sentence].extend([None for _ in range(len(columns))]) for sentence in sentence_list]

        df = pd.DataFrame(dataframe_list, columns=columns)

        #sheet = wb[sheet_name] if sheet_name in wb.sheetnames else wb.create_sheet(sheet_name)

        with pd.ExcelWriter(wb_path, engine='openpyxl', mode='a') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)

        #sheet = main_wb[sheet_name] if sheet_name in main_wb.sheetnames else main_wb.create_sheet(sheet_name)


        df.to_excel(wb_path, sheet_name = sheet_name, index=False)

        
        for sentence in sentence_list:
            sheet.append([sentence])
        
        #wb.save(wb_path)
        #wb.close()


    with open('texts\\pnp chapters\\one.txt', 'w') as file:
        file.write('')

    ends_in_quotes = False
    chapter_sentence_and_speaker_dictionary_list = []
    for sentence in chapter_sentence_list:

        if chapter_sentence_list.index(sentence) == 0:    ## this gets rid of the annoying beginning quote that messes things up 
            sentence = sentence.text.replace('\r\n\r\n', '')[1:]
        else:
            sentence = sentence.text.replace('\r\n\r\n', '')

        dicto = quote_parser(sentence)
        chapter_sentence_and_speaker_dictionary_list.append(dicto)

        print(sentence)
        print(dicto)
        print('\n')






    chapter_sentence_list = []
    for quot in chapter_split_doublequote:
        chapter_sentence_list.extend(sentencer(inputer = quot))

    for count, chapter in enumerate(chapter_list):
        chapter_list[count] = chapter.split('”\r\n\r\n“') 

    for count, quot in enumerate(chapter_split_doublequote):
        chapter_split_doublequote[count] = '“' + quot + '”'


    if ends_in_quotes:
        if 0 < sentence.find('”') + 1 < len(sentence):
            frag_and_ant_dict = fragmenter(sentence)
            fragments, antecedant = frag_and_ant_dict['lister'], frag_and_ant_dict['speaker']
            if fragments[-1]['ends in quotes']:
                ends_in_quotes = True
            else: 
                ends_in_quotes = False
            if sentence.endswith('”'):
                ends_in_quotes = False
            dicto['sentence'], dicto['ends in quotes'], dicto['fragments'] = sentence, ends_in_quotes, fragments 
        elif sentence.endswith('”'):
            ends_in_quotes = False
            if sentence.endswith('“'): # this would never happen but i included it for symmetry
                ends_in_quotes = True  # this would never happen but i included it for symmetry
            dicto['sentence'], dicto['ends in quotes'], dicto['speaker'] = sentence, ends_in_quotes, 'narrator'
        else:
            dicto['sentence'], dicto['ends in quotes'] = sentence, True
    elif not ends_in_quotes:
        if sentence[1:].find('“') >= 1:
            frag_and_ant_dict = fragmenter(sentence)
            fragments, antecedant = frag_and_ant_dict['lister'], frag_and_ant_dict['speaker']
            if fragments[-1]['ends in quotes']:
                ends_in_quotes = True
            else: 
                ends_in_quotes = False
            if sentence.endswith('”'):
                ends_in_quotes = False
            dicto['sentence'], dicto['ends in quotes'], dicto['fragments'] = sentence, ends_in_quotes, fragments 
        elif sentence.startswith('“'):
            ends_in_quotes = True
            if sentence.endswith('”'):
                ends_in_quotes = False
            dicto['sentence'], dicto['ends in quotes'], dicto['speaker'] = sentence, ends_in_quotes, 'narrator'
        else:
            dicto['sentence'], dicto['ends in quotes'] = sentence, False


    if sentence.startswith('“'):
        if 0 < sentence.find('”') + 1 < len(sentence):
            fragments, antecedant = fragmenter(sentence)['lister'], fragmenter(sentence)['speaker']
            if fragments[-1]['ends in quotes']:
                ends_in_quotes = True
            else: 
                ends_in_quotes = False
            dicto['sentence'], dicto['ends in quotes'], dicto['fragments'] = sentence, ends_in_quotes, fragments 
        else:
            if sentence.endswith('”'):
                ends_in_quotes = False
            else: 
                ends_in_quotes = True
            dicto['sentence'], dicto['ends in quotes'] = sentence, ends_in_quotes
    else:
        if sentence.find('“') >= 1:
            fragments, antecedant = fragmenter(sentence)['lister'], fragmenter(sentence)['speaker']
            if fragments[-1]['ends in quotes']:
                ends_in_quotes = True
            else: 
                ends_in_quotes = False
            dicto['sentence'], dicto['ends in quotes'], dicto['fragments'] = sentence, ends_in_quotes, fragments 
        else:
            if not ends_in_quotes:
                dicto['sentence'], dicto['ends in quotes'], dicto['speaker'] = sentence, ends_in_quotes, 'narrator'
            else:
                dicto['sentence'], dicto['ends in quotes'] = sentence, ends_in_quotes



    sentence = sentence + '\n'
    with open('texts\\pnp chapters\\one.txt', 'a') as file:
        if sentence != '\n':
            file.write(str(sentence))

for count, chapter in enumerate(chapter_list):
    sentence_list = sentencer(category = 'text', input = chapter)

    for sentence in sentence_list:
        with open(f'texts\\pnp chapters\\{count}.txt', 'a') as file:
            file.write(str(sentence))
    print(f'did {count}') 


def quote_parser(sentence):
    dicto = {}
    if (0 < sentence.find('”') + 1 < len(sentence)) or (sentence[1:].find('“') >= 1):
        frag_and_ant_dict = fragmenter(sentence)
        fragments, antecedant = frag_and_ant_dict['lister'], frag_and_ant_dict['speaker']
        if fragments[-1]['ends in quotes']:
            ends_in_quotes = True
        else: 
            ends_in_quotes = False
        if sentence.endswith('”'):
            ends_in_quotes = False
        dicto['sentence'], dicto['ends in quotes'], dicto['fragments'] = sentence, ends_in_quotes, fragments 
        dicto['color'] = mixed
    elif ends_in_quotes:

        if preceding_type != 'quote':
            color = initial_quote_color
        else:
            color = flip(color)

        if sentence.endswith('”'):
            preceding_type = 'quote'
            ends_in_quotes = False

            if sentence.endswith('“'): # this would never happen but i included it for symmetry
                ends_in_quotes = True  # this would never happen but i included it for symmetry
            dicto['sentence'], dicto['ends in quotes'], dicto['speaker'] = sentence, ends_in_quotes, 'narrator'
        else:
            dicto['sentence'], dicto['ends in quotes'] = sentence, True
    else: #elif not ends_in_quotes

        if sentence.startswith('“'):
            if preceding_type != 'quote':
                color = initial_quote_color
            else:
                color = flip(color)
            ends_in_quotes = True

            if sentence.endswith('”'):
                preceding_type = 'quote'
                ends_in_quotes = False

            dicto['sentence'], dicto['ends in quotes'], dicto['speaker'] = sentence, ends_in_quotes, 'narrator'
            dicto['color'] = color
        else:
            dicto['sentence'], dicto['ends in quotes'], dicto['speaker'] = sentence, ends_in_quotes, 'narrator'
            if preceding_type != 'paragraph': 
                color = initial_paragraph_color
                preceding_type = 'paragraph'
            dicto['color'] = color
            if sentence.endswith('\r\n\r\n'):
                color = flip(color)

    return dicto
    
 version 24 Jan 2024

    if (0 < sentence.find('”') + 1 < len(sentence)) or (sentence[1:].find('“') >= 1):
        frag_and_ant_dict = fragmenter(sentence)
        fragments = frag_and_ant_dict['lister']

        if fragments[-1]['ends in quotes']:
            ends_in_quotes = True
        else: 
            ends_in_quotes = False
        if sentence.endswith('”'):
            ends_in_quotes = False

        dicto['sentence'], dicto['ends in quotes'], dicto['fragments'] = sentence, ends_in_quotes, fragments 
        dicto['color'] = mixed

    if ends_in_quotes: 

        if sentence.endswith('”'):
            preceding_type = 'quote'
            ends_in_quotes = False

        dicto['sentence'], dicto['ends in quotes'], dicto['speaker'] = sentence, ends_in_quotes, 'narrator'
        dicto['color'] = color

    else: #elif not ends_in_quotes

        if sentence.startswith('“'):
            if preceding_type != 'quote':
                #preceding_type = 'quote'
                color = initial_quote_color
            else:
                color = flip(color)
            if sentence.endswith('”'):
                preceding_type = 'quote'
                ends_in_quotes = False
            else:
                ends_in_quotes = True
        else:
            if preceding_type != 'paragraph': 
                color = initial_paragraph_color
            else:
                color = flip(color)
            if sentence.endswith('\r\n\r\n'):
                preceding_type = 'paragraph'

        dicto['sentence'], dicto['ends in quotes'], dicto['speaker'] = sentence, ends_in_quotes, 'narrator'
        dicto['color'] = color

    return dicto    
    
    2.0 

def quote_parser(sentence):

    dicto = {}
    global ends_in_quotes, preceding_type, color

    if ends_in_quotes: 

        if sentence.endswith('”'):
            preceding_type_bool_true_if_quotes_false_if_paragraph = True
            ends_in_quotes = False

    else: #elif not ends_in_quotes

        if sentence.startswith('“'):
            if preceding_type_bool_true_if_quotes_false_if_paragraph:
                color = flip(color)
            else:
                preceding_type_bool_true_if_quotes_false_if_paragraph = True
                color = initial_quote_color
            if sentence.endswith('”'):
                ends_in_quotes = False
            else:
                ends_in_quotes = True
        else:
            if not preceding_type_bool_true_if_quotes_false_if_paragraph: 
                color = flip(color)
            else:
                color = initial_paragraph_color
            if sentence.endswith('\r\n\r\n'):
                preceding_type_bool_true_if_quotes_false_if_paragraph = False
                ends_in_quotes = False

    #dicto['sentence'], dicto['ends in quotes'], dicto['speaker'] = sentence, ends_in_quotes, 'narrator'
    dicto['color'] = color

    return dicto


        if not sentence.startswith('“'):
        if not preceding_type_bool_true_if_quotes_false_if_paragraph: 
            color = initial_paragraph_color
        else:
            color = flip(color)
        if sentence.endswith('\n'):
            preceding_type_bool_true_if_quotes_false_if_paragraph = False
            color = flip(color)
    else:
        if preceding_type_bool_true_if_quotes_false_if_paragraph:
            color = initial_quote_color
        else:
            color = initial_quote_color
        if sentence.endswith('\n'):
            preceding_type_bool_true_if_quotes_false_if_paragraph = True
            color = flip(color)

"""

'''
24 Jan 2024 3.0 

    if sentence.startswith('“') or preceder == 'quotes':
        if preceder == 'paragraph': 
            preceder = 'quotes'
            color = initial_quote_color
        if sentence.endswith('”') or sentence.endswith('\n'):
            preceder = 'quotes'
            color = alternate_quote_color
    elif preceder == 'paragraph':
        if preceder == 'quotes': 
            preceder = 'paragraph'
            color = initial_paragraph_color
        if sentence.endswith('\n'):
            preceder = 'paragraph'
            color = alternate_paragraph_color


'''






text = """
this is a paragraph. 
this is another paragraph. 
"this is a quote."
"this is another quote."
this is a paragraph.
this is a quote.
this is a paragraph. 
this is a quote. 
"""

initial_quote_color = "DFBB4C"        # light yellow
alternate_quote_color = "FFE699"      # darker yellow
initial_paragraph_color = "6691BA"    # light blue
alternate_paragraph_color = "9BC2E6"  # darker blue

paragraph_color = initial_paragraph_color
quote_color = initial_quote_color

result = ""

for line in text.split('\n'):
    if line.startswith('"'):
        return_color = quote_color
        quote_color = alternate_quote_color if quote_color == initial_quote_color else initial_quote_color
    else:
        return_color = paragraph_color
        paragraph_color = alternate_paragraph_color if paragraph_color == initial_paragraph_color else initial_paragraph_color

    print(return_color)
