from colorama import Fore, Back, Style
from colorama import init as color_init

color_init()

def colorprint(color=str, text=None):
    text = str(text)
    colors = {'black': Fore.BLACK,
                'red': Fore.RED, 
                'green': Fore.GREEN, 
                'yellow': Fore.YELLOW, 
                'green': Fore.GREEN, 
                'blue': Fore.BLUE,
                'magenta': Fore.MAGENTA, 
                'cyan': Fore.CYAN, 
                'white': Fore.WHITE}

    if color in colors:
        color = colors[color]
        print(color + text + Style.RESET_ALL)
    else:
        print(text)