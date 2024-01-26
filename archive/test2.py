par_list, sent_list = []

with open('text.txt', 'r') as text:

    for x in text:
        par_list.append(x)
        if x != '\n':
            sent_list.append(x.split('. '))
        

