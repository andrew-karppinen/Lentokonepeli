import mysql.connector
import random
from geopy.distance import geodesic

# Funktio etäisyyden laskemiseen geopy-kirjaston avulla
def laske_etaisyys(sijainti1: tuple, sijainti2: tuple) -> float:
    etaisyys = geodesic(sijainti1, sijainti2).kilometers
    return etaisyys

# Funktio, joka hakee satunnaisen lentokentän annetusta maasta ja laskee etäisyyden
def hae_etaisyys_lentokentta(yhteys: object, kohdelentokentta_nimi: str, arvattu_maa: str):
    try:
        kursori = yhteys.cursor()

        # Hae kohdelentokentän tiedot (leveys- ja pituusaste) lentokentän nimen perusteella
        kohde_query = """SELECT latitude_deg, longitude_deg, iso_country FROM airport WHERE name = %s"""
        kursori.execute(kohde_query, (kohdelentokentta_nimi,))
        kohde_tulos = kursori.fetchone()

        if not kohde_tulos:
            print(f"Lentokenttää nimellä {kohdelentokentta_nimi} ei löytynyt.")
            return False

        kohde_lat, kohde_lon, oikea_maa = kohde_tulos  # Kohdelentokentän koordinaatit ja oikea maan koodi

        # Hae kaikki lentokentät arvatussa maassa
        maa_query = f'SELECT airport.latitude_deg, airport.longitude_deg FROM airport,country where airport.iso_country = country.iso_country and country.name = "{arvattu_maa}"'
        kursori.execute(maa_query)
        arvattu_maa_lentokentat = kursori.fetchall()
        if not arvattu_maa_lentokentat:
            return False

        # Valitaan satunnainen lentokenttä kyseisestä maasta
        satunnainen_lentokentta = random.choice(arvattu_maa_lentokentat)
        kentan_lat, kentan_lon = satunnainen_lentokentta

        # Lasketaan etäisyys kohdelentokentän ja satunnaisesti valitun lentokentän välillä
        etaisyys = laske_etaisyys((kohde_lat, kohde_lon), (kentan_lat, kentan_lon))

        #palautetaan etäisyys
        return  etaisyys

    except mysql.connector.Error as err:
        print(f"Tietokantavirhe: {err}")
        return False

    finally:
        kursori.close()

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
    kohdelentokentta_nimi = "Helsinki Vantaa Airport"
    arvottu_maa = input("Anna arvotun maan koodi (esim. Finland): ")

    yhteys = liity_tietokantaan()

    oikea_maa, etaisyys = hae_etaisyys_lentokentta(yhteys,kohdelentokentta_nimi, arvottu_maa)

    if oikea_maa:
        if arvottu_maa == oikea_maa:
            print("Onnittelut! Arvauksesi on oikein.")
        else:
            print(f"Väärin. Oikea maan koodi on {oikea_maa}.")
            print(f"Etäisyys arvattujen maan lentokentistä kohdelentokenttään: {etaisyys:.2f} km")
    else:
        print("Lentokenttää tai maata ei löytynyt.")

    yhteys.close()
