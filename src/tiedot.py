import mysql.connector
import os

'''
Toiminnot:
Keskeneräisen pelin tietojen tallentamiseen ja hakemiseen (game_temp ja user_temp taulut)

Pelattujen pelien ja pistetilastojen hakemiseen (user_information, user_games game taulut)

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
    Tallentaa valmiin pelin tiedot tietokantaan
    '''

    #haetaan pelin tiedot

    hae_keskeneräisen_pelin_tiedot(yhteys)


    if maanosa_ == "*":
        komento = "INSERT INTO game (continent) VALUES (NULL);"
    else:
        komento = f"INSERT INTO game (continent) VALUES ('{maanosa_}');"
    kursori = yhteys.cursor()  # luodaan kursori
    kursori.execute(komento)  # suoritetaan komento


    #lisätään user_games tauluun uusi rivi
    for pelaaja in pelaajat_:
        luo_pelaaja(yhteys, pelaaja) #yritetään luoda pelaaja, jos pelaaja jo on tämä ei tee mitään

        komento = f"""INSERT INTO user_games (game_id,user_points,name)
        values ((SELECT MAX(game_id) FROM game),{pelaajat_[pelaaja]},'{pelaaja}');
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
    }`
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

        tulos = {
            "continent": game_temp_tulos[0][0],
            "country": game_temp_tulos[0][1],
            "players": user_temp_tulos
        }

    return tulos


def uusi_peli(yhteys, pelin_tiedot):
    ''''
    Luo uuden pelin game_tauluun

    pelin_tiedot = {country: "Finland", continent: "Europe"}
    '''

    poista_peli(yhteys) #tyhennetään game_temp ja user_temp taulut

    komento = f"INSERT INTO game_temp (continent, country) VALUES ('{pelin_tiedot['continent']}', '{pelin_tiedot['country']}');"
    kursori = yhteys.cursor()  # luodaan kursori
    kursori.execute(komento)  # suoritetaan komento
    tulos = kursori.fetchall()  # haetaan kaikki tulokset
    print("debug: ", tulos)
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




    continents = "Koko maapallo"
    pelaajatiedot = []
    for rivi in tulos:
        if rivi[3] is None:
            pelaajatiedot.append({"name": rivi[0], "total_games": rivi[1], "ranking": rivi[2] / rivi[1] if rivi[1] > 0 else 0, "top_continent": continents})
        else:
            pelaajatiedot.append({"name": rivi[0], "total_games": rivi[1], "ranking": (rivi[2] / rivi[1] if rivi[1] > 0 else 0), "top_continent": rivi[3]})


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
            "country":""
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

        poista_peli(yhteys)

        #print(hae_keskeneräisen_pelin_tiedot(yhteys))


        #print(hae_pelaajatiedot(yhteys))
        #uusi_peli(yhteys,pelin_tiedot)
        #poista_peli(yhteys)
        #print(tallenna_keskeneraisen_pelin_tiedot(yhteys,pelaajatiedot))
