import mysql.connector



'''
Esimerkki yhteyden muodostamisesta ja yhteysolion viemisestä funktiolle
'''


def KyselyFunktio(yhteys:object)->list:
    '''
    Tehdään sql kysely ja palautetaan serveriltä saatu vastaus
    '''

    komento = "SELECT * FROM airport;"  #sql komento
    kursori = yhteys.cursor() #luodaan kursori

    kursori.execute(komento) #suoritetaan komento
    tulos = kursori.fetchall()  #haetaan kaikki tulokset

    return tulos



if __name__ == '__main__': #pääohjelma

    try:
        yhteys = mysql.connector.connect(
                 host='127.0.0.1',
                 port= 3306,
                 database='flight_game',
                 user='sqlkayttaja',
                 password='salasana123',
                 autocommit=True
                 )
    except mysql.connector.Error as err: #virhe yhteyden muodostamisessa
        print(err)


    else: #yhteys muodostettu onnistuneesti
        print(KyselyFunktio(yhteys))