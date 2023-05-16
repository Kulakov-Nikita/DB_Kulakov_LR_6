import sys
import mysql.connector
from mysql.connector import Error
import mySQL_Queries

# Соединить приложение и БД
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("\nConnection to MySQL DB successful\n")
    except Error as e:
        print(f"\nThe error '{e}' occurred\n")

    return connection

if __name__ == '__main__':
    # Открыть доступ к БД
    dbConnection = create_connection("localhost", "root", "falcon27685", "mydb")

    print("Доступные запросы к БД:")
    print("[1] Получить информацию об автомобиле с информацией о модели")
    print("[2] Получить информацию о производителе")
    print("[3] Добавить отзыв")
    print("[4] Добавить клиента")
    print("[5] Изменить название услуги")
    print("[6] Изменить телефон работника")
    print("[7] Удалить отзыв")
    print("[8] Удалить автомобиль")
    print("[9] Подобрать деталь, соответствующую данной модели автомобиля")
    print("[10] Найти все автомобили данной модели")

    choise=int(input("Выбирите ваш запрос: "))
    
    while choise < 1 or choise > 10:
         choise=int(input("Запроса с таким номером нет списке. Попробуйте выбрать другой запрос: "))
    
    queriesDict={
        1:mySQL_Queries.getCarAndModelInfo,
        2:mySQL_Queries.getManufacturerInfo,
        3:mySQL_Queries.addReview,
        4:mySQL_Queries.addUser,
        5:mySQL_Queries.changeServiceName,
        6:mySQL_Queries.changeWorkerPhone,
        7:mySQL_Queries.deleteReview,
        8:mySQL_Queries.deleteCar,
        9:mySQL_Queries.findDetailToModel,
        10:mySQL_Queries.findCarsToModel,
        }

    queriesDict.get(choise)(dbConnection)

    # Закрыть доступ к БД
    dbConnection.close()
