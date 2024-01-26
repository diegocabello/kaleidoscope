initial_quote_color = "DFBB4C"        # light yellow
alternate_quote_color = "FFE699"      # darker yellow
initial_paragraph_color = "6691BA"    # light blue
alternate_paragraph_color = "9BC2E6"  # darker blue

initial_quote_color = 'quote yellow initial'
alternate_quote_color = 'quote yellow alternate'
initial_paragraph_color = 'paragraph blue initial' 
alternate_paragraph_color = 'paragraph blue alternate'

paragraph_color = initial_paragraph_color
quote_color = initial_quote_color

type = 'paragraph'
lines = ['this is a paragraph.\n', '“this is a quote.”\n', 'this is a paragraph.\n', '“this is a quote.”\n', 'this is a paragraph.', 'this is the same paragraph continued.\n', '“this is a quote.', 'this is the same quote continued.”\n', 'this is a paragraph.\n', 'this is a new paragraph.\n', '“this is a quote.”\n', '“this is a new quote.”\n']

for line in lines:
    if line.startswith('“'):
        type = 'quote'
    if type == 'quote':
        return_color = quote_color
    elif type == 'paragraph':
        return_color = paragraph_color
    if line.endswith('”\n'):
        type = 'paragraph'
        quote_color = alternate_quote_color if quote_color == initial_quote_color else initial_quote_color
        paragraph_color = initial_paragraph_color
    elif line.endswith('.\n'):
        paragraph_color = alternate_paragraph_color if paragraph_color == initial_paragraph_color else initial_paragraph_color
        quote_color = initial_quote_color

    print(line.strip('\n'))
    print(return_color)
    print('\n')