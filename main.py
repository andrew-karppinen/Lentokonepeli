import mysql.connector
from colorama import init, Fore, Style
init()
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




valinta = input(Fore.LIGHTWHITE_EX + "Valitse toiminto:\n1 = Uusi peli\n2 = Tulosta käyttäjien pistetilastot\n3 = Poistu\n").lower()


while True: #valikko, pyörii kunnes käyttäjä antaa oikenlasen syötteen
    if valinta == "1":
        break
    elif valinta == "2":
        tulosta_pelaajatiedot(yhteys)
        exit()
    elif valinta == "3":
        exit()




#peliin:

print("Valitse maanosa: " + ", ".join(maanosakoodit(yhteys)))

print("Valitse * jos haluat pelata kaikissa maanosissa.")

maanosa = input("Valinta: ").upper()


pelin_tiedot = PelinTiedot(maanosa) #luodaan pelin tiedot olio


while True: #kysytään käyttäjältä pelaajien määrä ja tarkistetaan syötteen oikeellisuus
    pelaajien_maara = input("Anna pelaajien määrä: (1-5): ") #ei tee tällä hetkellä mitään

    if pelaajien_maara.isdigit() == False: #virheellinen syöte
        print("Virheellinen syöte")
        continue
    else:
        pelaajien_maara = int(pelaajien_maara)
        if pelaajien_maara < 1 or pelaajien_maara > 5:
            print("Virheellinen syöte")
            continue
        else:
            break


for i in range(pelaajien_maara):

    nimimerkki = input("Anna nimimerkki: ")

    pelin_tiedot.pelaajat_[nimimerkki] = 0 #lisätään pelaaja tiedot olioon

    for i in range(0,5): #pelaaja pelaa 5 kierrosta


        print(Fore.LIGHTBLUE_EX + "--------------------------------------------------------" + Fore.RESET)
        print(Fore.LIGHTWHITE_EX + "Kierros: ", i+1)
        print()
        kohdelentokentta,kohdemaa,maanosa = arpominen(yhteys, maanosa) #arvotaan maa ja lentokenttä
        print(kohdelentokentta)

        pisteet = 5 #pelaajan pisteet
        arvaus = input(Fore.LIGHTWHITE_EX + "Arvaa maa jossa lentokenttä sijaitsee: ")

        while True: #peli silmukka

            if pisteet == 0:
                break

            if arvaus.lower() == kohdemaa.lower():
                print(Fore.GREEN + "✅ Arvauksesi oli oikein!" + Fore.RESET)
                break
            else:
                etaisyys = hae_etaisyys_lentokentta(yhteys,kohdelentokentta,arvaus)
                if etaisyys == False: #jos maata ei löydy
                    maat = hae_maat(yhteys)
                    print(Fore.RED + f"Maata nimellä " + arvaus + " ei löytynyt tai sillä ei ole lentokenttiä." + Style.RESET_ALL)
                    print(Fore.LIGHTWHITE_EX + "Tarkoititko: ", tarkistamaa(maat,arvaus))
                    print("Arvaa uudelleen:", end=' ')
                else:
                    print(Fore.RED + f"❌ Väärin, etäisyys: {etaisyys:.0f} km" + Fore.RESET)
                    print(Fore.LIGHTWHITE_EX + "Arvaa uudelleen:", end=' ')
                arvaus = input()  # Odotetaan pelaajan uutta arvausta

            pisteet -= 1

        print(Fore.LIGHTWHITE_EX + "Maa oli: ", kohdemaa)
        print("Pisteet kierroksesta: ", pisteet)
        pelin_tiedot.pelaajat_[nimimerkki] += pisteet #päivitetään pelaajan pisteet pelin tiedot olioon



pelin_tiedot.tallenna_pelin_tiedot(yhteys) #tallennetaan pelin tiedot tietokantaan

pelin_tiedot.tulosta_tiedot() #tulostetaan pelin tiedot

yhteys.close() #suljetaan tietokantayhteys




