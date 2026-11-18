# MOBBLOG INTELLIGENCE — MVP web

Este paquete se incorpora **dentro de `MOBBLOG-INTELLIGENCE/`** del repositorio `Agencia`.
No borres `data/`, `database/schema.sql`, `docs/` ni `notebooks/`.

## Qué incluye
- Aplicación web Flask con chat comercial inicial.
- API para prospectos, conversaciones, propuestas, dashboard y scoring heurístico.
- Conexión a MySQL mediante variables de entorno.
- Configuración inicial para Render (`render.yaml`).

## Antes de desplegar
1. Crear una instancia MySQL 8 administrada en un proveedor compatible.
2. Crear la base de datos `mobblog_intelligence`.
3. Ejecutar `database/schema.sql` (el archivo existente del repositorio).
4. Ejecutar `database/migrations/001_add_lead_score.sql` una sola vez.
5. Desplegar este servicio en Render desde el repositorio `Agencia`, indicando como Root Directory `MOBBLOG-INTELLIGENCE`.
6. Configurar en Render: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`.
7. Revisar `/api/health` y luego probar chat, registro de prospectos y dashboard.

## Variables de entorno
Ver `.env.example`. Nunca subas credenciales reales al repositorio.

## Importante
- Este agente inicial funciona con reglas determinísticas. No es IA generativa.
- El score es heurístico y explicable; no es una probabilidad del modelo ML.
- El modelo entrenado con Leads.csv es experimental y el dataset no representa clientes de MOBBLOG.
- Este paquete no configura automáticamente un servidor MySQL ni crea una cuenta de hosting.
- No hay autenticación administrativa todavía. No publiques información sensible ni uses datos reales hasta implementar autenticación, autorización y protección adicional.
- La instancia gratuita de hosting puede suspenderse o tener límites; revisa las condiciones vigentes del proveedor.
