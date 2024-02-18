def split_on(long='', short=''):
    indexer = long.find(short) + len(short)
    return long[(indexer + 1):] if long[indexer] == ' ' else long[indexer:]

def split_on(long='', short=None): # multiple usage cases 
#
    def the_after(long=long, short=''):
        indexer = long.find(short) + len(short)
        if long[indexer] == ' ':
            indexer += 1
        return [long[:indexer], long[indexer:]]
#
    if isinstance(short, str):
        return the_after(long, short)
#
    elif isinstance(short, list):
        lister = ['', '']
        for item in short:
            if not isinstance(item, str):
                raise TypeError('2. split input needs to be a string')
            if lister[1] == '':    # this might not be the fastest way to do it 
                lister[0], lister[1] = the_after(long, item)[0], the_after(long, item)[1]
            else:
                lister[0], lister[1] = lister[0] + the_after(lister[1], item)[0], the_after(lister[1], item)[1]
        return lister
#        
    else:
        raise TypeError('1. function input needs to be either a string or list of strings')
    
if __name__ == '__main__':
    print(split_on('CHAPTER one this is the story of', ['CHAPTER', ' ']))