#parse the text
#↓ makes a bigstring from the text file by decoding and recoding each letter and adding it to a string
def bigstringer(file):
    cryptable = open(f'{file}', 'rb').read().decode('utf-8', errors='ignore')
    numchar = 0
    text = ""
    for y in cryptable:
        char = y.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
        text = text + char
        if ((numchar := numchar + 1) % 100000 == 0):
            print('%s charachters decoded' %(numchar))
    return text







    #paragraph_list = text.split("\r\n\r\n") # list of paragraphs
    #sentence_list = text.split('. ')      # list of sentences
    #sentence_list = [element for element in sentence_list if element != '\n']
    #return_dict = {"text": text, "paragraphs": paragraph_list, "sentences": sentence_list}
    #return return_dict
"""
def bigstringer(file):
    cryptable = open(f'{file}', 'rb').read().decode('utf-8', errors='ignore')
    numchar = 0
    text = ""
    for y in cryptable:
        utfer1 = y.encode('utf-8', errors='ignore')
        utfer2 = utfer1.decode('utf-8', errors='ignore')
        text = text + utfer2
        numchar = numchar + 1
        if (numchar % 5000 == 0):
            print('%s charachters decoded' %(numchar))
    return text
"""