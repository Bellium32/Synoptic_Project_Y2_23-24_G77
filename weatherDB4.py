import mysql.connector
################Guide to establishing the connection##########################
#Have SQL Workbench, Installer, and Shell instealled on the device
#Have python and it's dependencies installed, if using VS studio install "MySQL Shell for VS Code"
#To establish the connection, press "Windows key + R", them type in "cmd"
#Type in: cd "C:\Users\emman\AppData\Local\Programs\Python\Python312\Scripts"
#If this doesn't work: cd "C:\Users\*yourusername*\AppData\Local\Programs\Python\" and find scripts from there
#Then copy in: pip install mysql-connector-python |or| python -m pip install mysql-connector-python

 
databaseExist = True
#If a database exists set this to true, if one doesn't, set to false and run to create the database
#After that run the create table function to create the tables of the database
global mydb
global databaseRECORD
if databaseExist == False:
    
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pass"
    )
    mycursor = mydb.cursor(buffered=True)
    mycursor2 = mydb.cursor()
    mycursor.execute("CREATE DATABASE weatherdb4")

else:
    #Connects the codebase to the database using this authentication
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pass",
    database="weatherdb4"
    )
    
    #Creates a cursor object that allows us to pass commands to the database
    mycursor = mydb.cursor(buffered=True)
    mycursor2 = mydb.cursor()
    databaseRECORD = False
def my_Tables_Create():
    #SQL commands to create tables
    
    mycursor.execute("CREATE TABLE weatherInfo (wDataId INT AUTO_INCREMENT PRIMARY KEY, dt INT, "
                     "temp FLOAT(24), feels_like FLOAT(24), temp_min FLOAT(24), "
                     "temp_max FLOAT(24), pressure INT, sea_level INT, grnd_level INT, humidity INT, temp_kf FLOAT(24), "
                     "weather_id INT, weather_main VARCHAR(25), weather_description VARCHAR(50), weather_icon VARCHAR(10), "
                     "clouds_all INT, wind_speed FLOAT(24), wind_deg INT, wind_gust FLOAT(24), visibility INT, pop FLOAT, "
                     "rain_3h FLOAT(24), sys_pod VARCHAR(5), dt_txt DATETIME, location VARCHAR(5))")
    
    
    mycursor.execute("CREATE TABLE weatherDay (wDayId INT AUTO_INCREMENT PRIMARY KEY, weatherData INT, location VARCHAR(5), day VARCHAR(10), date DATE, "
                     "FOREIGN KEY (weatherData) REFERENCES weatherInfo(wDataId))")
    mycursor.execute("CREATE TABLE weatherHour (wHourId INT AUTO_INCREMENT PRIMARY KEY, weatherData INT, location VARCHAR(5), hour TIME, date DATE, "
                     "FOREIGN KEY (weatherData) REFERENCES weatherInfo(wDataId))")
    mycursor.execute("CREATE TABLE people (peopleId INT AUTO_INCREMENT PRIMARY KEY, fname VARCHAR(255), lname VARCHAR(255), phoneNumber VARCHAR(15))")
                     
    
    
    
  


def my_Tables_Drop():
    #SQL commands to delete (drop) all tables
    mycursor.execute("DROP TABLE IF EXISTS weatherDay")
    mycursor.execute("DROP TABLE IF EXISTS weatherHour")
    mycursor.execute("DROP TABLE IF EXISTS people")
    mycursor.execute("DROP TABLE IF EXISTS weatherInfo")

    
def my_Tables_Truncate():
    mycursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    mycursor.execute("TRUNCATE TABLE weatherInfo")
    mycursor.execute("TRUNCATE TABLE weatherDay")
    mycursor.execute("TRUNCATE TABLE weatherHour")
    mycursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    
   

   
createAndDrop = 0
if createAndDrop == 1:
    print("Free space")
if createAndDrop == 2:
    my_Tables_Create()
    
if createAndDrop == 97:
    my_Tables_Truncate()
    
if createAndDrop == 98:
    mycursor.execute("DROP DATABASE weatherdb2")

if createAndDrop == 99:
    my_Tables_Drop()
    
def my_Day_Insert(location, day, date, weatherData):
    #Inserts data into the database, just pass the arguments into the commands 
    #So location = location etc
    sql = "INSERT INTO weatherDay (location, day, date, weatherData) VALUES (%s, %s, %s, %s)"
    values = (location, day, date, weatherData)
    #values not only makes it easier to pass information from parameters
    #But also escapes the values to prevent sql injection
    mycursor.execute(sql, values)
    #Commits the changes into the database
    mydb.commit()
    #Tells user if records where inserted
    if databaseRECORD == True:
        print(mycursor.rowcount, "record inserted.")

