#Funktio arpoo lentokentän nimen, maan nimen sille annetun mantereen mukaan.

maanosa = input("Anna Manner: ")

def arpominen(yhteys,maanosa):
    randomaus = f"SELECT airport.name, country.name, country.continent FROM airport LEFT JOIN country on airport.iso_country = country.iso_country where country.continent = '{maanosa}' ORDER BY RAND() LIMIT 1;"
    kursori = yhteys.cursor()
    kursori.execute(randomaus)
    tulos = kursori.fetchall()
    return tulos

tallennus = arpominen(yhteys,maanosa)

print(tallennus)
