import mysql.connector


def hae_maat(yhteys:object, maanosa:str= "*"):

    '''
    Tehdään sql kysely ja palautetaan serveriltä saatu vastaus
    '''

    maanosa = maanosa.upper() #muutetaan maanosa isoihin kirjaimiin

    if maanosa == "*":
        komento = f"SELECT DISTINCT name from country ORDER BY name;"  # sql komento
    else:
        komento = f"SELECT DISTINCT name from country WHERE continent='{maanosa}' ORDER BY name;"  #sql komento
    kursori = yhteys.cursor() #luodaan kursori

    kursori.execute(komento) #suoritetaan komento
    tulos = kursori.fetchall()  #haetaan kaikki tulokset
    kursori.close()


    return [rivi[0] for rivi in tulos]



if __name__ == '__main__': #pääohjelma

    # luodaan sql yhteys
    yhteys = mysql.connector.connect(
        host="localhost",
        port=3306,
        database='flight_game',
        user="sqlkayttaja",
        password="salasana123",
        connection_timeout=5,
        autocommit=True)


    print(hae_maat(yhteys, "*")) #testataan funktiota