#Funktio arpoo lentokentän nimen, maan nimen sille annetun mantereen mukaan.
import mysql.connector
import os

def arpominen(yhteys,maanosa:str="*",maa:str="*"):
    '''
    Funktio arpoo lentokentän nimen, maan nimen sille annetun mantereen mukaan.
    Hakutulosta voi rajata maanoasan mukaan tai hakea kaikista maanosista
    '''


    kursori = yhteys.cursor()

    #Parametrisoitu kysely sql injektien estämiseksi
    if maa == "*":  # Ei rajattu maan mukaan
        if maanosa == "*":  # Haetaan kaikista maanosista
            randomaus = """
                SELECT airport.name, country.name, country.continent, airport.latitude_deg, airport.longitude_deg 
                FROM airport 
                LEFT JOIN country ON airport.iso_country = country.iso_country 
                WHERE airport.type = 'large_airport' 
                ORDER BY RAND() LIMIT 1;
            """
            kursori.execute(randomaus)
        else:
            randomaus = """
                SELECT airport.name, country.name, country.continent, airport.latitude_deg, airport.longitude_deg 
                FROM airport 
                LEFT JOIN country ON airport.iso_country = country.iso_country 
                WHERE country.continent = %s AND airport.type = 'large_airport' 
                ORDER BY RAND() LIMIT 1;
            """
            kursori.execute(randomaus, (maanosa,))
    else:  # Haetaan tietystä maasta
        randomaus = """
            SELECT airport.name, country.name, country.continent, airport.latitude_deg, airport.longitude_deg 
            FROM airport 
            LEFT JOIN country ON airport.iso_country = country.iso_country 
            WHERE country.name = %s 
            ORDER BY RAND() LIMIT 1;
        """
        kursori.execute(randomaus, (maa,))

    tulos = kursori.fetchone()
    kursori.close()

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
    except mysql.connector.Error as err: #virhe yhteyden muodostamisessa
        print(err)


    else: #yhteys muodostettu onnistuneesti
        print(arpominen(yhteys,"","US"))