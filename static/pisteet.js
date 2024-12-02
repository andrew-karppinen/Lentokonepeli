'use strict';


//haetaan pelaajien pistetilastot: /api/get-user-scores


const enpoint = '/api/get-user-scores';

const pistetaulukko = document.getElementById('pistetaulukko');

const etusivulle_nappi = document.getElementById('etusivunappi')


etusivulle_nappi.addEventListener('click', function () {
   document.location.href = '/';
});


fetch(enpoint)
    .then(function (response) {
        return response.json();
    })
    .then(function (data) {

        if (data["players"].length != 0 )
        {
            let counter = 1;
            for (let i of data["players"]) {
                let row = pistetaulukko.insertRow(-1);
                let cell1 = row.insertCell(0);

                let cell2 = row.insertCell(1);
                let cell3 = row.insertCell(2);

                cell1.innerHTML = counter;
                cell2.innerHTML = i["name"];
                cell3.innerHTML = i["ranking"];

                counter += 1;
            }

        }


    }).catch(function (err) {
        alert('Virhe yhdistettäessä taustapalveluun');
    });





