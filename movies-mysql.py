from flask import Flask
import random
import requests
from bs4 import BeautifulSoup
import mysql.connector
app = Flask(__name__)

@app.route('/')
def home():
    URL = 'http://www.icbl.hw.ac.uk/santiago/teaching/F28WP/movies.php'
    response = requests.get(URL)
    results = BeautifulSoup(response.text, 'html.parser')
    all_hrefs = [a.get('href') for a in results.find_all('a')]
    all_texts = [a.text for a in results.find_all('a')]
    myhtml = ''
    for ref in all_hrefs:
        i = all_hrefs.index(ref)
        if not ref is None:
            try:
                title = all_texts.pop(i)
                myhtml = myhtml + "title: " + title + " *** URL: " + ref + "<br>\n"
            except:
                print("Error: Pop index "+str(i)+" out of range")
    return myhtml
@app.route('/initdb')
def db_init():
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1"
    )
    cursor = mydb.cursor()

    #cursor.execute("DROP DATABASE IF EXISTS inventory")
    cursor.execute("CREATE DATABASE IF NOT EXISTS inventory")
    cursor.execute("USE inventory")

    cursor.execute("CREATE TABLE IF NOT EXISTS Courses (code VARCHAR(25), name VARCHAR(255))")
   
    cursor.execute("INSERT INTO Courses VALUES ('F29IP', 'Industrial Project')")
    cursor.execute("INSERT INTO Courses VALUES ('F29AI', 'Artificial Intelligence')")
    cursor.execute("INSERT INTO Courses VALUES ('F29AS', 'Advanced Software Development')")

    cursor.execute("SELECT * FROM Courses")
    result = "<h3>Courses</h3>"
    for row in cursor.fetchall():
        result += row[0]+" - "+row[1]+"<br>"
    
    cursor.close()
    return result

if __name__ == "__main__":
    app.run(host ='0.0.0.0')