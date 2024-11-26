






# API

endpoint: /api/


### /getcontinents/

palauttaa
    
`{
    "continents": ["EU", "NA", "SA", "AF", "AS", "OC"] //jne
}`



### /getcountries/

Parametrit:

`{
    "continent": "Europe" //valinnainen
}`

Palauttaa:

`{
    "countries": ["Finland", "Sweden", "Norway"]
}`



### /getairport/

Parametrit:

`{
    "continent": "Europe",
    "country": "Finland"
}`

Palauttaa:

`{
    "airport":{
        "airport_name": "Helsinki-Vantaa",
        "country": "Finland",
        "continent": "Europe",
        "latitude_deg": 60.3172,
        "longitude_deg": 24.9633 
    }
}`





### /get-user-scores/

Palauttaa:

`{
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
}`




### /new-game/

Pyyhkii mahdollisen keskeneräisen pelin ja luo uuden pelin

Parametrit:

`{
    "continent": "Europe",
    "country": "Finland",
    "players":[
        "Pelaaja1",
        "Pelaaja2"
    ]
}`

Palauttaa:
Onnistuessaan:

`
{
    "game_id": 1
}
`


### /get-saved-game/

Hae taustapalvelimelta keskeneräisen pelin tiedot

Palauttaa:

`{
    "game_id": 1,
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
}`

### /save-game/

Tallenna taustapalvelimelle keskeneräisen pelin tiedot

Parametrit:

`{
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
}`


airport on numero joka on 0-5,
jos esim 3 pelaaja on pelannut 3 lentokenttää ja 2 on jäljellä

jos kaikkien pelaajien airport numero on 5 taustapalvelu tulkitsee pelin päättyneeksi
