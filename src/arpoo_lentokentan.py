#Funktio arpoo lentokentän nimen, maan nimen sille annetun mantereen mukaan.
import mysql.connector


def arpominen(yhteys,maanosa:str="*"):
    
    # Funktio arpoo lentokentän nimen, maan nimen sille annetun mantereen mukaan.
    # Hakutulosta voi rajata maanoasan mukaan tai hakea kaikista maanosista
    
    if maanosa=="*": #haetaan kaikista maanosista
        randomaus = f"SELECT airport.name, country.name, country.continent FROM airport LEFT JOIN country on airport.iso_country = country.iso_country where airport.type = 'large_airport' ORDER BY RAND() LIMIT 1;"
    else:
        randomaus = f"SELECT airport.name, country.name, country.continent FROM airport LEFT JOIN country on airport.iso_country = country.iso_country where country.continent = '{maanosa}' AND airport.type = 'large_airport' ORDER BY RAND() LIMIT 1;"


    kursori = yhteys.cursor()
    kursori.execute(randomaus)
    tulos = kursori.fetchone()
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
        print(arpominen(yhteys,"EU"))
