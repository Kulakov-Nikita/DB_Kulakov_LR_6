import sys
import mysql.connector
from mysql.connector import Error

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
    dbConnection = create_connection("localhost", "root", "falcon27685", "mydb")
