from datetime import date
from decimal import Decimal

from app.models.movimiento import Movimiento
from app.models.tipo_movimiento import TipoMovimiento
from app.repositories.categoria_repository import CategoriaRepository
from app.repositories.medio_pago_repository import MedioPagoRepository
from app.repositories.movimiento_repository import MovimientoRepository


class ValidationError(Exception):
    pass


class MovimientoService:
    def __init__(
        self,
        movimiento_repository: MovimientoRepository | None = None,
        categoria_repository: CategoriaRepository | None = None,
        medio_pago_repository: MedioPagoRepository | None = None,
    ):
        self._movimiento_repository = movimiento_repository or MovimientoRepository()
        self._categoria_repository = categoria_repository or CategoriaRepository()
        self._medio_pago_repository = medio_pago_repository or MedioPagoRepository()

    def crear_movimiento(
        self,
        tipo: TipoMovimiento,
        fecha: date,
        monto: Decimal,
        categoria_id: int,
        medio_pago_id: int,
        detalle: str | None = None,
    ) -> Movimiento:
        self._validar_monto(monto)
        self._validar_categoria(tipo, categoria_id)
        self._validar_medio_pago(medio_pago_id)

        movimiento = Movimiento(
            id=None,
            tipo=tipo,
            fecha=fecha,
            monto=monto,
            categoria_id=categoria_id,
            medio_pago_id=medio_pago_id,
            detalle=detalle.strip() if detalle else None,
            fecha_creacion=None,
        )
        return self._movimiento_repository.create(movimiento)

    def listar_movimientos(self) -> list[Movimiento]:
        return self._movimiento_repository.list_all()

    def listar_movimientos_por_tipo(self, tipo: TipoMovimiento) -> list[Movimiento]:
        return self._movimiento_repository.list_by_tipo(tipo)

    @staticmethod
    def _validar_monto(monto: Decimal) -> None:
        if monto <= 0:
            raise ValidationError("El monto debe ser mayor a cero")

    def _validar_categoria(self, tipo: TipoMovimiento, categoria_id: int) -> None:
        categoria = self._categoria_repository.get_by_id(categoria_id)
        if categoria is None:
            raise ValidationError("La categoria seleccionada no existe")
        if categoria.tipo != tipo:
            raise ValidationError("El tipo de movimiento no coincide con la categoria")

    def _validar_medio_pago(self, medio_pago_id: int) -> None:
        medio_pago = self._medio_pago_repository.get_by_id(medio_pago_id)
        if medio_pago is None:
            raise ValidationError("El medio de pago seleccionado no existe")
