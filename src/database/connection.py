import sqlite3


class DatabaseConnection:

    def __init__(self, database_name="loja.db"):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()