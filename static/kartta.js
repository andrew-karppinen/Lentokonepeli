
    // Globaaliin scopeen määritellään muuttujat
    let lentokentta, lentokentanNimi, lentokentanLatitude, lentokentanLongitude;

    // Luo kartta ja määritä aloituspaikka ja zoom-taso
    let map = L.map('map').setView([45.733, 3.167], 2); // Esimerkiksi Helsinki

    // Lisää OpenStreetMap-tason kartalle
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Muuttuja edellisen merkin ja klikkipisteen tallentamiseen
    let currentMarker = null;
    let clickLatLng = null;
    let arvaaClicked = false; // Tarkistaa, onko "Arvaa" painettu


    let endpoint = '/api/getairport';  // Flaskin API-reitti
    let maanosa = "*";  // Koko maailma
    let maa = "*";  // Koko

    // Rakennetaan endpoint URL query-parametreilla
    endpoint = endpoint + "?continent=" + maanosa + "&country=" + maa;

    // Varmistetaan, että URL on oikein enkoodattu
    endpoint = encodeURI(endpoint);

    // Tehdään fetch-pyyntö Flaskin API:iin
    fetch(endpoint)
        .then(function(response) {
            // Tarkistetaan, että pyyntö onnistui (status 200)
            if (!response.ok) {
                console.log("Virhe pyyntöä tehdessä");
                throw new Error('Verkkovirhe tai API ei vastannut oikein');
            }
            // Palautetaan JSON-vastaus
            return response.json();
        })
        .then(function(data) {
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
        .catch(function(error) {
            // Käsitellään virheet, jos pyyntö epäonnistui
            console.log('Virhe haettaessa lentokenttää:', error);
        });


    // Lisää kuuntelija kartan klikille
    map.on('click', function(event) {
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
    document.getElementById('arvaa').addEventListener('click', function() {
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

        // Merkitään, että "Arvaa"-nappia on painettu
        arvaaClicked = true;
    });

    // Refreshataan sivu
    document.getElementById('seuraava').addEventListener('click', function() {
        location.reload();
    });