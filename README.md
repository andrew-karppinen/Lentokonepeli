 # Airport Quest 

![kuva](https://github.com/user-attachments/assets/782946a5-8984-4d42-a51e-e1d61c4048a9)




Asenna kirjastot:
> pip install mysql-connector-python

> pip install geopy

> pip install jsonschema

Luo tietokanta flight_game 
> create database flight_game

Ota tietokanta käyttöön
> use flight_game

Aja tietokannan luontiskripti joka löytyy:
documentation/create_database_script.sql

aja se:
> source full/path/to/create_database_script.sql

aja ohjelma:  
> python3 flask_main.py

Tämän tulee löytää ympäristömuuttujat:

"flight_game_sql_user" ja "flight_game_sql_user_password"

se olettaa että sql tietokanta löytyy localhostista ja että sen portti on 3306

Kun flask lähtee pyörimään ohjelma toimii selaimessa puhelimella tai tietokoneella, flask kuuntelee porttia 5000

#### Relaatiomalli:
![relaatiomalli](https://github.com/user-attachments/assets/55b5e94e-9df5-449e-8ff7-233718a4ead9)



