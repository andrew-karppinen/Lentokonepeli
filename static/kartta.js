



// Globaaliin scopeen määritellään muuttujat
let lentokentta, lentokentanNimi, lentokentanLatitude, lentokentanLongitude;


// Muuttuja edellisen merkin ja klikkipisteen tallentamiseen
let currentMarker = null;
let clickLatLng = null;
let arvaaClicked = false; // Tarkistaa, onko "Arvaa" painettu

let pelintiedot = null;

const pelaajan_nimi_elementti = document.getElementById('pelaajan_nimi');
const kierros_elementti = document.getElementById('kierros');
let map = null; // Karttaobjekti globaalissa scopessa

const arvaa_nappi = document.getElementById('arvaa');
const seuraava_nappi = document.getElementById('seuraava');

let kaikki_pelaajat_pelannut = false; //tarkistaa onko kaikki pelaajat pelanneet 5 kertaa


const ajastin_elementti = document.getElementById('aika');

let timerInterval;
let seconds = 25;

let pelaaja = {"name": "", "score": 0, "airport_counter": 0}; //alustetaan pelaaja objekti



function formatTime(sec) {
    let minutes = Math.floor(sec / 60);
    let remainingSeconds = sec % 60;
    return `${String(minutes).padStart(2, '0')}:${String(remainingSeconds).padStart(2, '0')}`;
}

function updateTimer() {
    ajastin_elementti.textContent = formatTime(seconds);

    if (seconds <= 0) {//jos aika loppuu
        stopTimer();
        arvaaClicked = true; //estetään arvausnapin painaminen
        arvaa_nappi.disabled = true; //arvausnappi disabloidaan
        //pisteet 0
        pelaaja["airport_counter"] = pelaaja["airport_counter"] + 1; //päivitetään pelaajan lentokenttä laskuri

        document.getElementById('pisteet').textContent = "Pisteet: " + 0 + " pistettä."; //päivitetään pisteet html sivulle

        tallennatiedot(); //tallennetaan pelin tiedot taustapalvelimelle
    }
}

function startTimer() {
    if (!timerInterval) {
        timerInterval = setInterval(() => {
            seconds--;
            updateTimer();
        }, 1000);
    }
}
function stopTimer() {
    clearInterval(timerInterval);
    timerInterval = null;
}


async function tallennatiedot() {
    /*
    Tallentaa pelin tiedot taustapalvelimelle
     */


    tallennettava_data = {"gamedata":
        {
            "players": pelintiedot["players"]
        }
    }

    kaikki_pelaajat_pelannut = true; //oletetaan että kaikki pelaajat ovat pelanneet 5 kertaa
    for (let i =0;i<pelintiedot["players"].length;i++){
        //käydään läpi kaikki pelaajat, jotta voidaan päivittää pelivuorossa olevan pelaajan tiedot ja tarkistaa onko kaikki pelaajat pelanneet 5 kertaa

        if (pelintiedot["players"][i]["name"] == pelaaja["name"]) //päivitetään pelivuorossa olevan pelaajan tiedot pelintiedot objektiin
        {
            pelintiedot["players"][i]["score"] = pelaaja["score"];
            pelintiedot["players"][i]["airport_counter"] = pelaaja["airport_counter"];
        }
        ''
        if(pelintiedot["players"][i]["airport_counter"] < 5) //jos joku pelaajista ei ole pelannut vielä 5 kertaa
        {
            kaikki_pelaajat_pelannut = false;
        }
    }

    console.log(tallennettava_data);

    await fetch('/api/save-game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(tallennettava_data),
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });


}


async function aseta_kartan_aloituspaikka(maa) {
    /*
    Asettaa kartan aloituspaikan ja zoom-tason maan perusteella
    */

    let lat = 40, lon = 0, zoom = 3; // Koko maapallon oletuskoordinaatit ja zoom

    if (maa !== "*") {
        // Hae koordinaatit maan perusteella
        let endpoint = `https://nominatim.openstreetmap.org/search?country=${encodeURIComponent(maa)}&format=json`;

        try {
            let response = await fetch(endpoint);
            if (!response.ok) {
                throw new Error("Virhe geokoodauspyynnössä.");
            }

            let data = await response.json();
            if (data.length > 0) {
                // Käytä ensimmäistä tulosta
                lat = parseFloat(data[0].lat);
                lon = parseFloat(data[0].lon);
                zoom = 6; // Zoom-taso yksittäiselle maalle
            } else {
                console.error("Maan nimen perusteella ei löytynyt sijaintia.");
                return;
            }
        } catch (error) {
            console.error("Virhe geokoodauksessa:", error);
            return;
        }
    }

    // Luo tai päivitä kartta
    if (!map) {
        // Luo uusi kartta, jos sitä ei ole vielä olemassa
        map = L.map('map').setView([lat, lon], zoom);

        // Lisää OpenStreetMap-tason kartalle
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);
    } else {
        // Päivitä olemassa olevan kartan näkymä
        map.setView([lat, lon], zoom);
    }
}



