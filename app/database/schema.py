import sqlite3


def create_schema(connection: sqlite3.Connection) -> None:
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tipos_movimiento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE CHECK (nombre IN ('ingreso', 'egreso'))
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo_id INTEGER NOT NULL,
            FOREIGN KEY (tipo_id) REFERENCES tipos_movimiento (id)
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS medios_pago (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            monto NUMERIC NOT NULL CHECK (monto > 0),
            categoria_id INTEGER NOT NULL,
            medio_pago_id INTEGER NOT NULL,
            detalle TEXT,
            fecha_creacion TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tipo_id) REFERENCES tipos_movimiento (id),
            FOREIGN KEY (categoria_id) REFERENCES categorias (id),
            FOREIGN KEY (medio_pago_id) REFERENCES medios_pago (id)
        );
        """
    )

    cursor.execute(
        """
        INSERT OR IGNORE INTO tipos_movimiento (id, nombre)
        VALUES
            (1, 'ingreso'),
            (2, 'egreso');
        """
    )

    connection.commit()
