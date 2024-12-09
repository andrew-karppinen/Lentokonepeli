import mysql.connector
import os

'''
Toiminnot:
Keskeneräisen pelin tietojen tallentamiseen ja hakemiseen (game_temp ja user_temp taulut)

Pelaajien pistetilastojen haku pelatuista peleistä (user_games ja user_information taulut)
'''





def onko_pelaaja_olemassa(yhteys, nimi)->bool:
    '''
    Tarkistaa onko tämän niminen pelaaja tietokannassa
    '''

    komento = f"SELECT name FROM user_information WHERE name = '{nimi}';"

    kursori = yhteys.cursor()  # luodaan kursori
    kursori.execute(komento)
    tulos = kursori.fetchone()
    kursori.close()

    if tulos is None:
        return False
    else:
        return True

def luo_pelaaja(yhteys, nimi):
    '''
    Luo uuden pelaajan tietokantaan
    '''

    if onko_pelaaja_olemassa(yhteys, nimi) == False: #käyttäjää  ei ole jo olemassa
        komento = f"INSERT INTO user_information (name) VALUES ('{nimi}');"

        kursori = yhteys.cursor()  # luodaan kursori
        kursori.execute(komento)
        kursori.close()


def tallenna_pelin_tiedot(yhteys):
    '''
    Tallentaa valmiin pelin tiedot tietokantaan tilastointia varten
    '''

    pelin_tiedot = hae_keskeneräisen_pelin_tiedot(yhteys)    #haetaan pelin tiedot


    maanosa = pelin_tiedot["continent"]
    maa = pelin_tiedot["country"]
    pelaajat = pelin_tiedot["players"]

    komento = f"""INSERT INTO game (continent, country) VALUES ('{maanosa}', '{maa}');""" #lisätään uusi rivi game tauluun
    kursori = yhteys.cursor()  # luodaan kursori
    kursori.execute(komento)  # suoritetaan komento

    print(pelaajat)

    #lisätään user_games tauluun uusi rivi
    for pelaaja in pelaajat:
        luo_pelaaja(yhteys, pelaaja['name']) #yritetään luoda pelaaja, jos pelaaja jo on tämä ei tee mitään

        komento = f"""INSERT INTO user_games (game_id,user_points,name)
        values ((SELECT MAX(game_id) FROM game),{pelaaja['score']},'{pelaaja['name']}');
        """ #lisätään pelaajalle uusi rivi user_games tauluun

        kursori.execute(komento)  # suoritetaan komento

    kursori.close()


def tallenna_keskeneraisen_pelin_tiedot(yhteys,tiedot:dict)->bool:
    '''
    Tallenta tauluhin user_temp tauluun pelin keskeneräiset tietoja

    tyhjentää  taulut kaikesta aikaisemmasta tiedot

    `{
    "players":[
        {
            "name":"Pelaaja1",
            "airport_counter":1,
            "score": 25
        },
        {
            "name":"Pelaaja2",
            "airport_counter":2,
            "score": 20
        }
    ]
    }`
    '''


    if hae_keskeneräisen_pelin_tiedot(yhteys) == {}:
        return False


    #tyhjennetään user_temp taulun tiedot
    komento = """DELETE FROM user_temp;"""
    kursori = yhteys.cursor()  # luodaan kursori
    kursori.execute(komento)  # suoritetaan komento
    tulos = kursori.fetchall()  # haetaan kaikki tulokset
    kursori.close()

    print("debug: ", tulos)

    for pelaaja in tiedot["players"]:
        luo_pelaaja(yhteys, pelaaja["name"]) #yritetään luoda pelaaja, jos pelaaja jo on tämä ei tee mitään


    kursori = yhteys.cursor()  # luodaan kursori

    for pelaaja in tiedot["players"]:

        komento = f"""INSERT INTO user_temp (name,airport_counter,user_points) VALUES ('{pelaaja["name"]}','{pelaaja["airport_counter"]}','{pelaaja["score"]}')"""
        print("debug: ", tulos)
        kursori.execute(komento)  # suoritetaan komento
        game_temp_tulos = kursori.fetchall()  # haetaan kaikki tulokset
        print("debug: ", tulos)
    kursori.close()

    return True

def hae_keskeneräisen_pelin_tiedot(yhteys)->dict:
    '''
    Hakee taulusta game_temp ja user_temp keskeneräisen pelin tiedot
    Jos ei ole palauttaa tyhjän sanakirjan
    Muuten palauttaa:
    `{
    "continent":"Europe", //tms
    "country":"findland", //tms
    "players":[
        [
            "name":"Pelaaja1",
            "airport":1,
            "score": 25
        ],
        [
            "name":"Pelaaja2",
            "airport":2,
            "score": 20
        ]
    ]
    }
    '''

    komento = """
     SELECT  continent, country FROM game_temp;
     """
    kursori = yhteys.cursor()  # luodaan kursori
    kursori.execute(komento)  # suoritetaan komento
    game_temp_tulos = kursori.fetchall()  # haetaan kaikki tulokset
    kursori.close()

    komento = """
     SELECT  name, airport_counter, user_points FROM user_temp;
     """
    kursori = yhteys.cursor()  # luodaan kursori
    kursori.execute(komento)  # suoritetaan komento
    user_temp_tulos = kursori.fetchall()  # haetaan kaikki tulokset
    kursori.close()

    print(game_temp_tulos, user_temp_tulos)
    if game_temp_tulos == [] and user_temp_tulos == []:
        return {} #ei ole keskeneräistä peliä
    elif user_temp_tulos == [] and game_temp_tulos != []:
        tulos = {
            "continent": game_temp_tulos[0][0],
            "country": game_temp_tulos[0][1],
            "players": []
        }
    elif user_temp_tulos != [] and game_temp_tulos != []:

        players = []
        for rivi in user_temp_tulos:
            players.append({"name": rivi[0], "airport_counter": rivi[1], "score": rivi[2]})
        tulos = {
            "continent": game_temp_tulos[0][0],
            "country": game_temp_tulos[0][1],
            "players": players
        }

    return tulos


