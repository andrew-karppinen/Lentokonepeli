






# API


### /getcontinents/

palauttaa
    
`{
    "continents": ["Europe", "Asia", "Africa","jne"]
}`



### /getcountries/

Parametrit:

`{
    "continent": "Europe"
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






### /get-user-scores/

Palauttaa:

`{
    "players":[
        [
            "name":"Pelaaja1",
            "ranking": 7, // keskiarvo pelaajan pisteistä 0-25
            "victories": 10,
            "total_games": 20
        ],
        [
            "name":"Pelaaja2",
            "ranking": 4,
            "victories": 5,
            "total_games": 10
        ]
    ]
}`




### /new-game/

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
            "airport":1, //airport 1/5            
            "score": 7 //0-25
        ],
        [
            "name":"Pelaaja2",
            "airport":2, //airport 2/5
            "score": 21
        ]
    ]
}`

### /save-game/

Tallenna taustapalvelimelle keskeneräisen pelin tiedot

Parametrit:

`{
    "game_id": 1,
    "players":[
        [
            "name":"Pelaaja1",
            "airport":1,            
            "score": 25 //0-25
        ],
        [
            "name":"Pelaaja2",
            "airport":2,
            "score": 20
        ]
    ]
}`



