# Skills del Proyecto

## Objetivo

Definir las habilidades, criterios y buenas prácticas que debe aplicar cualquier IA que trabaje sobre este proyecto.

Este archivo no define el alcance funcional ni la arquitectura.  
Para eso se deben consultar:

- `ai/context.md`
- `ai/models.md`
- `ai/arquitectura.md`

## Skill de diseño de interfaz

La app debe tener una interfaz simple, clara y usable en móvil.

Criterios:

- Priorizar pantallas limpias.
- Evitar sobrecargar formularios.
- Usar textos claros en botones y mensajes.
- Pensar siempre en uso táctil.
- Mantener navegación simple.
- Evitar flujos largos para registrar un movimiento.
- Mostrar confirmaciones cuando una acción importante se complete.
- Mostrar errores de forma clara y directa.

## Skill de experiencia de usuario

El flujo principal debe ser rápido.

Criterios:

- Registrar un ingreso o egreso debe requerir pocos pasos.
- Los campos obligatorios deben ser mínimos.
- Los valores frecuentes deben poder reutilizarse o seleccionarse fácilmente.
- Las acciones principales deben estar visibles.
- La app debe sentirse práctica para uso diario.
- Evitar pedir datos innecesarios.

## Skill de código modular

El código debe estar separado por responsabilidades.

Criterios:

- No mezclar interfaz con lógica de negocio.
- No mezclar lógica de negocio con acceso a datos.
- Mantener archivos con una responsabilidad clara.
- Evitar módulos demasiado grandes.
- Separar pantallas, servicios, repositorios, modelos y utilidades.
- Crear funciones pequeñas y reutilizables cuando tenga sentido.

## Skill de código limpio

El código debe ser legible y fácil de mantener.

Criterios:

- Usar nombres claros y descriptivos.
- Evitar abreviaciones innecesarias.
- No duplicar lógica.
- Mantener funciones simples.
- Evitar condiciones difíciles de leer.
- Eliminar código muerto.
- No agregar dependencias sin necesidad.
- Priorizar claridad antes que soluciones demasiado abstractas.

## Skill de validaciones

La app debe validar los datos antes de guardarlos.

Criterios:

- Validar que el monto sea correcto.
- Validar que el tipo de movimiento sea válido.
- Validar que la fecha exista y sea coherente.
- Validar campos obligatorios.
- Mostrar mensajes simples cuando haya errores.
- Evitar que datos incompletos lleguen a la base de datos.

## Skill de persistencia de datos

El manejo de datos debe ser confiable y simple.

Criterios:

- Centralizar el acceso a la base de datos.
- Evitar consultas SQL dispersas por la app.
- Manejar errores básicos de lectura y escritura.
- Mantener consistencia en los nombres de campos.
- No guardar datos duplicados innecesariamente.
- Pensar en respaldo y exportación de datos.

## Skill de exportación

La exportación debe generar archivos simples y útiles.

Criterios:

- El CSV debe ser claro.
- Los nombres de columnas deben ser entendibles.
- Las fechas deben tener formato consistente.
- Los montos deben exportarse de forma usable en planillas.
- No mezclar lógica visual con generación de archivos.
- El archivo exportado debe poder analizarse luego en PC.

## Skill de mantenimiento

El proyecto debe poder crecer sin volverse confuso.

Criterios:

- Hacer cambios pequeños.
- Documentar decisiones importantes.
- No reestructurar sin necesidad.
- Mantener compatibilidad con la estructura definida.
- Evitar soluciones difíciles de probar.
- Pensar primero en una versión funcional y luego en mejoras.

## Skill de criterio técnico

Antes de modificar o agregar algo, evaluar:

1. ¿La solución es necesaria?
2. ¿Simplifica o complica el proyecto?
3. ¿Respeta la arquitectura?
4. ¿Es fácil de mantener?
5. ¿Evita dependencias innecesarias?

## Criterio principal

La IA debe trabajar con criterio práctico: código claro, diseño simple, estructura modular y decisiones fáciles de mantener.s