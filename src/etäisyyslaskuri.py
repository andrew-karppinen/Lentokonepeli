import mysql.connector
import random
from geopy.distance import geodesic
import os


#Funktio etäisyyden laskemiseen geopy-kirjaston avulla
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
    palauttaa etäisyyden kilometreinä ja kohdelentokentän sijainnin

    '''
    try:
        kursori = yhteys.cursor()

        # Hae kohdelentokentän tiedot (leveys- ja pituusaste) lentokentän nimen perusteella
        komento = "SELECT latitude_deg, longitude_deg FROM airport WHERE name = %s"
        kursori.execute(komento, (kohdelentokentta_nimi,)) #Parametrisoitu kysely sql injektien estämiseksi

        tulos = kursori.fetchone()
        kursori.close()


        if not tulos:
            print(f"Lentokenttää nimellä {kohdelentokentta_nimi} ei löytynyt.")
            return False,[]

        try:
            lentokentan_sijainti = (tulos[0], tulos[1])
            etaisyys = laske_etaisyys(sijanti, lentokentan_sijainti)
        except:
            print("Virhe laskiessa etäisyyttä")
            return False,[]


        #palautetaan etäisyys
        return  etaisyys, lentokentan_sijainti

    except mysql.connector.Error as err:
        print(err)
        return False,[]



if __name__ == "__main__":
    # Kysytään käyttäjältä lentokentän nimi ja arvottu maan koodi
    kohdelentokentta_nimi = "Cleveland Municipal Airport "

    kayttajatunnus = os.getenv('sqlkayttaja')
    salasana = os.getenv('sqlkayttaja_salasana')

    # luodaan sql yhteys
    yhteys = mysql.connector.connect(
        host="localhost",
        port=3306,
        database='flight_game',
        user=kayttajatunnus,
        password=salasana,
        connection_timeout=5,
        autocommit=True)


    sijainti = (30.3565, -95.008003)
    etaisyys = hae_etaisyys(yhteys, kohdelentokentta_nimi, sijainti)

    print(etaisyys)

    yhteys.close()