def uusi_peli(yhteys, pelin_tiedot):
    ''''
    Luo uuden pelin game_tauluun

    pelin_tiedot = {country: "Finland", continent: "Europe"}
    '''

    poista_peli(yhteys) #tyhennetään game_temp ja user_temp taulut

    country = pelin_tiedot["country"]
    continent = pelin_tiedot["continent"]


    if country != "*":
        #parametrisoitu kysely sql injektion estämiseksi
        komento = "SELECT continent from country WHERE name = %s;"
        kursori = yhteys.cursor()
        kursori.execute(komento,(country,))
        continent = kursori.fetchone()[0]

    #haetaan maan maanosa
    print("debug: ", continent)
    #parametrisoitu kysely sql injektion estämiseksi
    komento = "INSERT INTO game_temp (continent, country) VALUES (%s, %s);"
    kursori = yhteys.cursor()  # luodaan kursori
    kursori.execute(komento, (continent, country))  # suoritetaan komento

    kursori.close()




def poista_peli(yhteys):
    '''
    Kesken olevan pelin tiedot poistetaan

    eli taulut game_temp ja user_temp tyhjennetään tiedoista
    '''

    komento = """DELETE FROM game_temp;"""

    kursori = yhteys.cursor()  # luodaan kursori
    kursori.execute(komento)  # suoritetaan komento
    tulos = kursori.fetchall()  # haetaan kaikki tulokset
    kursori.close()
    print("debug: ", tulos)

    komento = """DELETE FROM user_temp;"""
    kursori = yhteys.cursor()  # luodaan kursori
    kursori.execute(komento)  # suoritetaan komento
    tulos = kursori.fetchall()  # haetaan kaikki tulokset
    kursori.close()

    print("debug: ", tulos)

def hae_viimeisimman_pelin_tiedot(yhteys:object):
    '''
    Hakee viimeisimmän pelin tiedot game, user_games ja user_information tauluista
    pelaajat lajitellaan pisteiden mukaan laskevaan järjestykseen
    '''


    komento = """SELECT name, user_points 
    FROM user_games 
    WHERE game_id = (SELECT MAX(game_id) FROM user_games) ORDER BY user_points DESC;"""


    kursori = yhteys.cursor()  # luodaan kursori
    kursori.execute(komento)  # suoritetaan komento
    tulos = kursori.fetchall()  # haetaan kaikki tulokset
    kursori.close()

    pelaajatiedot = []

    for rivi in tulos:
        score = round(rivi[1], 2)
        pelaajatiedot.append({"name": rivi[0], "score": rivi[1]})

    vastaus = {
        "players": pelaajatiedot
    }

    return vastaus

def hae_pelaajatiedot(yhteys: object)->dict:
    '''
    palauttaa pelaajien nimet, pelattujen pelien määrän ja pisteiden keskiarvon (kaikista peleistä)
    '''
    komento = """
    SELECT
        user_information.name,
        COUNT(user_games.game_id) AS games_played,
        SUM(user_games.user_points) AS total_points,
        (SELECT game.continent
         FROM user_games AS ug
         JOIN game ON ug.game_id = game.game_id
         WHERE ug.name = user_information.name
         GROUP BY game.continent
         ORDER BY SUM(ug.user_points) DESC
         LIMIT 1) AS top_continent
    FROM
        user_information
    LEFT JOIN
        user_games ON user_information.name = user_games.name
    GROUP BY
        user_information.name
    ORDER BY
        total_points DESC;
    """


    kursori = yhteys.cursor()  # luodaan kursori
    kursori.execute(komento)  # suoritetaan komento
    tulos = kursori.fetchall()  # haetaan kaikki tulokset
    kursori.close()


    continents = "*"
    pelaajatiedot = []
    for rivi in tulos:

        ranking = rivi[2] / rivi[1] if rivi[1] > 0 else 0 #lasketaan keskiarvo
        ranking = round(ranking, 2) #pyöristetään kahdelle desimaalille
        if rivi[3] == "*":
            pelaajatiedot.append({"name": rivi[0], "total_games": rivi[1], "ranking": ranking, "top_continent": continents})
        else:
            pelaajatiedot.append({"name": rivi[0], "total_games": rivi[1], "ranking": ranking, "top_continent": rivi[3]})


    vastaus = {
        "players": pelaajatiedot
    }

    return vastaus


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



        pelin_tiedot = {
            "continent":"Europe",
            "country":"finland"
        }

        pelaajatiedot = {
            "players":[
                {
                    "name":"Pelaaja1",
                    "airport_counter":2,
                    "score": 12
                },
                {
                    "name":"Pelaaja2",
                    "airport_counter":0,
                    "score": 0
                }
            ]
        }

        #poista_peli(yhteys)

        #print(hae_keskeneräisen_pelin_tiedot(yhteys))
        #print(tallenna_pelin_tiedot(yhteys))
        #uusi_peli(yhteys,pelin_tiedot)
        #print(tallenna_keskeneraisen_pelin_tiedot(yhteys,pelaajatiedot))

        print(hae_viimeisimman_pelin_tiedot(yhteys))