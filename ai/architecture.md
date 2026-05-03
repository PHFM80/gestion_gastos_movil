# Arquitectura del Proyecto

## Objetivo

Definir una estructura simple y modular para una app móvil desarrollada con **Python + Kivy**, orientada al control personal de ingresos y egresos.

La arquitectura debe facilitar:

- separación de responsabilidades
- mantenimiento simple
- crecimiento ordenado
- uso de SQLite local
- exportación de datos a CSV

## Estructura base

```text
app_gastos/
│
├── main.py
│
├── app/
│   ├── screens/
│   │   ├── home_screen.py
│   │   ├── movimiento_form_screen.py
│   │   ├── movimientos_list_screen.py
│   │   └── export_screen.py
│   │
│   ├── services/
│   │   ├── movimiento_service.py
│   │   ├── categoria_service.py
│   │   └── export_csv_service.py
│   │
│   ├── repositories/
│   │   ├── movimiento_repository.py
│   │   └── categoria_repository.py
│   │
│   ├── database/
│   │   ├── db.py
│   │   └── schema.py
│   │
│   ├── models/
│   │   ├── movimiento.py
│   │   └── categoria.py
│   │
│   └── utils/
│       ├── fechas.py
│       └── validaciones.py
│
├── assets/
│   ├── icons/
│   └── images/
│
├── exports/
│   └── csv/
│
└── ai/
    ├── README.md
    ├── context.md
    ├── models.md
    ├── arquitectura.md
    └── skills.md

esponsabilidades
main.py

Punto de entrada de la aplicación.

Responsabilidades:

iniciar la app Kivy
inicializar la base de datos
registrar las pantallas principales
cargar la pantalla inicial

No debe contener lógica de negocio.

app/screens/

Contiene las pantallas visuales de Kivy.

Responsabilidades:

mostrar formularios
capturar datos del usuario
mostrar listados
navegar entre pantallas
mostrar mensajes de error o confirmación

No debe acceder directamente a SQLite.

No debe contener reglas de negocio complejas.

app/services/

Contiene la lógica de negocio.

Responsabilidades:

validar datos antes de guardar
coordinar operaciones entre pantallas y repositorios
calcular saldos
calcular totales por fecha o categoría
preparar datos para exportación

Flujo esperado:

Pantalla → Servicio → Repositorio → SQLite
app/repositories/

Contiene el acceso a datos.

Responsabilidades:

crear registros
consultar registros
actualizar registros
eliminar registros
ejecutar consultas SQL necesarias

Los repositorios son la única capa que debe comunicarse directamente con SQLite.

app/database/

Contiene la configuración de la base de datos.

Responsabilidades:

abrir conexión SQLite
crear tablas iniciales
definir schema base
preparar la base al iniciar la app

Archivos sugeridos:

db.py: conexión a SQLite
schema.py: creación de tablas
app/models/

Contiene modelos simples del dominio.

Responsabilidades:

representar entidades principales
definir estructura básica de datos
facilitar el paso de datos entre capas

Modelos iniciales:

Movimiento
Categoria

No deben depender de Kivy.

app/utils/

Contiene funciones auxiliares reutilizables.

Ejemplos:

formateo de fechas
validaciones simples
helpers para montos
funciones comunes no específicas de una pantalla
assets/

Contiene recursos visuales de la app.

Ejemplos:

íconos
imágenes
logos
fuentes si fueran necesarias
exports/

Contiene archivos generados por la app.

Ejemplos:

reportes CSV
backups simples
archivos temporales exportados