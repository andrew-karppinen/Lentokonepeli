'use strict';

//haetaan pelaajien nimi elementit
const player1 = document.getElementById('player1');
const player2 = document.getElementById('player2');
const player3 = document.getElementById('player3');
const player4 = document.getElementById('player4');
const player5 = document.getElementById('player5');
const player6 = document.getElementById('player6');

const pelaajat = [player1,player2,player3,player4,player5,player6]; //laitetaan ne listaan, elämän helpottamiseksi

//haetaan aloita ja peruuta nappi
const aloita_nappi = document.getElementById('aloita_nappi')
const peruuta_nappi = document.getElementById('peruuta_nappi')

//haetaan maanosa ja maa listavalikko elementit
const maa_lista = document.getElementById('maa');
const maanosa_lista = document.getElementById('maanosa');



function paivita_maat(maanosa='*')
{
    let endpoint = '/api/getcountries'+'?continent='+maanosa;

    //haetaan maat /api/getcountries
    fetch(endpoint)
        .then(function(response) {
            if (!response.ok) {
                throw new Error('error');
            }
            return response.json();
        })
        .then(function(data) {
            maa_lista.innerHTML = ""; //tyhjennetään taulukko

            let option = document.createElement('option'); //lisätään * valinta
            option.value = '*'; //value on * ja teksti on *
            option.text = '*'; //value on * ja teksti on *

            maa_lista.appendChild(option);
            for (let i of data['countries']) { //käydään palvelimelta saadut maat läpi
                let option = document.createElement('option');
                option.value = i;
                option.text = i;
                maa_lista.appendChild(option); // Append to maa_lista instead of maanosa_lista
            }
        })
        .catch(function(error) {
            console.log(error);
            alert('Virhe yhdistettäessä taustapalveluun');
        });

}


paivita_maat(); //päivitetään maat kertaalleen


maanosa_lista.addEventListener('change', function() { //jos maanosalistaa muutetaan, päivitetään maat
    paivita_maat(maanosa_lista.value)
});




aloita_nappi.addEventListener('click', function() {

    console.log(maa_lista.value, maanosa_lista.value);

    let pelin_tiedot = {'gamedata':{'country': maa_lista.value, 'continent': maa_lista.value, 'players':[]}};



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
                return response.json(); //palauttaa jsonin jos ei tule erroria
            })
            .then(function(data) {
                console.log(data);

            })
            .catch(function(error) { //virhe
                console.log(error);
                alert('Virhe yhdistettäessä taustapalveluun');
            });


    }




});


peruuta_nappi.addEventListener('click', function() {
    window.location.href = "/";
});

