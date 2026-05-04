from dataclasses import dataclass


@dataclass(slots=True)
class MedioPago:
    id: int | None
    nombre: str
