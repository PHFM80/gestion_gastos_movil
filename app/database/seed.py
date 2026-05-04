import sqlite3


TIPOS_MOVIMIENTO = ("ingreso", "egreso")

MEDIOS_PAGO = (
    "efectivo",
    "billetera virtual",
    "transferencia",
    "qr",
    "otro",
)

CATEGORIAS_INGRESO = (
    "sueldo",
    "venta",
    "prestamo",
    "devolucion",
    "otro ingreso",
)

CATEGORIAS_EGRESO = (
    "supermercado",
    "combustible",
    "transporte",
    "alquiler",
    "servicios",
    "salud",
    "ocio",
    "compras",
    "otro egreso",
)


def ensure_seed_data(connection: sqlite3.Connection) -> None:
    _ensure_tipos_movimiento(connection)
    _ensure_medios_pago(connection)
    _ensure_categorias(connection, "ingreso", CATEGORIAS_INGRESO)
    _ensure_categorias(connection, "egreso", CATEGORIAS_EGRESO)
    connection.commit()


def _ensure_tipos_movimiento(connection: sqlite3.Connection) -> None:
    cursor = connection.cursor()
    for tipo in TIPOS_MOVIMIENTO:
        cursor.execute(
            """
            INSERT INTO tipos_movimiento (nombre)
            SELECT ?
            WHERE NOT EXISTS (
                SELECT 1 FROM tipos_movimiento WHERE nombre = ?
            )
            """,
            (tipo, tipo),
        )


def _ensure_medios_pago(connection: sqlite3.Connection) -> None:
    cursor = connection.cursor()
    for medio_pago in MEDIOS_PAGO:
        cursor.execute(
            """
            INSERT INTO medios_pago (nombre)
            SELECT ?
            WHERE NOT EXISTS (
                SELECT 1 FROM medios_pago WHERE nombre = ?
            )
            """,
            (medio_pago, medio_pago),
        )


def _ensure_categorias(
    connection: sqlite3.Connection, tipo_nombre: str, categorias: tuple[str, ...]
) -> None:
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id FROM tipos_movimiento WHERE nombre = ?",
        (tipo_nombre,),
    )
    row = cursor.fetchone()
    if row is None:
        raise ValueError(f"No existe el tipo de movimiento requerido: {tipo_nombre}")

    tipo_id = int(row["id"])
    for categoria in categorias:
        cursor.execute(
            """
            INSERT INTO categorias (nombre, tipo_id)
            SELECT ?, ?
            WHERE NOT EXISTS (
                SELECT 1
                FROM categorias
                WHERE nombre = ? AND tipo_id = ?
            )
            """,
            (categoria, tipo_id, categoria, tipo_id),
        )