async function main() {
    //päöfunktio sen takia että await avainsanaa voidaan käyttää vain async-funktioiden sisällä


    //haetaan pelin tiedot taustapoalvelimelta
    await fetch("api/get-saved-game")
        .then(function (response) {
            // Tarkistetaan, että pyyntö onnistui (status 200)
            if (!response.ok) {
                console.log("Virhe pyyntöä tehdessä");
                throw new Error('Verkkovirhe tai API ei vastannut oikein');
            }
            // Palautetaan JSON-vastaus
            return response.json();
        })
        .then(function (data) { //data haettu onnistuneesti
            pelintiedot = data;


        })
        .catch(function (error) {
           alert('Virhe haettaessa pelin tietoja:', error);
        });


    let endpoint = '/api/getairport';  // Flaskin API-reitti
    let maanosa = pelintiedot["continent"];  //haetaan pelin tiedoista maanosa
    let maa = pelintiedot["country"];  //haetaan pelin tiedoista maa


    await aseta_kartan_aloituspaikka(maa); //asetetaan kartan aloituspaikka




    //selvitetään kuka pelaaja on pelivuorossa, luodaan siitä pelaaja objekti
    for (let i =0;i<pelintiedot["players"].length;i++){
        if (pelintiedot["players"][i]["airport_counter"] < 5)
        {
            pelaaja["name"] = pelintiedot["players"][i]["name"];
            pelaaja["score"] = pelintiedot["players"][i]["score"];
            pelaaja["airport_counter"] = pelintiedot["players"][i]["airport_counter"];
            break;
        }
    }

    //päivitetään pelaajan nimi html sivulle
    pelaajan_nimi_elementti.textContent = "Pelaaja: "+ pelaaja["name"];


    //päivitetään kierros html sivulle
    kierros_elementti.textContent = "Kierros: "+ (pelaaja["airport_counter"]+1) + "/5";

    // Rakennetaan endpoint URL query-parametreilla
    endpoint = endpoint + "?continent=" + maanosa + "&country=" + maa;

    // Varmistetaan, että URL on oikein enkoodattu
    endpoint = encodeURI(endpoint);


    //Haetaan lentokenttä Flaskin API:sta
    fetch(endpoint)
        .then(function (response) {
            // Tarkistetaan, että pyyntö onnistui (status 200)
            if (!response.ok) {
                console.log("Virhe pyyntöä tehdessä");
                throw new Error('Verkkovirhe tai API ei vastannut oikein');
            }
            // Palautetaan JSON-vastaus
            return response.json();
        })
        .then(function (data) {
            // Käsitellään JSON-vastaus
            console.log(data);  // Tulostetaan JSON-objekti konsoliin

            // Otetaan lentokentän tiedot vastausobjektista
            lentokentta = data.airport;  // Lentokenttä, joka saatiin Flaskista
            lentokentanNimi = lentokentta.airport;  // Lentokentän nimi
            lentokentanLatitude = lentokentta.latitude_deg;  // Lentokentän leveysaste
            lentokentanLongitude = lentokentta.longitude_deg;  // Lentokentän pituusaste

            // Tulostetaan tiedot konsoliin
            console.log("Lentokentän nimi:", lentokentanNimi);
            console.log("Leveysaste:", lentokentanLatitude);
            console.log("Pituusaste:", lentokentanLongitude);

            // Päivitä HTML:n <h1> elementti lentokentan nimellä
            document.getElementById('ohje').textContent = "Arvaa missä: " + lentokentanNimi + " lentokenttä sijaitsee.";

        })
        .catch(function (error) {
            // Käsitellään virheet, jos pyyntö epäonnistui
            alert('Virhe haettaessa lentokenttää:', error);
        });


    //käynnistetään ajastin
    startTimer();



    map.on('click', function (event) {   // Lisää kuuntelija kartan klikille
        // Jos "Arvaa"-nappia ei ole painettu
        if (!arvaaClicked) {
            // Koordinaatit kartan klikattaessa
            let lat = event.latlng.lat; // Leveysaste
            let lng = event.latlng.lng; // Pituusaste


            // Tallenna klikkipiste muistiin
            clickLatLng = [lat, lng];

            // Jos edellinen merkki on olemassa, poista se
            if (currentMarker) {
                map.removeLayer(currentMarker);
            }

            // Lisää uusi merkki painalluksen kohtaan
            currentMarker = L.marker([lat, lng]).addTo(map)
        }
    });

    // Lisää tapahtumakäsittelijä "Arvaa"-nappiin
    arvaa_nappi.addEventListener('click', async function () {
        // Tarkistetaan, onko kartalle jo klikattu
        if (!clickLatLng) {
            alert("Klikkaa karttaa ennen arvaamista!");
            return; // Estetään napin toiminta, jos kartalle ei ole vielä klikattu
        }

        stopTimer(); //pysäytetään ajastin

        // Poistetaan "Arvaa"-nappi käytöstä, jotta sitä ei voi painaa uudelleen
        this.disabled = true;
        this.textContent = 'Arvattu!'; // Vaihdetaan napin teksti

        // Piirtoviivan pisteet, jotka sisältävät klikkipisteen ja toisen paikan (esimerkiksi Helsinki)
        let points = [
            clickLatLng, // Klikattu piste
            [lentokentanLatitude, lentokentanLongitude]  // Arvottu lentokenttä
        ];

        // Lentokentän markkeri
        L.marker([lentokentanLatitude, lentokentanLongitude])
            .addTo(map)


        // Viivan lisääminen karttaan
        L.polyline(points, {color: 'red'}).addTo(map);


        // Etäisyyden laskeminen
        let clickPoint = L.latLng(clickLatLng); // Klikattu piste
        let airportPoint = L.latLng([lentokentanLatitude, lentokentanLongitude]); // Lentokenttä

        let distanceInMeters = clickPoint.distanceTo(airportPoint); // Etäisyys metreinä
        let distanceInKilometers = (distanceInMeters / 1000).toFixed(0); // Etäisyys kilometreinä, pyöristetty kahteen desimaaliin



        // Estetään merkkiä liikkumasta napin painamisen jälkeen
        if (currentMarker) {
            currentMarker.dragging.disable(); // Estetään merkkiä liikuttamasta
        }




        //lasketaan pisteet 0-100

        let score = 0;
        if (pelintiedot["country"] =="*") {
            //jos maa on kaikki maat
            score = (1000 - distanceInKilometers)/10;

        }
        else {
            //jos maa on tietty maa kilometriraja on tiukempi
            score = (200 - distanceInKilometers)/2;

        }
        if (score < 0) { //pisteet ei voi mennä negatiiviseksi
            score = 0;
        }

        //pyöristetään pisteet kokonaisluvuksi
        score = Math.round(score);

        pelaaja["score"] = pelaaja["score"] + score; //päivitetään pelaajan pisteet
        pelaaja["airport_counter"] = pelaaja["airport_counter"] + 1; //päivitetään pelaajan lentokenttä laskuri


        //päivitetään pisteet ja etäisyys html sivulle
        document.getElementById('etäisyys').textContent = "Etäisyys lentokentälle: " + distanceInKilometers + " kilometriä.";
        document.getElementById('pisteet').textContent = "Pisteet: " + score + " pistettä.";


        tallennatiedot(); //tallennetaan pelin tiedot taustapalvelimelle


        // Merkitään, että "Arvaa"-nappia on painettu
        arvaaClicked = true;



    });


    //seuraava nappin tapahtumakuuntelija
    seuraava_nappi.addEventListener('click', function () {

        if (kaikki_pelaajat_pelannut==true) //jos kaikki pelaajat ovat pelanneet 5 kertaa
        {
            console.log("kaikki pelaajat pelanneet 5 kertaa");
            window.location.href = "/pelikohtainen-pistetilasto.html"; //siirrytään  pistetilastoon
        }
        else {
            window.location.reload(); //muuten refreshataan sivu
        }
    });
}

// Kutsutaan main-funktiota
main();