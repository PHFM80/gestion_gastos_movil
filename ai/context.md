# Contexto del Proyecto

## Descripción general

Este proyecto es una app móvil desarrollada con **Python + Kivy** para el control personal de ingresos y egresos.

La app está pensada para uso propio, con funcionamiento local y simple.

## Objetivo principal

Permitir registrar y consultar movimientos económicos personales desde el celular.

La app debe ayudar a controlar:

- ingresos
- egresos
- saldo disponible
- movimientos por fecha
- movimientos por categoría

## Enfoque inicial

La primera versión debe ser simple y funcional.

El foco está en:

- carga manual de movimientos
- almacenamiento local
- consulta básica de movimientos
- exportación de datos a CSV

## Funcionamiento general

La app debe funcionar principalmente **offline**.

Los datos se guardan localmente usando **SQLite**.

No se requiere conexión a internet para cargar, consultar o modificar movimientos.

## Alcance inicial

La primera versión incluye:

- app móvil con Kivy
- base de datos local SQLite
- registro de ingresos
- registro de egresos
- categorías básicas
- listado de movimientos
- filtros simples
- exportación a CSV

## Fuera del alcance inicial

No forman parte de la primera versión:

- inteligencia artificial
- reportes avanzados
- gráficos complejos

Estas funcionalidades pueden evaluarse más adelante como mejoras futuras.

## Uso esperado

El usuario carga movimientos desde el celular.

Luego puede exportar la información a CSV para analizarla en una PC con herramientas como:

- Excel
- LibreOffice Calc
- Google Sheets
- Python / pandas

## Criterio general

El proyecto debe mantenerse simple, claro y fácil de mantener.

La prioridad es tener una app útil para registrar ingresos y egresos sin convertirla en un sistema complejo.