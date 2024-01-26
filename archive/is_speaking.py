import spacy

class quot:
    def __init__(self, content, speaker='', in_quotes=True):
        super().__init__()
        self.content = content
        self.speaker = speaker
        self.in_quotes = True
#
    def __str__(self):
        return self.content
#
    def __repr__(self):
        return f"quot('{self.content}', '{self.speaker}')"


# Usage
my_string = quot("This is a string", isquote=True)
print(my_string)  # prints the string
print(my_string.isquote)  # prints True


nlp = spacy.load("en_core_web_sm")

"""
what i am trying to do is take each sentence, decide if it needs to be split or not
if it is split
then i need to determine if it is in quotes or not 

these two do the same thing just slightly differently
"""

sentence = '"i cant believe he would do that," remarked Billiam, "if he knew it would drive him off a cliff."'

#works
def det(inputer):
    stringer = str(inputer)
    list_of_substrings = []
    bool_flag = True if stringer.startswith('"') else False
    while True:
        start = stringer.find('"')
        end = stringer[(start + 1):].find('"')
        if end == -1:
            return list_of_substrings
        quoter = stringer[(start+1):(end+1)].strip(', ')
        list_of_substrings.append({'fragment': quoter, 'quotes or not': bool_flag})
        stringer = stringer[(end+1):]
        bool_flag = not bool_flag

#good 
def det2(inputer):
    stringer = str(inputer)
    lister = list(x.strip(', ') for x in stringer.split('"') if x != '')
    lister2 = []
    bool_flag = True if stringer.startswith('"') else False
    for x in lister:
        #lister2.append((x, bool_flag))
        lister2.append({'fragment': x, 'quotes or not': bool_flag})
        bool_flag = not bool_flag
    return lister2

#better
def det2(inputer):
    stringer = str(inputer)
    lister = list(x.strip(', ') for x in stringer.split('"') if x)
    bool_flag = True if stringer.startswith('"') else False
    for index, value in enumerate(lister):
        lister[index] = {'fragment': value, 'quotes or not': bool_flag}
        bool_flag = not bool_flag
    return lister

#best
def det2(inputer):
    return [{'fragment': frag.strip(', '), 'quotes or not': i % 2 == (1 if str(sentence).startswith('"') else 0)} for i, frag in enumerate(str(inputer).split('"')) if frag]

fff = det2(sentence)

for x in fff:
    if x['quotes or not'] == False:
        doc = nlp(x['fragment'])
        charachter = list(doc.ents)[0]

for x in fff:
    if x['quotes or not'] ==  False:
        x['speaker'] = 'Narrator'
    else:
        x['speaker'] = charachter





sentences = []

quotes_list = []
for x in range(len(sentences)): 
    if sentences[x].startswith('"'): 
        for zz in sentences[x:]:
            if zz.endswith('"'):
                y = sentences.index(y)
    quote = quote.join(z for z in sentences[x:y])
    quotes_list.append(quote)