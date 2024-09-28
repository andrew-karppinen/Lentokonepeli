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




yhteys = yhdista() #yhdistetään tietokantaan

if yhteys == False: #jos yhtyes
    exit()




valinta = input("valitse toiminto: 1 = uusi peli 2 = tulosta käyttäjien pistetilastot, 3 = poistu ").lower()


if valinta == "2":
    tulosta_pelaajatiedot(yhteys)
    exit()
elif valinta == "3":
    exit()




#peliin:

print("Maanosat: ", maanosakoodit(yhteys))

print("Pelaa kaikissa maanosissa: * ")
print("Tai anna jokin maanosa")

maanosa = input("Valinta: ").upper()


pelin_tiedot = PelinTiedot(maanosa) #luodaan pelin tiedot olio

pelaajien_maara = int(input("Anna pelaajien määrä: (1-5): ")) #ei tee tällä hetkellä mitään



nimimerkki = input("Anna nimimerkki: ")

pelin_tiedot.pelaajat_[nimimerkki] = 0 #listään pelaaja tiedot olioon

kohdelentokentta,kohdemaa,maanosa = arpominen(yhteys, maanosa) #arvotaan maa ja lentokenttä
print(kohdelentokentta)


for pisteet in range(10,-1,-1): #peli silmukka
    arvaus = input("Arvaa maa jossa lentokenttä sijaitsee: ")

    if arvaus.lower() == kohdemaa.lower():
        print("Arvauksesi oli oikein!")
        break
    else:
        etaisyys = hae_etaisyys_lentokentta(yhteys,kohdelentokentta,arvaus)
        if etaisyys == False: #jos maata ei löydy
            maat = hae_maat(yhteys)
            print("Tarkoititko: ", tarkistamaa(maat,arvaus))
        else:
            print("Väärin, etäisyys: ", etaisyys)


print("Maa oli: ", kohdemaa)
print("Pisteet: ", pisteet)
pelin_tiedot.pelaajat_[nimimerkki] = pisteet #päivitetään pelaajan pisteet pelin tiedot olioon



pelin_tiedot.tallenna_pelin_tiedot(yhteys) #tallennetaan pelin tiedot tietokantaan

yhteys.close()




