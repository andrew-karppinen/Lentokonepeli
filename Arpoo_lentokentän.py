#Funktio arpoo lentokentän nimen, maan nimen sille annetun mantereen mukaan.

maanosa = input("Anna Manner: ")

def arpominen(yhteys,maanosa:str="*"):
    
    # Funktio arpoo lentokentän nimen, maan nimen sille annetun mantereen mukaan.
    # Hakutulosta voi rajata maanoasan mukaan tai hakea kaikista maanosista
    
    if maanosa=="*": #haetaan kaikista maanosista
        randomaus = f"SELECT airport.name, country.name, country.continent FROM airport LEFT JOIN country on airport.iso_country = country.iso_country ORDER BY RAND() LIMIT 1;"
    else:
        randomaus = f"SELECT airport.name, country.name, country.continent FROM airport LEFT JOIN country on airport.iso_country = country.iso_country where country.continent = '{maanosa}' ORDER BY RAND() LIMIT 1;"


    kursori = yhteys.cursor()
    kursori.execute(randomaus)
    tulos = kursori.fetchone()
    return tulos


tallennus = arpominen(yhteys,maanosa)

print(tallennus)
