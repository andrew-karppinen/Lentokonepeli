
from flask import Flask, request, jsonify, render_template
import mysql.connector
from jsonschema import validate, ValidationError

from src import *
import os


#haetaan käyttäjätunnus ja salasana ympäristömuuttujista
kayttajatunnus = os.getenv('sqlkayttaja')
salasana = os.getenv('sqlkayttaja_salasana')



#luodaan sql yhteys
yhteys = mysql.connector.connect(
    host="localhost",
    port=3306,
    database='flight_game',
    user=kayttajatunnus,
    password=salasana,
    connection_timeout=5,
    autocommit=True)

app = Flask(__name__)


####sivusto:
@app.route('/')
def index_html():
    return render_template('etusivu.html')


@app.route('/pisteet.html')
def pisteet_html():
    return render_template('pisteet.html')

@app.route('/uusipeli.html')
def pelaajat_html():
    return render_template('uusipeli.html')


@app.route('/jatketaanko.html')
def uusi_peli_html():
    return render_template('jatketaanko.html')

####api:


@app.route('/api/calculate-distance', methods=['get'])
def calculate_distance():
    '''
    Laskee kahden lentokentän välisen etäisyyden
    '''

    latitude_deg = request.args.get('latitude_deg')
    longitude_deg = request.args.get('longitude_deg')
    airport_name = request.args.get('airport_name')

    if latitude_deg == None or latitude_deg == "" or longitude_deg == None or longitude_deg == "" or airport_name == None or airport_name == "":
        return jsonify({"error": "Missing parameters"})

    sijainti = (latitude_deg, longitude_deg)
    etaisyys,sijanti = hae_etaisyys(yhteys, airport_name, sijainti) #haetaan etäisyys tietokannasta
    if etaisyys == False:
        return jsonify({"error": "Airport not found"})

    return jsonify({"distance": etaisyys,"airport_location": sijanti})

@app.route('/api/getcontinents', methods=['get'])
def get_continents():
    '''
    Palauttaa maanosakoodit
    '''

    koodit = ["NA", "OC", "AF", "AN", "EU", "AS", "SA", "*"] #maanosakoodit

    vastaus = {
        "continents": koodit
    }
    return jsonify(vastaus)


@app.route('/api/getcountries', methods=['GET'])
def get_countries():
    '''
    Palauttaa maanosan maat
    '''

    continent = request.args.get('continent')

    if continent == None or continent == "": #ei annettua maanosaa
        continent = "*"

    maat = hae_maat(yhteys,continent) #haetaan maat tietokannasta
    vastaus = {
        "countries": maat
    }
    return jsonify(vastaus)


@app.route('/api/getairport', methods=['GET'])
def get_airport():
    '''
    Palauttaa satunnaisen lentokentän
    annettujen parametrien mukaan
    '''

    continent = request.args.get('continent')
    country = request.args.get('country')

    if continent == None or continent == "": #ei annettua maanosaa
        continent = "*"
    if country == None or country == "": #ei annettua maata
        country = "*"

    lentokentta = arpominen(yhteys,continent,country) #haetaan lentokenttä tietokannasta
    vastaus = {
        "airport": lentokentta
    }
    return jsonify(vastaus)

@app.route('/api/get-user-scores', methods=['GET'])
def get_user_scores():

    return jsonify(hae_pelaajatiedot(yhteys))





@app.route('/api/get-saved-game', methods=['GET'])
def get_saved_game():

    return jsonify(hae_keskeneräisen_pelin_tiedot(yhteys))


@app.route('/api/new-game', methods=['POST'])
def new_game():
    gamedata = request.json.get('gamedata')
    print(gamedata)
    if gamedata == None:
        return jsonify({"error": "Missing parameters"}),400

    schema = {
        "type": "object",
        "properties": {
            "continent": {"type": ["string", "null"]},
            "country": {"type": ["string", "null"]},
            "players": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "airport_counter": {"type": "integer"},
                        "score": {"type": "integer"}
                    },
                    "required": ["name", "airport_counter", "score"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["continent", "country","players"],
        "additionalProperties": False
    }

    try:
        validate(instance=gamedata, schema=schema) #tarkistetaan parametrinä saadun datan oikeellisuus
    except ValidationError as e:
        print("validation error")
        return jsonify({"error": "Invalid parameters"}), 400

    uusi_peli(yhteys, gamedata)
    return jsonify({"status": "success"}), 201

@app.route('/api/save-game', methods=['POST'])
def save_game():
    gamedata = request.json.get('gamedata')

    if gamedata == None:
        return jsonify({"error": "Missing parameters"})

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "players": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "airport_counter": {"type": "integer"},
                        "score": {"type": "integer"}
                    },
                    "required": ["name", "airport_counter", "score"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["players"],
        "additionalProperties": False
    }


    try:
        validate(instance=gamedata, schema=schema) #tarkistetaan parametrinä saadun datan oikeellisuus
    except ValidationError as e:
        return jsonify({"error": "Invalid parameters"})

    if tallenna_keskeneraisen_pelin_tiedot(yhteys, gamedata) == False:
        return jsonify({"error": "Error saving game"})
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)


