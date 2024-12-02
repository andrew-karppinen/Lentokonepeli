'use strict';


const player1 = document.getElementById('player1');
const player2 = document.getElementById('player2');
const player3 = document.getElementById('player3');
const player4 = document.getElementById('player4');
const player5 = document.getElementById('player5');
const player6 = document.getElementById('player6');

const pelaajat = [player1,player2,player3,player4,player5,player6];


const aloita_nappi = document.getElementById('aloita_nappi')
const peruuta_nappi = document.getElementById('peruuta_nappi')


let maa = "suomi";
let maanosa = "eurooppa";


let pelin_tiedot = { 'gamedata':{'country': maa, 'continent': maanosa, 'players':[]}};


aloita_nappi.addEventListener('click', function() {



    for (let pelaaja of pelaajat) {

        if (pelaaja.value != '')
        {
            let pelaaja_tiedot = {'name': pelaaja.value, 'score': 0, 'airport_counter': 0};
            pelin_tiedot['gamedata']['players'].push(pelaaja_tiedot);

        }
    }

    if (pelin_tiedot['gamedata']['players'].length === 0) //yhtään pelaajaa ei ole syötetty
    {
        alert("syötä pelaajien nimet");
    }
    else {

        //pelaajat ja muut tiedot syötetty onnistuneesti
        //tallennetaan pelin tiedot serverille post menetelmällä

        fetch('/api/new-game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(pelin_tiedot)
        })
            .then(function(response) {
                if (!response.ok) {
                    console.log("tässä");
                    throw new Error('error'); //aiheuttaa virheen
                }
                return response.json(); //palauttaa promise jos ei tule erroria
            })
            .then(function(data) {
                console.log(data);

            })
            .catch(function(error) { //virhe
                console.log(error);
            });


    }




});


peruuta_nappi.addEventListener('click', function() {
    window.location.href = "/";
});

