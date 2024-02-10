import re

from text_parser import sentencer, entitier

initial_quote_color = "DFBB4C"        # dark yellow
initial_quote_to_sentence_color = "A99A6C" # brown
alternate_quote_color = "FFE699"      # light yellow
alternate_quote_to_sentence_color = "FFF3CC" # lighter yellow
initial_paragraph_color = "6691BA"    # light blue
alternate_paragraph_color = "9BC2E6"  # darker blue
initial_bit_color = "7A808C"          # light grey
alternate_bit_color = "1E1F21"        # dark grey 
ignore_color = "2A4225"               # green-grey  
pink = "FF00FF"
green = "00FF00"

paragraph_ender_pattern = '[).?!]\r\n\r\n$'         # choose between `)`, `.`, `?`, `!`; optionally (\r\n\r\n), `$` adds to the end | need to add `—` as an 'or' option 
ques_exclam_close_qt_pattern = '[?!]”\s?$'              # either ? or ! [?!], optional space \s?, anchors pattern to end of string $


def sentence_parser(sentence_list, input_color_dicto):

    output_list = []
    fflag = False

    for sentence_counter, sentence in enumerate(sentence_list): 
        to_put_in_dicto = {}

        if sentence_counter == 0:
            if '“' in sentence:
                color = input_color_dicto['color']
                fflag = False
            else:
                color = input_color_dicto['highlite']    
                fflag = True

        if fflag:
            color = input_color_dicto['highlite']
            fflag = False

        if '“' in sentence:
            color = input_color_dicto['color']
        if '”' in sentence:
            fflag = True

        to_put_in_dicto['sentence'] = sentence
        to_put_in_dicto['color'] = color 

        print(to_put_in_dicto)
        output_list.append(to_put_in_dicto)

    return output_list

def flatten_list(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        elif isinstance(item, str):
            result.append(item.strip() + ' ')
    return result

def split_and_tack_on_properly(inputer = '', splitter = ''):
    splitted = inputer.split(splitter)
    return [sub_sentence + splitter if sub_sentence != splitted[-1] else sub_sentence for sub_sentence in splitted if sub_sentence] 

def sentence_splitter(section):
    sentence_list = [str(sentence) for sentence in sentencer(inputer=section)]                          #    ====SENTENCE====
    flatten_flag = False

    for sentence_counter, sentence in enumerate(sentence_list):      # spacy doesnt correctly parse open or closed double quotes sometimes

        clone_minus_one = sentence_list[sentence_counter - 1]
        clone_itself = sentence_list[sentence_counter]

        if clone_itself.startswith('”'):          # replaces floating closed quotes  
            clone_minus_one = clone_minus_one +  '”'
            clone_itself = clone_itself.strip('”')

        if re.search(ques_exclam_close_qt_pattern, clone_itself): # makes sure sentences with partial quotes that end in '!”' or '?”' stay intact  # it could split a partial quote that ends in '!”' or '?”' as '!' and '”' or '?' and '”' so needs multiple 'for' loops
            if not sentence_list[sentence_counter + 1].startswith("“") and sentence_list[sentence_counter + 1][0].islower(): # this isnt completely failproof in case the sentence goes “what on earth?” Alice screamed, or dialogue tag after
                clone_itself += ' ' + sentence_list.pop(sentence_counter + 1)                        
                print(f'\tconcatenated sentence')
            else:
                print(f'\tpotential dialouge tag after which may need manual concatenation')
                print('\t' + clone_itself + '\n\t' + sentence_list[sentence_counter + 1])
    
        if len(sentence) > 150 and sentence.find(';') not in [0, -1, (len(sentence) - 1)]:  # this splits by semicolon if it is longer then a certain length 
            flatten_flag = True
            clone_itself = split_and_tack_on_properly(inputer = sentence, splitter = ';')

        sentence_list[sentence_counter - 1] = clone_minus_one

        if isinstance(clone_itself, str):
            sentence_list[sentence_counter] = clone_itself.strip()
        else:
            sentence_list[sentence_counter] = clone_itself 

    if flatten_flag:           # the two 'for' loops could be concatenated here, just not sure how 
        sentence_list = flatten_list(sentence_list)

    return sentence_list 

sentence = '“there once was a time where that happened. poland packs money from the german hand and germany feeds poland to a certain extent and\
 they closed their route to germany. why? i dont understand,” said putin. Mr. Carlson says otherwise. “look guys we give you money and weapons open\
 up the price we are competitve economy down to zero,” continuted putin. He had a serious look on his face.'

if __name__ == '__main__':

    color_dict_to_pass = {'color': 'yellow', 'highlite': 'light'}
    sentence_parser(sentence_splitter(sentence), color_dict_to_pass)
    #print(*(x for x in sentence_parser(sentence_splitter(sentence), color_dict_to_pass)), sep='\n')