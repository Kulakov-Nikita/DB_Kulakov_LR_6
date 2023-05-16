# Получить информацию об автомобиле с информацией о модели
def getCarAndModelInfo(dbConnection):
    dbCursor=dbConnection.cursor()
    query = """
        SELECT Car.Mileage, Car.Complectation, Model.Name, Model.Year
        FROM Car
        INNER JOIN Model
        ON Car.Model_ID = Model.Model_ID;
    """
    dbCursor.execute(query)
    for data in dbCursor:
        print(data)

    dbCursor.close()

# Получить информацию о производителе
def getManufacturerInfo(dbConnection):
    dbCursor=dbConnection.cursor()
    query = """
        SELECT Name, Adress, PhoneNumber
        FROM Manufacturer
    """
    dbCursor.execute(query)
    for data in dbCursor:
        print(data)

    dbCursor.close()


# Добавить отзыв
def addReview(dbConnection):
    dbCursor=dbConnection.cursor()

    # Получаем данные
    reviewGrade=int(input("Grade: "))
    reviewComment=input("Comment: ")
    reviewUser=int(input("User_ID: "))
    review=(reviewGrade,reviewComment,reviewUser)

    query = """
        INSERT INTO Review (Grade,Comment,User_ID) VALUES ('%d','%s','%d');
    """
    dbCursor.execute(query % review)
    dbConnection.commit()

    # Проверяем, что данные были добавленны
    check="SELECT * FROM Review WHERE User_ID = '%d';"
    dbCursor.execute(check % reviewUser)
    for data in dbCursor:
        print(data)

    dbCursor.close()

# Добавить клиента
def addUser(dbConnection):
    dbCursor=dbConnection.cursor()

    # Получаем данные
    userLogin=input("Login: ")
    userPhone=int(input("Phone: "))
    user=(userLogin,userPhone)

    query = """
        INSERT INTO User (Login, PhoneNumber) VALUES ('%s','%d');
    """
    dbCursor.execute(query % user)
    dbConnection.commit()

    # Проверяем, что данные были добавленны
    check="SELECT * FROM User WHERE Login = '%s';"
    dbCursor.execute(check % userLogin)
    for data in dbCursor:
        print(data)

    dbCursor.close()

# Изменить название услуги
def changeServiceName(dbConnection):
    dbCursor=dbConnection.cursor()

    # Получить от пользователя id услуги, название которой он хочет изменить
    serviceID = int(input("Service_ID: "))

    doesItExist="SELECT ID FROM Service WHERE ID = '%d';"
    dbCursor.execute(doesItExist % serviceID)
    result = dbCursor.fetchone()

    if result:
        newName = input("New Service Name: ")
        query="""
            UPDATE mydb.Service 
            SET mydb.Service.Name = '%s'
            WHERE mydb.Service.ID = %d;
        """
        newData=(newName,serviceID)
        dbCursor.execute(query % newData)
        dbConnection.commit()

        # Проверяем, что данные были обновлены
        check="SELECT * FROM Service WHERE ID = %d;"
        dbCursor.execute(check % serviceID)
        for data in dbCursor:
            print(data)
    else:
        print("The service isn't found")

    dbCursor.close()

# Изменить телефон работника
def changeWorkerPhone(dbConnection):
    dbCursor=dbConnection.cursor()

    # Получить от пользователя id работника, номер которого он хочет изменить
    WorkerID = int(input("Worker_ID: "))

    doesItExist="SELECT ID FROM Worker WHERE ID = %d;"
    dbCursor.execute(doesItExist % WorkerID)
    result = dbCursor.fetchone()

    if result:
        newPhone = int(input("New Phone: "))
        query="""
            UPDATE mydb.Worker 
            SET mydb.Worker.PhoneNumber = %d
            WHERE mydb.Worker.ID = %d;
        """
        newData=(newPhone,WorkerID)
        dbCursor.execute(query % newData)
        dbConnection.commit()

        # Проверяем, что данные были обновлены
        check="SELECT * FROM Worker WHERE ID = %d;"
        dbCursor.execute(check % WorkerID)
        for data in dbCursor:
            print(data)
    else:
        print("The worker isn't found")

    dbCursor.close()

# Удалить комментарий
def deleteReview(dbConnection):
    dbCursor=dbConnection.cursor()

    grade = int(input("Grade: "))

    # Проверить есть ли хоть один комментарий с такой оценкой
    doesItExist = "SELECT * FROM Review WHERE Grade = '%d';"
    dbCursor.execute(doesItExist % grade)
    result = dbCursor.fetchone()

    if result:
        query="DELETE FROM Review WHERE Grade = '%d';"
        dbCursor.execute(query % grade)
        dbConnection.commit()

        # Проверяем, что деталь была удалена
        check="SELECT * FROM Review WHERE Grade = %d;"
        dbCursor.execute(check % grade)
        for data in dbCursor:
            print(data)

    else:
        print("The Review doesn't exist")

    dbCursor.close()

# Удалить автомобиль
def deleteCar(dbConnection):
    dbCursor=dbConnection.cursor()

    VIN = int(input("VIN: "))

    # Проверить есть ли машина с таким VIN-номером
    doesItExist = "SELECT * FROM Car WHERE VIN = '%d';"
    dbCursor.execute(doesItExist % VIN)
    result = dbCursor.fetchone()

    if result:
        # Удаляем все записи из таблицы 'Follow' соответсвующие введённому VIN-номеру
        query="DELETE FROM Follow WHERE Car = '%d';"
        dbCursor.execute(query % VIN)
        dbConnection.commit()

        # Удаляем все записи из таблицы 'Car' соответсвующие введённому VIN-номеру
        query="DELETE FROM Car WHERE VIN = '%d';"
        dbCursor.execute(query % VIN)
        dbConnection.commit()

        # Проверяем, что деталь была удалена
        check="SELECT * FROM Car WHERE VIN = '%d';"
        dbCursor.execute(check % VIN)
        for data in dbCursor:
            print(data)

    else:
        print("The Car doesn't exist")

    dbCursor.close()

# Подобрать деталь, соответствующую данной модели автомобиля
def findDetailToModel(dbConnection):
    dbCursor=dbConnection.cursor()

    modelName=input("Model Name: ")

    query="""
        SELECT Detail.Name, Detail.Coast 
        FROM Detail 
        WHERE Detail_ID IN 
            (
            SELECT Detail_ID 
            FROM Corresponds 
            WHERE Model_ID IN 
                (
                SELECT Model_ID 
                FROM Model 
                WHERE Name='%s'
                )
            ); 
    """
    dbCursor.execute(query % modelName)
    for data in dbCursor:
        print(data)

    dbCursor.close()

# Найти все автомобили данной модели, с пробегом в заданном диапозоне
def findCarsToModel(dbConnection):
    dbCursor=dbConnection.cursor()

    modelName=input("Model Name: ")
    minMileage=int(input("Mileage min: "))
    maxMileage=int(input("Mileage max: "))

    query="""
       SELECT Mileage, Cost, Complectation
       FROM Car 
       WHERE Model_ID = (
            SELECT Model_ID
            FROM Model
            WHERE Name = '%s')
       AND Mileage BETWEEN '%d' AND '%d';
       
    """
    dbCursor.execute(query % (modelName,minMileage,maxMileage))

    for data in dbCursor:
        print(data)

    dbCursor.close()