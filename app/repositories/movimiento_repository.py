import sqlite3
from datetime import date, datetime
from decimal import Decimal

from app.database import get_connection
from app.models.movimiento import Movimiento
from app.models.tipo_movimiento import TipoMovimiento


class MovimientoRepository:
    def __init__(self, connection: sqlite3.Connection | None = None):
        self._connection = connection or get_connection()

    def create(self, movimiento: Movimiento) -> Movimiento:
        tipo_id = self._get_tipo_id(movimiento.tipo)
        cursor = self._connection.cursor()
        cursor.execute(
            """
            INSERT INTO movimientos (
                tipo_id, fecha, monto, categoria_id, medio_pago_id, detalle
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                tipo_id,
                movimiento.fecha.isoformat(),
                str(movimiento.monto),
                movimiento.categoria_id,
                movimiento.medio_pago_id,
                movimiento.detalle,
            ),
        )
        self._connection.commit()
        created = self.get_by_id(cursor.lastrowid)
        if created is None:
            raise RuntimeError("No se pudo recuperar el movimiento creado")
        return created

    def list_all(self) -> list[Movimiento]:
        cursor = self._connection.cursor()
        cursor.execute(
            """
            SELECT m.id, t.nombre AS tipo, m.fecha, m.monto, m.categoria_id,
                   m.medio_pago_id, m.detalle, m.fecha_creacion
            FROM movimientos m
            JOIN tipos_movimiento t ON t.id = m.tipo_id
            ORDER BY m.fecha DESC, m.id DESC
            """
        )
        rows = cursor.fetchall()
        return [self._map_row(row) for row in rows]

    def list_by_tipo(self, tipo: TipoMovimiento) -> list[Movimiento]:
        cursor = self._connection.cursor()
        cursor.execute(
            """
            SELECT m.id, t.nombre AS tipo, m.fecha, m.monto, m.categoria_id,
                   m.medio_pago_id, m.detalle, m.fecha_creacion
            FROM movimientos m
            JOIN tipos_movimiento t ON t.id = m.tipo_id
            WHERE t.nombre = ?
            ORDER BY m.fecha DESC, m.id DESC
            """,
            (tipo.value,),
        )
        rows = cursor.fetchall()
        return [self._map_row(row) for row in rows]

    def get_by_id(self, movimiento_id: int) -> Movimiento | None:
        cursor = self._connection.cursor()
        cursor.execute(
            """
            SELECT m.id, t.nombre AS tipo, m.fecha, m.monto, m.categoria_id,
                   m.medio_pago_id, m.detalle, m.fecha_creacion
            FROM movimientos m
            JOIN tipos_movimiento t ON t.id = m.tipo_id
            WHERE m.id = ?
            """,
            (movimiento_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return self._map_row(row)

    def delete(self, movimiento_id: int) -> bool:
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM movimientos WHERE id = ?", (movimiento_id,))
        self._connection.commit()
        return cursor.rowcount > 0

    def _get_tipo_id(self, tipo: TipoMovimiento) -> int:
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT id FROM tipos_movimiento WHERE nombre = ?",
            (tipo.value,),
        )
        row = cursor.fetchone()
        if row is None:
            raise ValueError(f"Tipo de movimiento no soportado: {tipo}")
        return int(row["id"])

    @staticmethod
    def _map_row(row: sqlite3.Row) -> Movimiento:
        fecha_creacion = row["fecha_creacion"]
        return Movimiento(
            id=int(row["id"]),
            tipo=TipoMovimiento(str(row["tipo"])),
            fecha=date.fromisoformat(str(row["fecha"])),
            monto=Decimal(str(row["monto"])),
            categoria_id=int(row["categoria_id"]),
            medio_pago_id=int(row["medio_pago_id"]),
            detalle=str(row["detalle"]) if row["detalle"] is not None else None,
            fecha_creacion=datetime.fromisoformat(str(fecha_creacion))
            if fecha_creacion is not None
            else None,
        )