def my_Hour_Insert(location, hour, date, weatherData):
    sql = "INSERT INTO weatherHour (location, hour, date, weatherData) VALUES (%s, %s, %s, %s)"
    values = (location, hour, date, weatherData)
    mycursor.execute(sql, values)
    mydb.commit()
    if databaseRECORD == True:
        print(mycursor.rowcount, "record inserted.")
    
def my_people_Insert(fname, lname, phoneNumber):
    sql = "INSERT INTO people (fname, lname, phoneNumber) VALUES (%s, %s, %s)"
    values = (fname, lname, phoneNumber)
    mycursor.execute(sql, values)
    mydb.commit()
    if databaseRECORD == True:
        print(mycursor.rowcount, "record inserted.")

def my_Day_Select_Check(dataL, dataD):
    #Finds the data from within the database that matches the parameters
    sql = "SELECT * FROM weatherDay WHERE location = %s AND date = %s"
    values = (dataL, dataD, ) 
    mycursor.execute(sql, values)
    #Fetches all results that matches the query
    myresult = mycursor.fetchall()
    if myresult == []:      
        return False
    return True

def my_Day_Select_WeatherID(dataL, dataD):
    #Finds the data from within the database that matches the parameters
    sql = "SELECT weatherData FROM weatherDay WHERE location = %s AND date = %s"
    values = (dataL, dataD, ) 
    mycursor.execute(sql, values)
    #Fetches all results that matches the query
    myresult = mycursor.fetchone()
    # if myresult == []:
    #     print("nuh uh")
    #     return False
    #Prints all results that matches the query
    # for p in myresult:
    #     print(p)
    return myresult

def my_Hour_Select_Check(dataL, dataD, dataH):
    sql = "SELECT * FROM weatherHour WHERE location = %s AND date = %s AND hour = %s"
    values = (dataL, dataD, dataH) 
    mycursor.execute(sql, values)
    myresult = mycursor.fetchall()
    if myresult == []:
        return False
        #print("nuh uh")
    return True

def my_Hour_Select_WeatherID(dataL, dataD, dataH):
    #Finds the data from within the database that matches the parameters
    sql = "SELECT weatherData FROM weatherHour WHERE location = %s AND date = %s AND hour = %s"
    values = (dataL, dataD, dataH) 
    mycursor.execute(sql, values)
    #Fetches all results that matches the query
    myresult = mycursor.fetchone()
    # if myresult == []:
    #     print("nuh uh")
    #     return False
    #Prints all results that matches the query
    # for p in myresult:
    #     print(p)
    return myresult

def my_People_Select(data):
    sql = "SELECT * FROM people WHERE phoneNumber = %s"
    values = (data, ) 
    mycursor.execute(sql, values)
    myresult = mycursor.fetchall()
    if myresult == []:
        print("nuh uh")
        return False
    for p in myresult:
        print(p)

def my_Day_Update_Weather(dataW, dataL, dataD, ):
    #Updates the database for the weatherData on that day + location
    sql = "UPDATE weatherDay SET weatherData = %s WHERE location = %s AND date = %s"
    values = (dataW, dataL, dataD, ) 
    mycursor2.execute(sql, values)
    myresult = mycursor.fetchall()
    # for p in myresult:
    #     print(p)
    mydb.commit()
    if databaseRECORD == True:
        print(mycursor.rowcount, "record(s) affected")    
        
def my_Hour_Update_Weather(dataW, dataL, dataD, dataH, ):
    sql = "UPDATE weatherHour SET weatherData = %s WHERE location = %s AND date = %s AND hour = %s"
    values = (dataW, dataL, dataD, dataH, ) 
    mycursor2.execute(sql, values)
    myresult = mycursor.fetchall()
    # for p in myresult:
    #     print(p)
    mydb.commit()
    if databaseRECORD == True:
        print(mycursor.rowcount, "record(s) affected")  
        
