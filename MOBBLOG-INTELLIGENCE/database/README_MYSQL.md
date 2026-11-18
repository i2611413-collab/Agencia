# Archivos MySQL — MOBBLOG INTELLIGENCE

## Contenido
- `schema.sql`: esquema completo; crea y selecciona `mobblog_intelligence`.
- `schema_render.sql`: mismo esquema, pero sin `CREATE DATABASE` ni `USE`.
  Úsalo cuando el proveedor MySQL ya haya creado la base de datos.
- `seed.sql`: reservado para datos de prueba; no inserta datos ficticios.

## Instalación
1. Crear una base de datos MySQL 8+ en el proveedor elegido.
2. Abrir su consola SQL o cliente MySQL.
3. Seleccionar la base de datos asignada.
4. Ejecutar `schema_render.sql` completo.
5. Configurar en Render las variables `DB_HOST`, `DB_PORT`, `DB_NAME`,
   `DB_USER` y `DB_PASSWORD` con los datos entregados por el proveedor.
6. Reiniciar el servicio web y comprobar `/api/health`.

## Importante
El archivo SQL crea las tablas, pero no ejecuta un servidor MySQL.
Render Web Service ejecuta la aplicación Flask; MySQL debe estar disponible
en un servidor/servicio de base de datos accesible desde Render.

No subir contraseñas ni credenciales al repositorio.
