from colorama import Fore, Back, Style
from colorama import init as color_init

color_init()

black = Fore.BLACK
red = Fore.RED
green = Fore.GREEN
yellow = Fore.YELLOW
blue = Fore.BLUE
magenta = Fore.MAGENTA
cyan = Fore.CYAN
white = Fore.WHITE

def colorprint(color=None, text=None):
    text = str(text)
    print(color + text + Style.RESET_ALL)