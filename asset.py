import random
from colorama import init
from colorama import Fore, Back, Style
init()
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m" 

BULLET =Fore.BLUE +"|"+Style.RESET_ALL
BULLETS = Fore.RED + "|" + Style.RESET_ALL
print(BULLET)
ENEMY_BULLET = Fore.RED + "⬤"+ Style.RESET_ALL
MAX_HEALTH = 5
MAX_BULLET_POWER = 5
HEART_POWERUP = "❤️"
BULLET_POWERUP = "⚡"

# Adjustable formation dimensions
FORMATION_HEIGHT = 7  # Default number of enemy rows(7 is best for experience)
FORMATION_WIDTH = 20 # Default number of enemy columns(20 is best for experience)
E1= [
    "/|\\",
    "-O-",
    "\\|/"
]
# E1=Fore.RED + "/|\\" + Style.RESET_ALL


E2= [
    "\\|/",
    "-O-",
    "/|\\"
]
def enemys():
    enmy=[E1, E2]
    return random.choice(enmy)

# Global variable to store the selected spaceship
selected_spaceship = None
base_spaceships = {
        "a": [
            "  A  ",
            " /|\\ ",
            "/_|_\\"
        ],
       
        "b": [
            " \\-A-/  ",
            "  -|-  ",
            "X-=W=-X"
        ],
      
        "c": [
            " _A_ ",
            "[=V=]",
            " <O> "
        ],}
upgrade_spaceship = {
         "a1": [
            " |A|  ",
            " /|\\ ",
            "/_|_\\"
        ],
        "a2": [
            "|_A_|  ",
            " /|\\ ",
            "/_|_\\"
        ],
        "a3": [
            "|_|A|_|  ",
            "  /|\\ ",
            " /_|_\\"
        ],
        "a4": [
            " |_|_A_|_|  ",
            "    /|\\ ",
            "   /_|_\\"
        ],
          "b1": [
            " \\-A-/  ",
            "  -|-  ",
            "X-=W=-X"
        ],
        "b2": [
            " \\-A-/  ",
            "  =|=  ",
            "X-=W=-X"
        ],
        "b3": [
            " |\\-A-/|  ",
            "   =|=  ",
            "    |   ",
            " X-=W=-X"
        ],
        "b4": [
            "| _ A _ |  ",
            " |=|H|=|  ",
            "    H",
            " X-=W=-X",
        ],
        "c1": [
            " _A_ ",
            "[=V=]",
            " <O> "
        ],
        "c2": [
            " v_A_v ",
            " [=V=]",
            "   |  ",
            "  <O> "
        ],
        "c3": [
            "\\-_A_-/  ",
            "[==V==]",
            "   |  ",
            "  <O> "
        ],
        "c4": [
            "\\-\\_A_/-/  ",
            "[===V===]",
            "    H ",
            "   <O> "
        ]
    }

def return_spaceship():
    global selected_spaceship
    

    # If a spaceship has already been selected, return it
    if selected_spaceship is not None:
        return selected_spaceship

    # Randomly select a base spaceship (a, b, or c)
    base = random.choice(["a", "b", "c"])
    # base = random.choice(["b"])
    selected_spaceship = base_spaceships[base]

    # Return the selected spaceship
    return selected_spaceship

def return_boss_ship():
    a = [
        "              _____        ",
        "       __--===========--__    ",
        "     /        -----        \\  ",
        "    /  ==------| |------==  \\ ",
        "   /  | []     | |     [] |  \\ ",
        "  |   |  []    | |    []  |   |",
        " /|   |  []    | |    []  |   |\\",
        " ||   |________| |________|   ||",
        " ||   /        | |        \\   ||",
        " ||  |   ()    | |    ()   |  ||",
        " ||  |_________| |_________|  ||",
        " || /     ===  [ ]     ===   \\ ||",
        " ||/_________________________\\||",
        " /-_-_-_-_-_-_-_-_-_-_-_-_-_-_-\\",
        "|  [___]                 [___]  |",
        "|_______________V_______________|",
        " \\_/  \\_/               \\_/  \\_/"
    ]
    b = [
        "                                  ",
        "                /\\*********/\\  ",
        "               /  |       |  \\  ",
        "              /---|_____ _|---\\   ",
        "         /\\__/ [] |  | |  | [] \\__/\\ ",
        "        /  []|----|  | |  |----|[]  \\ ",
        "       /----|____|   | |   |____|----\\ ",
        "   /\\_/  [] |====|   | |   |====| []  \\_/\\",
        "  / []-----|______|  | |  |______|-----[] \\  ",
        "[==========|______|  | |  |______|==========]",
        "Y[=========|______|  | |  |______|=========]Y",
        "| \\  []------|====|  | |  |====|------[]  / |",
        "|  \\/__   [] |____|  | |  |____| []   __\\/  |",
        "       \\-----|====|  | |  |====|-----/ ",
        "        \\  []|____|  | |  |____|[]  / ",
        "         \\/__/ [] |  | |  | [] \\__\\/",
        "              \\---|__| |__|---/",
        "               \\  |       |  /",
        "                \\/****V****\\/",
        "                  ||     ||",
        "                  ||     ||"
    ]
    # BOSS_SHIP = [a, b]
    BOSS_SHIP = [b]
    return random.choice(BOSS_SHIP)


game_over = [
    " ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗ ██╗   ██╗███████╗██████╗  ",
    "██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██║   ██║██╔════╝██╔══██╗ ",
    "██║      ██║  ██║████║ ████║██║         ██║   ██║██║   ██║██║     ██║  ██║ ",
    "██║  ███╗███████║██╔████╔██║█████╗      ██║   ██║██║   ██║█████╗  ██████╔╝ ",
    "██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║██║   ██║██╔══╝  ██╔══██╗ ",
    "██║   ██║██║  ██║██║ ╚═╝ ██║██║         ██║   ██║ ██║ ██╔╝██║     ██║  ██║ ",    
    "╚██████╔╝██║  ██║██║     ██║███████╗    ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║ ",
    " ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝ "
]
