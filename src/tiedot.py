import mysql.connector



class PelinTiedot:
    def __init__(self,maanosa:str):

        self.maanosa_ = maanosa
        self.pelaajat_ = {} #("nimi":pisteet)


    def tulosta_tiedot(self):
        '''
        Tulostaa pelin tiedot
        '''
        print(f"Maanosa: {self.maanosa_}")
        for pelaaja in self.pelaajat_:
            print(f"Pelaaja: {pelaaja}, Pisteet: {self.pelaajat_[pelaaja]}")
    
    

    def onko_pelaaja_olemass(self, yhteys, nimi)->bool:
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

    def luo_pelaaja(self, yhteys, nimi):
        '''
        Luo uuden pelaajan tietokantaan
        '''

        if self.onko_pelaaja_olemass(yhteys, nimi) == False: #käyttäjää  ei ole jo olemassa
            komento = f"INSERT INTO user_information (name) VALUES ('{nimi}');"

            kursori = yhteys.cursor()  # luodaan kursori
            kursori.execute(komento)
            kursori.close()


    def tallenna_pelin_tiedot(self, yhteys):

        #lisätään game tauluun uusi rivi
        #continent = self.maanosa_
        if self.maanosa_ == "*":
            komento = "INSERT INTO game (continent) VALUES (NULL);"
        else:
            komento = f"INSERT INTO game (continent) VALUES ('{self.maanosa_}');"
        kursori = yhteys.cursor()  # luodaan kursori
        kursori.execute(komento)  # suoritetaan komento


        #lisätään user_games tauluun uusi rivi
        for pelaaja in self.pelaajat_:
            self.luo_pelaaja(yhteys, pelaaja) #yritetään luoda pelaaja, jos pelaaja jo on tämä ei tee mitään

            komento = f"""INSERT INTO user_games (game_id,user_points,name)
            values ((SELECT MAX(game_id) FROM game),{self.pelaajat_[pelaaja]},'{pelaaja}');
            """ #lisätään pelaajalle uusi rivi user_games tauluun

            kursori.execute(komento)  # suoritetaan komento

        kursori.close()

def tulosta_pelaajatiedot(yhteys: object):
    '''
    Tulostaa pelaajien nimet, pelattujen pelien määrän ja pisteiden keskiarvon
    '''
    komento = """
    SELECT
        user_information.name,
        COUNT(user_games.game_id) AS games_played,
        SUM(user_games.user_points) AS total_points
    FROM
        user_information
    LEFT JOIN
        user_games ON user_information.name = user_games.name
    GROUP BY
        user_information.name;
    """
    kursori = yhteys.cursor()  # luodaan kursori
    kursori.execute(komento)  # suoritetaan komento
    tulos = kursori.fetchall()  # haetaan kaikki tulokset

    for rivi in tulos:
        print(f"Pelaaja: {rivi[0]}, Pelit: {rivi[1]}, Pisteeiden keskiarvo: {rivi[2]/rivi[1]}")

    kursori.close()



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

        tiedot = PelinTiedot("Eu")

        tiedot.pelaajat_ = {"Jukka": 0, "Matti": 0, "Pekka": 0} #luodaan pelaaajat
        tiedot.pelaajat_["Jukka"] = 3 #muokattan pelaajien pisteitä
        tiedot.pelaajat_["Matti"] = 5
        tiedot.pelaajat_["Pekka"] = 0

        tiedot.tallenna_pelin_tiedot(yhteys) #tallennetaan pelin ja pelaajien tiedot tietokantaan
        tulosta_pelaajatiedot(yhteys)
        #tiedot.LuoPelaaja(yhteys,"Jukka")

