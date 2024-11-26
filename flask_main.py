
from flask import Flask, request, jsonify, render_template
import mysql.connector

from src.maanosakoodit import *
from src import *

#luodaan sql yhteys
yhteys = mysql.connector.connect(
    host="localhost",
    port=3306,
    database='flight_game',
    user="sqlkayttaja",
    password="salasana123",
    connection_timeout=5,
    autocommit=True)


app = Flask(__name__)


####sivusto:
@app.route('/')
def index():
    return render_template('etusivu.html')



####api:


@app.route('/api/calculate_distance', methods=['get'])
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
    etaisyys = hae_etaisyys(yhteys, airport_name, sijainti) #haetaan etäisyys tietokannasta
    if etaisyys == False:
        return jsonify({"error": "Airport not found"})

    return jsonify({"distance": etaisyys})

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
    pass


@app.route('/api/new-game', methods=['POST'])
def new_game():
    pass



@app.route('/api/get-saved-game', methods=['GET'])
def get_saved_game():
    pass

@app.route('/api/save-game', methods=['POST'])
def save_game():
    pass


if __name__ == '__main__':
    app.run(debug=True, port=5000)


