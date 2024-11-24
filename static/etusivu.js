'use strict';


/*
Esimerkki javascriptistä joka käyttää flaskin apia
 */


let data = fetch("api/getcontinents") //palauttaa promise olion
    .then(response => response.json()) //yritetään muuttaa vastaus JSON muotoon
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.log("Virhe:", error);  // Käsitellään virheet, jos niitä tulee
    });
