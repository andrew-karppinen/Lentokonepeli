'use strict';


/*

 */


document.getElementById('pelaa_nappi').addEventListener('click', function() {

    /* Haetaan mahdolliset pelitiedot
    /api/get-saved-game
     */

    fetch ('/api/get-saved-game')
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {

            if ('country' in data && 'continent' in data && 'players' in data && data['players'].length > 0) {
                console.log('Löytyi tallennettu peli');
                console.log(data);
            }
             else {
                console.log("error");
            }
        });




});