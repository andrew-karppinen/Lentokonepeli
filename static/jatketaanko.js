'use strict';









const jatka_nappi = document.getElementById('jatka_nappi');
const uusipeli_nappi = document.getElementById('uusipeli_nappi');
const peruuta_nappi = document.getElementById('peruuta_nappi');





jatka_nappi.addEventListener('click', function() {
    window.location.href = "/peli";
});



uusipeli_nappi.addEventListener('click', function() {
    window.location.href = "/uusipeli.html";

});



peruuta_nappi.addEventListener('click', function() {
    window.location.href = "/";
});

