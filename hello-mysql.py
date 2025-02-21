from flask import Flask
import mysql.connector
app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, Docker!'
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