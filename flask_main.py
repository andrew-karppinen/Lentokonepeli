
from flask import Flask, request, jsonify, render_template
import mysql.connector

from src.maanosakoodit import maanosakoodit
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

@app.route('/api/getcontinents', methods=['get'])
def get_continents():
    '''
    Palauttaa maanosakoodit
    '''
    koodit = maanosakoodit(yhteys)  #hakee maanosakoodit listaan

    vastaus = {
        "continents": koodit
    }
    return jsonify(vastaus)


@app.route('/api/getcountries', methods=['GET'])
def get_countries():
    '''
    Palauttaa maanosan maat
    '''
    pass



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


