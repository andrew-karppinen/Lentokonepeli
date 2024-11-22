import mysql.connector



'''
Esimerkki yhteyden muodostamisesta ja yhteysolion viemisestä funktiolle
'''


def maanosakoodit(yhteys:object)->list:
    '''
    Tehdään sql kysely ja palautetaan serveriltä saatu vastaus
    '''

    komento = "SELECT DISTINCT continent from airport;"  #sql komento
    kursori = yhteys.cursor() #luodaan kursori

    kursori.execute(komento) #suoritetaan komento
    tulos = kursori.fetchall()  #haetaan kaikki tulokset

    return [rivi[0] for rivi in tulos]



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
        print(maanosakoodit(yhteys))