from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal

from app.models.tipo_movimiento import TipoMovimiento


@dataclass(slots=True)
class Movimiento:
    id: int | None
    tipo: TipoMovimiento
    fecha: date
    monto: Decimal
    categoria_id: int
    medio_pago_id: int
    detalle: str | None = None
    fecha_creacion: datetime | None = None
