#↓ makes a bigstring from the text file by decoding and recoding each letter and adding it to a string
def bigstringer(file):
    cryptable = open(f'{file}', 'rb').read().decode('utf-8', errors='ignore')
    numchar = 0
    text = ""
    for y in cryptable:
        text = text + y.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
        if ((numchar := numchar + 1) % 100000 == 0):
            print(f'{str(numchar)} characters decoded')
    return text


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