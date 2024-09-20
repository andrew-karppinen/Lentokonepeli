import mysql.connector

from src import * #importataan funktiot






def yhdista():

    '''
    Käyttöliittymä serveriin yhdistämiseen

    Jos yhdistäminen onnistuu, palautetaan yhteys
    muuten palautetaan False

    Mahdollista käyttää tiedostoon tallennettuja asetuksia

    '''


    while True:

        asetukset = LueAsetukset() #yritys lukea asetukset tiedostosta

        lue_asetukset = False

        if asetukset != False: #asetukset löytyy tiedostosta
            if input("serverin asetukset on tallennettu aikaisemmalla kerralla haluatko käyttää niitä (k/e): ").lower() == "k":
                lue_asetukset = True
                server_ip,kayttaja,salasana = asetukset


        if lue_asetukset == False: #kysytään asetukset käyttäjältä
            print("Anna sql palvelimen tiedot, (exit = poistu)")
            server_ip = input("Anna serverin ip: ")
            kayttaja = input("Anna käyttäjätunnus: ")
            salasana = input("Anna salasana: ")


        if "exit" in (server_ip,kayttaja,salasana): #jos käyttäjä haluaa poistua
            return False


        # yhteys
        try:
            yhteys = mysql.connector.connect(
                host=server_ip,
                port=3306,
                database='flight_game',
                user=kayttaja,
                password=salasana,
                autocommit=True)
        except mysql.connector.Error as err:  # virhe yhteyden muodostamisessa
            print("Virhe yhteyden muodostamisessa tietokantaan: ", err)
            continue

        else:
            if lue_asetukset == False: #jos asetukset on luettu tiedostosta, ei kysytä uudestaan
                if input("Yhteys muodostettu onnistuneesti, haluan tallentaa asetukset (k/e)").lower() == "k":
                    TallennaAsetukset(server_ip,kayttaja,salasana)

            return yhteys




yhteys = yhdista()


print("Maanosat: ", maanosakoodit(yhteys))


print("Pelaa kaikissa maanosissa: * ")
print("Tai anna jokin maanosa")


valinta = input("Valinta: ").upper()

print(arpominen(yhteys,valinta))