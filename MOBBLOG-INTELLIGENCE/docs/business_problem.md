# Definición del problema de negocio

## Contexto

MOBBLOG es una agencia de marketing digital que necesita mejorar la forma en que recibe, diagnostica y gestiona prospectos comerciales.

## Problema

La información inicial de un prospecto puede llegar por distintos canales y no siempre se recoge de manera estructurada. Esto dificulta comprender de forma consistente el negocio, identificar necesidades prioritarias, relacionarlas con servicios adecuados y dar seguimiento al proceso comercial.

## Propuesta de solución

Desarrollar un agente inteligente que:

1. Mantenga una conversación inicial con el prospecto.
2. Recopile información relevante mediante preguntas.
3. Genere un perfil estructurado del negocio.
4. Apoye un diagnóstico de necesidades y oportunidades.
5. Recomiende estrategias y servicios usando conocimiento documentado y reglas explícitas.
6. Prepare un resumen o propuesta para revisión humana.
7. Registre el resultado del seguimiento: contratado, no contratado o pendiente.

## Pregunta de Ciencia de Datos

Como línea experimental separada, se plantea estudiar si las características disponibles de un prospecto permiten estimar su conversión comercial.

## Variable objetivo experimental

En el dataset externo X Education, la variable objetivo es `Converted`:
- 1: el prospecto se convirtió.
- 0: el prospecto no se convirtió.

Esta definición corresponde al dataset de referencia y no debe confundirse con datos históricos de MOBBLOG.

## Alcance del prototipo

El prototipo demostrará el flujo conversacional, el registro estructurado, un diagnóstico basado en reglas/conocimiento y un panel básico. El modelo predictivo se integrará únicamente después de preparar y evaluar los datos.

## Fuera del alcance inicial

- Garantizar cierres de venta.
- Ejecutar campañas publicitarias automáticamente.
- Afirmar causalidad entre una recomendación y una venta.
- Presentar predicciones experimentales como resultados comerciales reales.
