import mysql.connector


class Database:
    def __init__(self):
        # Run: `sudo lsof -i -P | grep -i mysqld` to check current running of mysql port
        config = {
            'user': 'root',
            'password': '12354',
            'host': '127.0.0.1',
            'port': '3307',
            'database': 'ruppthesis',
            'use_pure': False
        }
        self.connection = mysql.connector.connect(**config)
        self.cursor = self.connection.cursor()

    def execute(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    def execute_query(self, query):
        self.cursor.execute(
            query
        )

        # gets the number of rows affected by the command executed
        return self.cursor.fetchone()
