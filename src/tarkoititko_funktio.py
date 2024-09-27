import mysql.connector
import difflib



def hae_maat(yhteys:object)->list:
    '''
    Haetaan sql palvelimelta kaikkien maiden nimet ja palautetaan ne
    '''

    komento = "SELECT name FROM country;"  #sql komento
    kursori = yhteys.cursor() #luodaan kursori
    kursori.execute(komento) #suoritetaan komento
    tulos = [rivi[0].lower() for rivi in
             kursori.fetchall()] #haetaan kaikki tulokset
    kursori.close()

    return tulos

def tarkistamaa(maat: list, kayttajan_syote: str) -> str:
    '''
    Palautetaan maan nimi joka on lähimpänä käyttäjän syötettä
    '''
    kayttajan_syote = kayttajan_syote.lower()

    if kayttajan_syote in maat:
        return None

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
            user='sqlkayttaja',
            password='salasana123',
            autocommit=True
        )
        return yhteys

    except mysql.connector.Error as err:  # virhe yhteyden muodostamisessa
        print(err)


    else:  # yhteys muodostettu onnistuneesti
        print(hae_maat(yhteys))


if __name__ == '__main__': #testiohjelma
    yhteys = muodosta_yhteys()

    if yhteys:

        maat=hae_maat(yhteys)
        kayttajan_syote = input("Anna maan nimi: ")

        tulos = tarkistamaa(maat, kayttajan_syote)

        print(tulos)

        yhteys.close()