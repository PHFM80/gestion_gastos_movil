import sqlite3

from app.database import get_connection
from app.models.categoria import Categoria
from app.models.tipo_movimiento import TipoMovimiento


class CategoriaRepository:
    def __init__(self, connection: sqlite3.Connection | None = None):
        self._connection = connection or get_connection()

    def create(self, categoria: Categoria) -> Categoria:
        tipo_id = self._get_tipo_id(categoria.tipo)
        cursor = self._connection.cursor()
        cursor.execute(
            """
            INSERT INTO categorias (nombre, tipo_id)
            VALUES (?, ?)
            """,
            (categoria.nombre, tipo_id),
        )
        self._connection.commit()
        return Categoria(id=cursor.lastrowid, nombre=categoria.nombre, tipo=categoria.tipo)

    def list_all(self) -> list[Categoria]:
        cursor = self._connection.cursor()
        cursor.execute(
            """
            SELECT c.id, c.nombre, t.nombre AS tipo
            FROM categorias c
            JOIN tipos_movimiento t ON t.id = c.tipo_id
            ORDER BY c.nombre
            """
        )
        rows = cursor.fetchall()
        return [self._map_row(row) for row in rows]

    def list_by_tipo(self, tipo: TipoMovimiento) -> list[Categoria]:
        cursor = self._connection.cursor()
        cursor.execute(
            """
            SELECT c.id, c.nombre, t.nombre AS tipo
            FROM categorias c
            JOIN tipos_movimiento t ON t.id = c.tipo_id
            WHERE t.nombre = ?
            ORDER BY c.nombre
            """,
            (tipo.value,),
        )
        rows = cursor.fetchall()
        return [self._map_row(row) for row in rows]

    def get_by_id(self, categoria_id: int) -> Categoria | None:
        cursor = self._connection.cursor()
        cursor.execute(
            """
            SELECT c.id, c.nombre, t.nombre AS tipo
            FROM categorias c
            JOIN tipos_movimiento t ON t.id = c.tipo_id
            WHERE c.id = ?
            """,
            (categoria_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return self._map_row(row)

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
    def _map_row(row: sqlite3.Row) -> Categoria:
        return Categoria(
            id=int(row["id"]),
            nombre=str(row["nombre"]),
            tipo=TipoMovimiento(str(row["tipo"])),
        )