def my_WeatherInfo_Insert(dt, temp, feels_like, temp_min, temp_max, pressure, sea_level, grnd_level, 
                          humidity, temp_kf, weather_id, weather_main, weather_description, weather_icon, 
                          clouds_all, wind_speed, wind_deg, wind_gust, visibility, pop, rain_3h, sys_pod, dt_txt, location):
    sql = """
    INSERT INTO weatherInfo (
        dt, temp, feels_like, temp_min, temp_max, pressure, sea_level, grnd_level, humidity, temp_kf, 
        weather_id, weather_main, weather_description, weather_icon, clouds_all, wind_speed, wind_deg, wind_gust, 
        visibility, pop, rain_3h, sys_pod, dt_txt, location
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (dt, temp, feels_like, temp_min, temp_max, pressure, sea_level, grnd_level, humidity,
              temp_kf, weather_id, weather_main, weather_description, weather_icon, clouds_all,
              wind_speed, wind_deg, wind_gust, visibility, pop, rain_3h, sys_pod, dt_txt, location)
    mycursor.execute(sql, values)
    mydb.commit()
    if databaseRECORD == True:
        print(mycursor.rowcount, "record inserted.")

        
def my_W_Info_Select_WeatherID(dataL, dataDT):
    #Finds the data from within the database that matches the parameters
    sql = "SELECT wDataId FROM weatherInfo WHERE location = %s AND dt_txt = %s"
    values = (dataL, dataDT) 
    mycursor.execute(sql, values)
    #Fetches all results that matches the query
    myresult = mycursor.fetchone()
    if myresult == []:
         print("nuh uh")
    #    return False
    #Prints all results that matches the query
    # for p in myresult:
    #     print(p)
    return myresult

def my_W_All_Select_WeatherID(dataA, dataID):
    #Finds the data from within the database that matches the parameters
    sql = "SELECT * FROM weatherInfo WHERE wDataId = %s"
    values = (dataID, ) 
    mycursor.execute(sql, values)
    #Fetches all results that matches the query
    myresult = mycursor.fetchone()
    if myresult == []:
         print("nuh uh")
    #    return False
    #Prints all results that matches the query
    #25 results
    dataList = []
    for i in myresult:
        dataList.append(i)
        #dataList.append((len[i],i))
        #print(i)
    #print(dataList)
    global dataFound
   
    match dataA:
        case "wDataId":
            return dataList[0]
        case "dt":
            return dataList[1]
        case "temp":
            return dataList[2]
        case "feels_like":
            return dataList[3]
        case "temp_min":
            return dataList[4]
        case "temp_max":
            return dataList[5]
        case "pressure":
            return dataList[6]
        case "sea_level":
            return dataList[7]
        case "grnd_level":
            return dataList[8]
        case "humidity":
            return dataList[9]
        case "temp_kf":
            return dataList[10]
        case "weather_id":
            return dataList[11]
        case "weather_main":
            return dataList[12]
        case "weather_description":
            return dataList[13]
        case "weather_icon":
            return dataList[14]
        case "clouds_all":
            return dataList[15]
        case "wind_speed":
            return dataList[16]
        case "wind_deg":
            return dataList[17]
        case "wind_gust":
            return dataList[18]
        case "visibility":
            return dataList[19]
        case "pop":
            return dataList[20]
        case "rain_3h":
            return dataList[21]
        case "sys_pod":
            return dataList[22]
        case "dt_txt":
            return dataList[23]
        case "location":
            return dataList[24]
        case _:
            return dataList
    # for p in myresult:
    #     print(p)
     
    #return str(myresult[0])
        
if createAndDrop == 3:                   
    my_Day_Insert("PN", "Monday", "2024-06-06", "2114")
    my_Hour_Insert("MO", "09:00", "2024-06-06", "6885")
    my_people_Insert("Timmothy", "Smith", "071411 26345")

if createAndDrop == 4:
    my_Day_Select_WeatherID("PN", '2024-06-13')

if createAndDrop == 5:
    my_Day_Insert("PN", "Tuesday", "2024-06-07", "8442")

if createAndDrop == 6:
    my_Hour_Select_Check("MO", '2024-06-08', "09:00")

if createAndDrop == 7:
    my_People_Select("071411 26345")
    
if createAndDrop == 8:
    my_Day_Update_Weather("4855","PN", "2024-06-06")
    my_Hour_Update_Weather("2008","MO", "2024-06-06", "09:00")

if createAndDrop == 9:
    #my_Day_Select_Check("MO", "Teheehee")
    print("yo")
    
if createAndDrop == 10:
    tempemp = my_W_All_Select_WeatherID("feels_like",7, )
    print(tempemp)


#mycursor.execute("SHOW TABLES")



