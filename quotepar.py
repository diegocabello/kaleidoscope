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

lines = ['this is a paragraph.', '“this is a quote.”', 'this is a paragraph.', 'this is the same paragraph continued.', '“this is a quote.', 'this is the same quote continued.”', 'this is a paragraph.', 'this is a new paragraph.', '“this is a quote.”', '“this is a new quote.”']

for line in lines:
    if line.startswith('“'):
        return_color = quote_color
        quote_color = alternate_quote_color if quote_color == initial_quote_color else initial_quote_color
    else:
        return_color = paragraph_color
        paragraph_color = alternate_paragraph_color if paragraph_color == initial_paragraph_color else initial_paragraph_color

    print(line)
    print(return_color)
    print('\n')