import pymysql

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
        return requests

    def getEmployeers(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM EMPLOYEERS")
        employeers = cursor.fetchall()
        return employeers

    def getServices(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM SERVICES")
        services = cursor.fetchall()
        return services

    def getHistory(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM EntryHistory")
        history = cursor.fetchall()
        return history

    def get_pas(self, login):
        cursor = self.connection.cursor()
        cursor.execute(f"""SELECT password FROM employeers WHERE login = '{login}'""")
        pas = cursor.fetchone()
        print(pas)
        return pas

    def get_role(self,login):
        cursor = self.connection.cursor()
        cursor.execute(f"""SELECT post FROM employeers WHERE login = '{login}'""")
        pos = cursor.fetchall()
        return pos

if __name__ == '__main__':
    D = Database()
    #D.getEmployeers()
    D.get_pas('Ivanov@namecomp.ru')