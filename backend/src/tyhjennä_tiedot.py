import mysql.connector

def tyhjennä_tiedot(yhteys: object):

    komento = """
    SET foreign_key_checks = 0;
    TRUNCATE TABLE game;
    TRUNCATE TABLE user_games;
    TRUNCATE TABLE user_information;
    SET foreign_key_checks = 1;
    """

    try:
        kursori = yhteys.cursor()  # luodaan kursori
        for lause in komento.strip().split(';'):
            if lause.strip():  # Varmistetaan, ettei tyhjät lauseet suorita
                kursori.execute(lause)  # suoritetaan komento
        yhteys.commit()  # varmistetaan muutokset
    except Exception as e:
        print(f"Virhe suoritettaessa komentoja: {e}")
    finally:
        kursori.close()  # suljetaan kursori



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