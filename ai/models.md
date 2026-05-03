# Modelos del Proyecto

## Objetivo

Definir las entidades principales de la app móvil para control personal de ingresos y egresos.

El modelo debe mantenerse simple, claro y fácil de mantener.

---

## Conceptos principales

La app trabaja con movimientos económicos personales.

Un movimiento puede ser:

- ingreso
- egreso

Cada movimiento tiene:

- tipo
- fecha
- monto
- categoría
- medio de pago
- detalle opcional

---

## Tipo de Movimiento

Representa si un movimiento es un ingreso o un egreso.

### Valores posibles

- `ingreso`
- `egreso`

## Decisión 

Aunque inicialmente tenga solo dos registros (`ingreso` y `egreso`), se modela como tabla porque se relaciona con categorías y movimientos.

Esto permite:

- filtrar categorías según el tipo seleccionado
- mantener una relación clara entre tipo, categoría y movimiento
- evitar valores sueltos dispersos por la app
- simplificar consultas y validaciones

## Categoría

Representa la clasificación del movimiento.

Ejemplos:

### Categorías de ingreso

- sueldo
- venta
- préstamo
- devolución
- otro ingreso

### Categorías de egreso

- supermercado
- combustible
- transporte
- alquiler
- servicios
- salud
- ocio
- compras
- otro egreso

### Campos

- `id`
- `nombre`
- `tipo`

### Reglas

- Toda categoría debe tener un nombre.
- Toda categoría debe estar asociada a un tipo.
- El tipo de categoría puede ser `ingreso` o `egreso`.
- Si el usuario selecciona `ingreso`, la app debe mostrar solo categorías de ingreso.
- Si el usuario selecciona `egreso`, la app debe mostrar solo categorías de egreso.
- Al guardar un movimiento, el tipo del movimiento debe coincidir con el tipo de la categoría seleccionada.

---

## Medio de Pago

Representa el medio utilizado para realizar o recibir el movimiento.

Ejemplos:

- efectivo
- transferencia
- Mercado Pago
- tarjeta de débito
- tarjeta de crédito
- cuenta bancaria
- billetera virtual
- otro

### Campos

- `id`
- `nombre`

### Reglas

- Todo medio de pago debe tener un nombre.
- Puede usarse tanto para ingresos como para egresos.
- No depende del tipo de movimiento.
- No depende de la categoría.

---

## Movimiento

Representa una operación económica registrada por el usuario.

Puede ser un ingreso o un egreso.

### Campos

- `id`
- `tipo`
- `fecha`
- `monto`
- `categoria_id`
- `medio_pago_id`
- `detalle`
- `fecha_creacion`

### Detalle de campos

#### `tipo`

Indica si el movimiento es:

- `ingreso`
- `egreso`

Debe coincidir con el tipo de la categoría seleccionada.

#### `fecha`

Fecha real del ingreso o egreso.

Ejemplo:

- fecha en que se pagó una compra
- fecha en que se recibió un sueldo
- fecha en que se realizó una transferencia

#### `monto`

Importe del movimiento.

Reglas:

- debe ser mayor a cero
- no debe guardarse como texto
- debe permitir decimales

#### `categoria_id`

Referencia a la categoría del movimiento.

Reglas:

- es obligatoria
- debe pertenecer al mismo tipo que el movimiento

#### `medio_pago_id`

Referencia al medio de pago utilizado.

Reglas:

- es obligatorio
- puede usarse en ingresos o egresos

#### `detalle`

Texto opcional para aclaraciones.

Ejemplos:

- compra mensual
- pago compartido
- transferencia recibida
- regalo
- carga de combustible
- pago de servicio

Reglas:

- puede estar vacío
- no debe ser obligatorio

#### `fecha_creacion`

Fecha automática de creación del registro.

Reglas:

- se genera automáticamente
- sirve para ordenar o auditar cargas
- no reemplaza a la fecha real del movimiento

---

