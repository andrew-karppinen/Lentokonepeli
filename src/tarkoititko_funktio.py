import mysql.connector
import difflib



'''
Esimerkki yhteyden muodostamisesta ja yhteysolion viemisestä funktiolle
'''


def KyselyFunktio(yhteys:object)->list:
    '''
    Tehdään sql kysely ja palautetaan serveriltä saatu vastaus
    '''

    komento = "SELECT name FROM country;"  #sql komento
    kursori = yhteys.cursor() #luodaan kursori
    kursori.execute(komento) #suoritetaan komento
    tulos = [rivi[0].lower() for rivi in
             kursori.fetchall()] #haetaan kaikki tulokset
    kursori.close()

    return tulos

def tarkistamaa(maat: list, kayttajan_syote: str) -> str:
    kayttajan_syote = kayttajan_syote.lower()

    if kayttajan_syote in maat:
        return kayttajan_syote.capitalize()

    lahimmat = difflib.get_close_matches(kayttajan_syote, maat, n=1, cutoff=0.6)

    if lahimmat:
        return lahimmat[0].capitalize()
    else:
        return "Maan nimeä ei löytynyt"


def muodosta_yhteys():
    try:
        yhteys = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            database='flight_game',
            user='jessecs',
            password='mariadb',
            autocommit=True
        )
        return yhteys

    except mysql.connector.Error as err:  # virhe yhteyden muodostamisessa
        print(err)


    else:  # yhteys muodostettu onnistuneesti
        print(KyselyFunktio(yhteys))


if __name__ == '__main__': #pääohjelma
    yhteys = muodosta_yhteys()

    if yhteys:

        maat=KyselyFunktio(yhteys)
        kayttajan_syote = input("Anna maan nimi: ")

        tulos = tarkistamaa(maat, kayttajan_syote)

        print(tulos)

        yhteys.close()