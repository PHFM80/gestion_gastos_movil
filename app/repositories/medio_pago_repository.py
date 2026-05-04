import sqlite3

from app.database import get_connection
from app.models.medio_pago import MedioPago


class MedioPagoRepository:
    def __init__(self, connection: sqlite3.Connection | None = None):
        self._connection = connection or get_connection()

    def create(self, medio_pago: MedioPago) -> MedioPago:
        cursor = self._connection.cursor()
        cursor.execute(
            """
            INSERT INTO medios_pago (nombre)
            VALUES (?)
            """,
            (medio_pago.nombre,),
        )
        self._connection.commit()
        return MedioPago(id=cursor.lastrowid, nombre=medio_pago.nombre)

    def list_all(self) -> list[MedioPago]:
        cursor = self._connection.cursor()
        cursor.execute("SELECT id, nombre FROM medios_pago ORDER BY nombre")
        rows = cursor.fetchall()
        return [self._map_row(row) for row in rows]

    def get_by_id(self, medio_pago_id: int) -> MedioPago | None:
        cursor = self._connection.cursor()
        cursor.execute("SELECT id, nombre FROM medios_pago WHERE id = ?", (medio_pago_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return self._map_row(row)

    @staticmethod
    def _map_row(row: sqlite3.Row) -> MedioPago:
        return MedioPago(id=int(row["id"]), nombre=str(row["nombre"]))
