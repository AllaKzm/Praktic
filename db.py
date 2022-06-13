import pymysql
import datetime
import mysql
from mysql.connector import connect, Error

class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',
            database='igora',
        )

    def getCLients(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM CLIENTS")
        clients = cursor.fetchall()
        return clients

    def getRequests(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM REQUESTS")
        requests = cursor.fetchall()
        cursor.close()
        return requests

    def insertRequests(self, number_request, date_create, time_request, number_client, services,
                       status_request, rental_time):
        cursor = self.connection.cursor()
        cursor.execute(
            f"INSERT INTO requests"
            f"(`number_request`, `date_create`, `time_request`, `number_client`, `services`, `status_request`, `rental_time`)"
            f"VALUES ('{number_request}', '{date_create}', '{time_request}', '{number_client}', '{services}', '{status_request}', '{rental_time}')"
        )
        cursor.close()
        self.connection.commit()

    def getEmployeers(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM EMPLOYEERS")
        employeers = cursor.fetchall()
        cursor.close()
        return employeers

    def getServices(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM SERVICES")
        services = cursor.fetchall()
        cursor.close()
        return services

    def getHistory(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM History")
        history = cursor.fetchall()
        cursor.close()
        return history

    def check_login(self):
        log = []
        cursor = self.connection.cursor()
        cursor.execute(f"""SELECT login FROM employeers""")
        rows = cursor.fetchall()
        for i in rows:
            for j in i:
                log.append(j)
        return log
        cursor.close()

    def get_log(self, login):
        log = []
        cursor = self.connection.cursor()
        cursor.execute(f"""SELECT password, post FROM employeers WHERE login = '{login}'""")
        rows = cursor.fetchall()
        for i in rows :
            for j in i:
                log.append(j)
        return log
        cursor.close()


if __name__ == '__main__':
    D = Database()
    print(D.get_log('Ivanov@namecomp.ru'))
