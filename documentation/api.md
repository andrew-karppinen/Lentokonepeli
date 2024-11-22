






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
            "ranking": 100,
            "victories": 10,
            "total_games": 20
        ],
        [
            "name":"Pelaaja2",
            "ranking": 200
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
            "score": 100
        ],
        [
            "name":"Pelaaja2",
            "airport":2, //airport 2/5
            "score": 200
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
            "score": 100
        ],
        [
            "name":"Pelaaja2",
            "airport":2,
            "score": 200
        ]
    ]
}`



