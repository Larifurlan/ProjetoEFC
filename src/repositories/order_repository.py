import json

from src.database.connection import DatabaseConnection
from src.repositories.interfaces.order_repository_interface import (
    OrderRepositoryInterface,
)


class OrderRepository(OrderRepositoryInterface):

    def __init__(self):
        self.db = DatabaseConnection()
        self.cursor = self.db.cursor

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ped (
                id INTEGER PRIMARY KEY,
                cli TEXT,
                itens TEXT,
                tot REAL,
                st TEXT,
                dt TEXT,
                tp TEXT
            )
            """
        )

        self.db.commit()

    def save_order(
        self,
        client_name,
        items,
        total,
        status,
        date,
        customer_type
    ):
        items_json = json.dumps(items)

        self.cursor.execute(
            """
            INSERT INTO ped (
                cli,
                itens,
                tot,
                st,
                dt,
                tp
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                client_name,
                items_json,
                total,
                status,
                date,
                customer_type,
            ),
        )

        self.db.commit()

        return self.cursor.lastrowid

    def get_order_by_id(self, order_id):

        self.cursor.execute(
            "SELECT * FROM ped WHERE id = ?",
            (order_id,)
        )

        result = self.cursor.fetchone()

        if not result:
            return None

        return {
            "id": result[0],
            "cli": result[1],
            "itens": json.loads(result[2]),
            "tot": result[3],
            "st": result[4],
            "dt": result[5],
            "tp": result[6],
        }

    def update_status(self, order_id, status):

        self.cursor.execute(
            "UPDATE ped SET st = ? WHERE id = ?",
            (status, order_id)
        )

        self.db.commit()

    def get_orders_by_client(self, client_name):

        self.cursor.execute(
            "SELECT * FROM ped WHERE cli = ?",
            (client_name,)
        )

        return self.cursor.fetchall()

    def get_all_orders(self):

        self.cursor.execute("SELECT * FROM ped")

        return self.cursor.fetchall()

    def close(self):
        self.db.close()