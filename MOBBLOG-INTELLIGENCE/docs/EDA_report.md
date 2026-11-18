# Informe de Exploración de Datos (EDA)
## MOBBLOG INTELLIGENCE — versión 1.0

**Estado:** análisis exploratorio inicial completado  
**Dataset:** Lead Scoring — X Education (`Leads.csv`)  
**Uso:** referencia experimental; no representa el historial comercial de MOBBLOG Digital.

---

## 1. Objetivo

Comprender la estructura, calidad y distribución del dataset antes de preparar variables y desarrollar un modelo predictivo de conversión de prospectos.

La variable objetivo de referencia es `Converted`:
- `0`: el prospecto no convirtió.
- `1`: el prospecto convirtió.

Este análisis no constituye entrenamiento ni evaluación de un modelo de Machine Learning.

## 2. Dimensiones y estructura

La carga inicial mediante Pandas confirmó:

- **9,240 registros**
- **37 columnas**

El archivo se cargó en un DataFrame denominado `df`.

## 3. Distribución de la variable objetivo

| Converted | Registros | Porcentaje |
|---:|---:|---:|
| 0 — No convirtió | 5,679 | 61.46 % |
| 1 — Convirtió | 3,561 | 38.54 % |
| **Total** | **9,240** | **100.00 %** |

La distribución presenta una diferencia entre clases. No es correcto evaluar un futuro clasificador únicamente mediante accuracy: deberán considerarse precision, recall, F1-score, matriz de confusión y ROC-AUC.

Como referencia, un clasificador trivial que siempre predijera la clase mayoritaria alcanzaría aproximadamente 61.46 % de accuracy, pero no identificaría conversiones.

## 4. Calidad de datos: valores faltantes

Los principales faltantes observados fueron:

| Variable | Faltantes | Porcentaje |
|---|---:|---:|
| Lead Quality | 4,767 | 51.59 % |
| Asymmetrique Profile Index | 4,218 | 45.65 % |
| Asymmetrique Activity Score | 4,218 | 45.65 % |
| Asymmetrique Activity Index | 4,218 | 45.65 % |
| Asymmetrique Profile Score | 4,218 | 45.65 % |
| Tags | 3,353 | 36.29 % |
| What matters most to you in choosing a course | 2,709 | 29.32 % |
| Lead Profile | 2,709 | 29.32 % |
| What is your current occupation | 2,690 | 29.11 % |
| Country | 2,461 | 26.63 % |
| Specialization | 1,438 | 15.56 % |
| City | 1,420 | 15.37 % |
| Page Views Per Visit | 137 | 1.48 % |
| TotalVisits | 137 | 1.48 % |
| Last Activity | 103 | 1.11 % |

**Interpretación:** la ausencia de información es considerable en algunas variables. No debe suponerse que un valor faltante equivale a una categoría de baja calidad ni deben eliminarse columnas o filas sin estudiar el significado y el patrón de ausencia.

Se observó que las cuatro variables `Asymmetrique` indicadas comparten exactamente 4,218 faltantes. Se debe investigar si responden a un mismo proceso de captura o cálculo.

## 5. Revisión categórica

La exploración de variables de tipo `object` mostró, entre otros, los siguientes casos:

- `Asymmetrique Activity Index` y `Asymmetrique Profile Index` presentan categorías `High`, `Medium` y `Low`, además de valores ausentes.
- `I agree to pay the amount through cheque` contiene únicamente `No` en los 9,240 registros. Al ser constante en este dataset, no discrimina entre observaciones y previsiblemente no aportará información predictiva.
- Se debe revisar el significado de valores como `Select`. Podrían representar opciones no seleccionadas y no respuestas sustantivas.

La decisión definitiva sobre codificación y exclusión se tomará durante la preparación de datos.

## 6. Estadísticas numéricas

Estadísticas observadas:

| Variable | Registros no nulos | Media | Mediana | Máximo |
|---|---:|---:|---:|---:|
| TotalVisits | 9,103 | 3.45 | 3 | 251 |
| Total Time Spent on Website | 9,240 | 487.70 | 248 | 2,272 |
| Page Views Per Visit | 9,103 | 2.36 | 2 | 55 |
| Asymmetrique Activity Score | 5,022 | 14.31 | 14 | 18 |
| Asymmetrique Profile Score | 5,022 | 16.34 | 16 | 20 |

`Lead Number` también aparece como variable numérica, pero es un identificador y no debe tratarse automáticamente como predictor.

`Converted` es la variable objetivo y debe mantenerse separada de las variables predictoras.

## 7. Investigación de valores extremos en TotalVisits

Percentiles observados:

| Percentil | TotalVisits |
|---:|---:|
| 50 % | 3 |
| 75 % | 5 |
| 90 % | 7 |
| 95 % | 10 |
| 99 % | 17 |
| 100 % | 251 |

Frecuencia por umbral:

| Umbral | Registros por encima | Porcentaje sobre 9,240 |
|---:|---:|---:|
| 10 | 353 | 3.82 % |
| 17 | 83 | 0.90 % |
| 30 | 10 | 0.11 % |
| 50 | 6 | 0.06 % |
| 100 | 3 | 0.03 % |

Se inspeccionaron los diez registros con más visitas. El máximo observado fue 251 visitas. En ese registro se observaron 49 segundos de tiempo en el sitio, 1.48 páginas por visita y `Converted = 1`.

Estos valores son atípicos respecto de la distribución, pero no se ha demostrado que sean errores. **No se eliminaron ni transformaron durante este EDA.** Cualquier tratamiento posterior deberá justificarse y compararse con una alternativa que conserve los registros.

## 8. Alertas y decisiones pendientes

1. Investigar los valores `Select` y distinguirlos de los valores realmente ausentes.
2. Consultar el diccionario de datos para comprender cada variable y sus categorías.
3. Investigar el patrón de ausencia de las variables `Asymmetrique`.
4. Revisar los valores extremos de `TotalVisits` y otras variables sin eliminarlos automáticamente.
5. Excluir identificadores como `Prospect ID` y `Lead Number` de los predictores, salvo justificación metodológica explícita.
6. Evitar fuga de información (*data leakage*): solo usar variables disponibles en el momento en que se estimaría la conversión.
7. Definir imputación, codificación y selección de variables dentro del flujo de preparación, ajustando transformaciones solo con los datos de entrenamiento.
8. Separar entrenamiento y evaluación antes de ajustar el modelo y establecer una línea base.

## 9. Limitaciones

- El dataset procede de X Education y no contiene el historial real de prospectos de MOBBLOG Digital.
- Sus resultados no permiten afirmar cómo convierten los clientes de MOBBLOG.
- El análisis presentado es exploratorio; todavía no se ha entrenado ni evaluado ningún modelo.
- Los datos faltantes y valores extremos requieren investigación adicional.
- No se deben presentar métricas predictivas hasta implementar y evaluar el modelo con un protocolo reproducible.

## 10. Conclusión

La exploración inicial permitió identificar la dimensión del dataset, la distribución de la variable objetivo, faltantes relevantes, variables categóricas constantes y valores extremos en `TotalVisits`.

El dataset puede utilizarse como referencia experimental para desarrollar y probar un flujo de preparación y clasificación. Antes del entrenamiento será necesario documentar el significado de las variables, resolver el tratamiento de faltantes y categorías especiales, controlar la fuga de información y definir una evaluación adecuada.

**Estado del proyecto:** fase de comprensión de datos de CRISP-DM — exploración inicial completada; preparación de datos pendiente.
