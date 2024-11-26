import mysql.connector
import random
from geopy.distance import geodesic



# Funktio etäisyyden laskemiseen geopy-kirjaston avulla
def laske_etaisyys(sijainti1: tuple, sijainti2: tuple) -> float:
    '''
    sijainti = latitude_deg, longitude_deg
    palauttaa etäisyyden kilometreinä
    '''

    etaisyys = geodesic(sijainti1, sijainti2).kilometers
    return etaisyys

def hae_etaisyys(yhteys: object, kohdelentokentta_nimi: str, sijanti: tuple):
    '''
    Funktio, joka laskee annetun lentokentän ja annetun sijainnin välisen etäisyyden

    sijainti = latitude_deg, longitude_deg
    palauttaa etäisyyden kilometreinä

    '''
    try:
        kursori = yhteys.cursor()

        # Hae kohdelentokentän tiedot (leveys- ja pituusaste) lentokentän nimen perusteella
        komento = f"""SELECT latitude_deg, longitude_deg FROM airport WHERE name = '{kohdelentokentta_nimi}';"""
        print(komento)
        kursori.execute(komento)
        tulos = kursori.fetchone()



        if not tulos:
            print(f"Lentokenttää nimellä {kohdelentokentta_nimi} ei löytynyt.")
            return False

        try:
            lentokentan_sijainti = (tulos[0], tulos[1])
            etaisyys = laske_etaisyys(sijanti, lentokentan_sijainti)
        except:
            print("Virhe laskiessa etäisyyttä")
            return False


        #palautetaan etäisyys
        return  etaisyys

    except mysql.connector.Error as err:
        print(err)
        return False

# Yhteys MySQL-tietokantaan
def liity_tietokantaan():
    return mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        database='flight_game',
        user='sqlkayttaja',
        password='salasana123',
        autocommit=True
    )

if __name__ == "__main__":
    # Kysytään käyttäjältä lentokentän nimi ja arvottu maan koodi
    kohdelentokentta_nimi = "Cleveland Municipal Airport "

    yhteys = liity_tietokantaan()
    sijainti = (30.3565, -95.008003)
    etaisyys = hae_etaisyys(yhteys, kohdelentokentta_nimi, sijainti)

    print(etaisyys)

    yhteys.close()