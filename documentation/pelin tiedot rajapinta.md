
# Toiminnot pelaajien pelien ja pistemäärien ylläpidolle ja tulostamiselle



> tiedot = PelinTiedot("EU")  #luo rajapinnan pelin tiedoille



> tiedot.pelaajat_["jorma"] = 3 #lisätään pelaaja 

> tiedot.pelaajat_["jorma"] = 5 #muokataan pelaajan pisteitä


## Kun peli on ohi tallennetaan pelin ja pelaajien tiedot tietokantaan

> tiedot.tallenna_pelin_tiedot(yhteys:object)


## Tulosta pelaajien Tiedot:

> tulosta_pelaajatiedot(yhteys:object)
