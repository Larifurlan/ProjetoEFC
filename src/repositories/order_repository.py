import json
from typing import Any, cast

from src.database.connection import DatabaseConnection
from src.domain import DbOrderRow, OrderItem, OrderRecord
from src.repositories.interfaces.order_repository_interface import (
    OrderRepositoryInterface,
)


class OrderRepository(OrderRepositoryInterface):
    def __init__(self) -> None:
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
        client_name: str,
        items: list[OrderItem],
        total: float,
        status: str,
        date: str,
        customer_type: str,
    ) -> int:
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

        order_id = self.cursor.lastrowid
        if order_id is None:
            raise RuntimeError("Pedido salvo sem id gerado pelo banco.")

        return order_id

    def get_order_by_id(self, order_id: int) -> OrderRecord | None:
        self.cursor.execute(
            "SELECT * FROM ped WHERE id = ?",
            (order_id,),
        )

        result = cast(DbOrderRow | None, self.cursor.fetchone())

        if not result:
            return None

        items = cast(list[OrderItem], json.loads(result[2]))

        return {
            "id": result[0],
            "cli": result[1],
            "itens": items,
            "tot": float(result[3]),
            "st": result[4],
            "dt": result[5],
            "tp": result[6],
        }

    def update_status(self, order_id: int, status: str) -> None:
        self.cursor.execute(
            "UPDATE ped SET st = ? WHERE id = ?",
            (status, order_id),
        )

        self.db.commit()

    def get_orders_by_client(self, client_name: str) -> list[DbOrderRow]:
        self.cursor.execute(
            "SELECT * FROM ped WHERE cli = ?",
            (client_name,),
        )

        return self._rows_to_orders(self.cursor.fetchall())

    def get_all_orders(self) -> list[DbOrderRow]:
        self.cursor.execute("SELECT * FROM ped")
        return self._rows_to_orders(self.cursor.fetchall())

    def close(self) -> None:
        self.db.close()

    def _rows_to_orders(self, rows: list[Any]) -> list[DbOrderRow]:
        return [cast(DbOrderRow, row) for row in rows]
