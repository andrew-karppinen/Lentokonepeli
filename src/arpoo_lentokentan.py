#Funktio arpoo lentokentän nimen, maan nimen sille annetun mantereen mukaan.
import mysql.connector


def arpominen(yhteys,maanosa:str="*",maa:str="*"):
    '''
    Funktio arpoo lentokentän nimen, maan nimen sille annetun mantereen mukaan.
    Hakutulosta voi rajata maanoasan mukaan tai hakea kaikista maanosista
    '''


    if maa == "*": #ei rajattu maan mukaan
        if maanosa=="*": #haetaan kaikista maanosista
            randomaus = f"SELECT airport.name, country.name, country.continent, airport.latitude_deg, airport.longitude_deg FROM airport LEFT JOIN country on airport.iso_country = country.iso_country where airport.type = 'large_airport' ORDER BY RAND() LIMIT 1;"
        else:
            randomaus = f"SELECT airport.name, country.name, country.continent, airport.latitude_deg, airport.longitude_deg FROM airport LEFT JOIN country on airport.iso_country = country.iso_country where country.continent = '{maanosa}' AND airport.type = 'large_airport' ORDER BY RAND() LIMIT 1;"

    else: #haetaan tietystä maasta
        randomaus =f"SELECT airport.name, country.name, country.continent, airport.latitude_deg, airport.longitude_deg FROM airport LEFT JOIN country on airport.iso_country = country.iso_country where country.iso_country = '{maa}' AND airport.type = 'large_airport' ORDER BY RAND() LIMIT 1;"


    kursori = yhteys.cursor()
    kursori.execute(randomaus)
    tulos = kursori.fetchone()

    if tulos == None:
        return None
    else:
        tulos = {
            "airport": tulos[0],
            "country": tulos[1],
            "continent": tulos[2],
            "latitude_deg": tulos[3],
            "longitude_deg": tulos[4]
        }
        return tulos


if __name__ == '__main__': #testiohjelma

    try:
        yhteys = mysql.connector.connect(
                 host='127.0.0.1',
                 port= 3306,
                 database='flight_game',
                 user='sqlkayttaja',
                 password='salasana123',
                 autocommit=True
                 )
    except mysql.connector.Error as err: #virhe yhteyden muodostamisessa
        print(err)


    else: #yhteys muodostettu onnistuneesti
        print(arpominen(yhteys,"","US"))