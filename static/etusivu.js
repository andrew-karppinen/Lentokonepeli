'use strict';


/*

 */


document.getElementById('pelaa_nappi').addEventListener('click', function() {

    /* Haetaan mahdolliset pelitiedot
    /api/get-saved-game

    jos nämä löytyy ohjataan sivulle jatketaanko.html

    muuten uusipeli.html
     */

    fetch ('/api/get-saved-game')
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {

            if ('country' in data && 'continent' in data && 'players' in data && data['players'].length > 0) { // Tarkistetaan, löytyykö tarvittavat pelitiedot
                console.log('Löytyi tallennettu peli');
                window.location.href = '/jatketaanko.html';
            }
             else { //jos ei ohjataan käyttäjä luomaan uusi peli
                window.location.href = '/uusipeli.html';
            }
        }).catch(function(err) { // Virheenkäsittely
            alert('Virhe yhdistettäessä taustapalveluun');
        });




});