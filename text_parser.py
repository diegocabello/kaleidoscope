import spacy
from spacy.matcher import Matcher
from spacy.tokens import Span
from bigstringer import bigstringer
print('imported...')


# Load the SpaCy model
nlp = spacy.load("en_core_web_sm")
print('loaded model...')

"""
matcher = Matcher(nlp.vocab)
patterns = [
    [{"LOWER": "mrs"}, {"IS_PUNCT": True, "OP": "?"}, {"LOWER": "bennet"}], 
    [{"LOWER": "mr"}, {"IS_PUNCT": True, "OP": "?"}, {"LOWER": "bennet"}],
    [{"LOWER": "mr"}, {"IS_PUNCT": True, "OP": "?"}, {"LOWER": "bingley"}],
    [{"LOWER": "mr"}, {"IS_PUNCT": True, "OP": "?"}, {"LOWER": "collins"}],
    [{"LOWER": "mr"}, {"IS_PUNCT": True, "OP": "?"}, {"LOWER": "darcy"}],
]

for pattern in patterns:
    print(pattern)
    print(type(pattern))
    matcher.add("CustomEntity", [pattern])
"""

def spacyer(func):

    def wrapper(**kwargs):

        text = kwargs['inputer']

        """
        matches = matcher(nlp(text))

        for match_id, start, end in matches:
            entity = Span(nlp(text), start, end, label="PERSON")  # You can specify your own label
            nlp.get_pipe("ner").add_label(entity.label_)
            nlp.get_pipe("ner").update([entity])
        """

        return func(inputer=text)
    
    return wrapper


@spacyer
def sentencer(inputer=''):
    doc = nlp(inputer)
    return list(doc.sents)

@spacyer
def entitier(inputer=''):
    doc = nlp(inputer)
    return list(doc.ents)





#entities = list({str(x).lower() for sentence in sentences for x in sentence.ents if str(x).lower() not in entities})
#entities = {x for sentence in sentences for x in sentence.ents if x not in entities}


def poke(lister):
    print(lister)
    print("hit 'y' to poke, hit 'enter' to pass ")
    lister = [x for x in lister if input(f'{x}: ') != 'y']



if __name__ == '__main__':
    entities = entitier('alice through the looking glass')