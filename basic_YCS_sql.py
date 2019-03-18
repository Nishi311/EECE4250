import mysql.connector

mydb = mysql.connector.connect(
  host="yuppie-city-simulator-db.cohu57vlr7rd.us-east-2.rds.amazonaws.com",
  user="MeanderingArma",
  passwd="Dillos1999",
  database="YCS"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM city_index")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)
