import sqlite3


class DatabaseConnection:
    def __init__(self, database_name: str = "loja.db") -> None:
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def commit(self) -> None:
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()
