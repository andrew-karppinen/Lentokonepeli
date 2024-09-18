#Funktio arpoo lentokentän nimen, maan nimen ja mantereen

def arpominen(yhteys,maanosa):
    randomaus = f'SELECT airport.name, country.name FROM airport LEFT JOIN country on airport.iso_country = country.iso_country ORDER BY RAND() where country.continent = {maanosa} LIMIT 1;'
    kursori = yhteys.cursor()
    kursori.execute(randomaus)
    tulos = kursori.fetchall()
    return tulos

tallennus = arpominen()

print(tallennus)
