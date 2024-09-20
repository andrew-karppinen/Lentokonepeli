import mysql.connector

from src import * #importataan funktiot




#yhteys
try:
    yhteys = mysql.connector.connect(
        host='127.0.0.1',
        port= 3306,
        database='flight_game',
        user='sqlkayttaja',
        password='salasana123',
        autocommit=True)
except mysql.connector.Error as err: # virhe yhteyden muodostamisessa
    print(err)





print("Maanosat: ", maanosakoodit(yhteys))


print("Pelaa kaikissa maanosissa: * ")
print("Tai anna jokin maanosa")


valinta = input("Valinta: ").upper()

print(arpominen(yhteys,valinta))