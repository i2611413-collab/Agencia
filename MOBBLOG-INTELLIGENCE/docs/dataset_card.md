# Ficha del dataset de referencia

## Identificación

- Nombre: Leads Dataset – X Education.
- Fuente: https://www.kaggle.com/datasets/ashydv/leads-dataset
- Archivo analizado: `Leads.csv`.
- Uso previsto: experimentación y aprendizaje metodológico sobre clasificación de conversión.

## Resumen del archivo inspeccionado

- Filas: 9,240.
- Columnas: 37.
- Variable objetivo: `Converted`.
- Convertidos (`1`): 3,561 (38.54%).
- No convertidos (`0`): 5,679 (61.46%).
- Filas duplicadas completas detectadas: 0.

## Valores faltantes destacados

- `Lead Quality`: 4,767.
- `Asymmetrique Profile Index`: 4,218.
- `Asymmetrique Activity Score`: 4,218.
- `Asymmetrique Activity Index`: 4,218.
- `Asymmetrique Profile Score`: 4,218.
- `Tags`: 3,353.

## Target

`Converted`: 1 indica conversión y 0 indica no conversión, según la codificación del conjunto.

## Limitaciones

1. Los datos corresponden al contexto de X Education, no a MOBBLOG.
2. No se debe afirmar que el modelo resultante representa el comportamiento de clientes de una agencia de marketing.
3. Se debe revisar la licencia y las condiciones de redistribución antes de subir el CSV al repositorio público.
4. Antes de entrenar, revisar valores faltantes, categorías, variables redundantes y fuga de información (*data leakage*).
5. Las variables predictoras deben estar disponibles en el momento en que se pretende emitir la predicción.
6. El rendimiento del modelo debe medirse con un conjunto de prueba y métricas apropiadas.

## Próximos pasos

- Construir diccionario de las 37 variables.
- Analizar distribución y calidad.
- Definir el momento de predicción.
- Seleccionar variables admisibles.
- Entrenar una línea base y comparar modelos.
