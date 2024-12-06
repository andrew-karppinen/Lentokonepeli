








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

async function aseta_kartan_aloituspaikka(maa) {
    /*
    Asettaa kartan aloituspaikan ja zoom-tason maan perusteella
    */

    let lat = 0, lon = 0, zoom = 4; // Koko maapallon oletuskoordinaatit ja zoom

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



    let pelaaja = {"name": "", "score": 0, "airport_counter": 0}; //alustetaan pelaaja objekti

    //selitetään kuka pelaaja on pelivuorossa, luodaan siitä pelaaja objekti
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



    // Tehdään fetch-pyyntö Flaskin API:iin
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


    // Lisää kuuntelija kartan klikille
    map.on('click', function (event) {
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
    document.getElementById('arvaa').addEventListener('click', async function () {
        // Tarkistetaan, onko kartalle jo klikattu
        if (!clickLatLng) {
            alert("Klikkaa karttaa ennen arvaamista!");
            return; // Estetään napin toiminta, jos kartalle ei ole vielä klikattu
        }

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

        // Näytetään etäisyys kilometreinä
        document.getElementById('etäisyys').textContent = "Etäisyys lentokentälle: " + distanceInKilometers + " kilometriä.";

        // Estetään merkkiä liikkumasta napin painamisen jälkeen
        if (currentMarker) {
            currentMarker.dragging.disable(); // Estetään merkkiä liikuttamasta
        }




        //lasketaan pisteet 0-100


        let score = 0;
        if (pelintiedot["country"] =="*") {
            //jos maa on kaikki maat
            score = 1000 - distanceInKilometers/10;

        }
        else {
            //jos maa on tietty maa kilometriraja on tiukempi
            score = 500 - distanceInKilometers/5;

        }
        if (score < 0) { //pisteet ei voi mennä negatiiviseksi
            score = 0;
        }
        
        //pyöristetään pisteet kokonaisluvuksi
        score = Math.round(score);

        pelaaja["score"] = pelaaja["score"] + score; //päivitetään pelaajan pisteet
        pelaaja["airport_counter"] = pelaaja["airport_counter"] + 1; //päivitetään pelaajan lentokenttä laskuri


        let kaikki_pelaajat_pelannut = true; //tarkistetaan onko kaikki pelaajat pelanneet
        for (let i =0;i<pelintiedot["players"].length;i++){ //käydään läpi kaikki pelaajat

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



        //tallennetaan pelin tiedot taustapalvelimelle

        tallennettava_data = {"gamedata":
            {
                "players": pelintiedot["players"]
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



        // Merkitään, että "Arvaa"-nappia on painettu
        arvaaClicked = true;


        if (kaikki_pelaajat_pelannut==true) //jos kaikki pelaajat ovat pelanneet 5 kertaa
        {
            console.log("kaikki pelaajat pelanneet 5 kertaa");
            window.location.href = "/pelikohtainen-pistetilasto.html"; //siirrytään  pistetilastoon
        }


    });


    // Refreshataan sivu
    document.getElementById('seuraava').addEventListener('click', function () {
        location.reload();
    });
}

// Kutsutaan main-funktiota
main();