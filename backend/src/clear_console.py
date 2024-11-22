import os

import platform


def clear_console():
    '''
    Tyhjentää konsolin
    tunnistaa käyttöjärjestelmän (linux, windows)
    '''

    system = platform.system()  # get operating system

    if system == "Linux":  # linux
        os.system('clear')

    elif system == "Windows":  # windows
        os.system('cls')



if __name__ == "__main__":
    print("uli uli")
    tyhjenna_konsoli()

    print("nojaa")