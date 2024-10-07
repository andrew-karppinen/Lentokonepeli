import os

import platform


def TallennaAsetukset(server_ip, kayttaja, salasana):
    '''
    Tallentaa asetukset tiedostoon

    '''

    path = GetHomeConfigDirectory() + "/flight_game"

    if not os.path.exists(path):  # hakemistoa ei ole
        os.makedirs(path)  # luodaan hakemisto

    with open(path + "/asetukset.txt", "w") as f:
        f.write(f"{server_ip}\n{kayttaja}\n{salasana}")


def LueAsetukset():
    '''
    Lukee asetukset tiedostosta

    data = server_ip,kayttaja,salasana
    '''

    path = GetHomeConfigDirectory() + "/flight_game/asetukset.txt"

    if not os.path.exists(path):  # tiedostoa ei ole
        return False

    with open(path, "r") as f:
        data = f.read().split("\n")

    return data


def GetHomeConfigDirectory():
    '''
    get this path in linux:
    home/.config

    get this path in windows:
    appdata/Roaming

    '''

    system = platform.system()  # get operating system

    if system == "Linux":  # linux
        path = os.path.expanduser('~') + "/.config"

        return path

    elif system == "Windows":  # windows
        path = os.getenv('APPDATA')
        return path


if __name__ == "__main__":
    print(GetHomeConfigDirectory())
