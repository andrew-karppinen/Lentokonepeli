#Funktio arpoo lentokentän nimen, maan nimen ja mantereen

def arpominen():
    randomaus = f'SELECT airport.name, country.name, country.continent FROM airport LEFT JOIN country on airport.iso_country = country.iso_country ORDER BY RAND() LIMIT 1;'
    kursori = yhteys.cursor()
    kursori.execute(randomaus)
    tulos = kursori.fetchall()
    return tulos

tallennus = arpominen()

print(tallennus)
