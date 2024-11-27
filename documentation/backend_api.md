






# API

endpoint: /api/


### /getcontinents/
Menetelmä: GET

palauttaa tiedot json muodossa:

```    
{
    "continents": ["EU", "NA", "SA", "AF", "AS", "OC"]
}
```

### /getcountries/
Menetelmä: GET

Parametrit:

valinnainen url parametri: continent: "EU"

Palauttaa:

```
{
    "countries": ["Finland", "Sweden", "Norway"]
}
```


### /getairport/
Menetelmä: GET

Parametrit:

2kpl valinnaisia url parametreja: 

continent, country


Palauttaa:

```
{
    "airport":{
        "airport_name": "Helsinki-Vantaa",
        "country": "Finland",
        "continent": "Europe",
        "latitude_deg": 60.3172,
        "longitude_deg": 24.9633 
    }
}
```

### /calculate-distance/
Menetelmä: GET

url parametrit:

latitude_deg, 
longitude_deg,
airport_name

palauttaa etäisyyden kilometreinä ja annetun lentokentän sijainnin:
    
```
{
    "distance": etaisyys,
    "airport_location": sijanti
}
```

### /get-user-scores/
Menetelmä: GET

Palauttaa pelaajien tietoja pelatuista peleistä:
huom ei liity keskeneräiseen peliin vaan aikaisempiin peleihin!

```
{
    "players":[
        {
            "name":"Pelaaja1",
            "ranking": 7, // keskiarvo pelaajan pisteistä 0-25
            "victories": 10,
            "total_games": 20
        },
        {
            "name":"Pelaaja2",
            "ranking": 4,
            "victories": 5,
            "total_games": 10
        }
    ]
}
```

huomaa että lista voi olla tyhjä jos pelaajia ei ole


### /new-game/
Luo uuden-pelin ja poistaa vanhan pelin tiedot
Menetelmä: POST


Parametrit:

```
{
    "continent": "Europe",
    "country": "Finland",
    "players":[
        "Pelaaja1",
        "Pelaaja2"
    ]
}
```

### /get-saved-game/
Menetelmä: GET

Hae taustapalvelimelta keskeneräisen pelin tiedot
jos ei ole tietoja palauttaa tyhjän sanakirjan

"players" kohta voi myös olla tyhjä jos pelin tietoja ei ole tallennettu vielä

Palauttaa:
```
{
    "continent": "Europe",
    "country": "Finland",
    "players":[
        [
            "name":"Pelaaja1",
            "airport":1,          
            "score": 7 
        ],
        [
            "name":"Pelaaja2",
            "airport":2, 
            "score": 21
        ]
    ]
}
```



### /save-game/
Menetelmä: POST

Tallenna taustapalvelimelle keskeneräisen pelin tiedot

Parametrit:

```
{
    "players":[
        [
            "name":"Pelaaja1",
            "airport":1,           
            "score": 25 
        ],
        [
            "name":"Pelaaja2",
            "airport":2,
            "score": 20
        ]
    ]
}
```

airport on numero joka on 0-5,
jos esim 3 pelaaja on pelannut 3 lentokenttää ja 2 on jäljellä

jos kaikkien pelaajien airport numero on 5 taustapalvelu tulkitsee pelin päättyneeksi ( Toiminto kesken!)
ja tallentaa pelin tiedot automaattisesti pysvästi ( Toiminto kesken!)
