from app.models.categoria import Categoria
from app.models.tipo_movimiento import TipoMovimiento
from app.repositories.categoria_repository import CategoriaRepository


class CategoriaService:
    def __init__(self, categoria_repository: CategoriaRepository | None = None):
        self._categoria_repository = categoria_repository or CategoriaRepository()

    def crear_categoria(self, nombre: str, tipo: TipoMovimiento) -> Categoria:
        nombre_limpio = nombre.strip()
        if not nombre_limpio:
            raise ValueError("El nombre de la categoria es obligatorio")
        return self._categoria_repository.create(
            Categoria(id=None, nombre=nombre_limpio, tipo=tipo)
        )

    def listar_por_tipo(self, tipo: TipoMovimiento) -> list[Categoria]:
        return self._categoria_repository.list_by_tipo(tipo)

    def listar_todas(self) -> list[Categoria]:
        return self._categoria_repository.list_all()
