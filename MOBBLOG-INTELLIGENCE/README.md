# MOBBLOG INTELLIGENCE

**Sistema inteligente de diagnóstico, asesoramiento estratégico y apoyo a la conversión comercial para una agencia de marketing digital.**

> Estado: El proyecto cuenta con una primera experimentación de Machine Learning utilizando el conjunto de datos público Lead Scoring de X Education. Se entrenó y evaluó un modelo de Regresión Logística, cuyos resultados y artefactos experimentales se encuentran en proceso de documentación e integración. La integración del agente conversacional, la conexión con MySQL y la validación del modelo con datos reales de MOBBLOG Digital permanecen pendientes.

## 1. Problema

Una agencia de marketing necesita recopilar información de sus prospectos, comprender sus necesidades, recomendar acciones de marketing pertinentes y dar seguimiento a las oportunidades comerciales. Cuando esta información queda dispersa o el diagnóstico depende únicamente de procesos manuales, se dificulta mantener una atención consistente y medir los resultados.

## 2. Objetivo

Diseñar y desarrollar un prototipo que permita:

1. Interactuar con prospectos mediante un agente conversacional.
2. Recopilar y estructurar información del negocio, necesidades, objetivos y presupuesto.
3. Elaborar un diagnóstico comercial y sugerir estrategias de marketing con base en reglas y una base de conocimiento.
4. Registrar prospectos, conversaciones, diagnósticos, propuestas y resultados.
5. Explorar un modelo de clasificación que estime la probabilidad de conversión cuando existan datos etiquetados adecuados.
6. Visualizar la actividad comercial mediante un dashboard.

## 3. Arquitectura propuesta

- **Interfaz:** aplicación web para el chat y panel administrativo.
- **Backend:** Python para coordinar la lógica, validaciones y servicios.
- **Persistencia:** MySQL para almacenar prospectos, conversaciones, diagnósticos, propuestas y resultados.
- **Agente:** modelo de lenguaje (LLM), instrucciones y reglas comerciales.
- **Conocimiento:** recuperación de información (RAG) sobre servicios, precios y procedimientos de MOBBLOG.
- **Ciencia de datos:** Pandas y scikit-learn para exploración, preparación, entrenamiento y evaluación.
- **Dashboard:** Streamlit como opción inicial de visualización.
- **Control de versiones:** GitHub para documentar y mantener el código fuente.

El backend conecta los componentes. MySQL se utiliza desde el inicio como almacenamiento operativo. El dashboard consulta la información del sistema y puede desarrollarse en paralelo. Machine Learning no es requisito para que el agente converse: se incorpora para resolver una tarea predictiva definida y evaluable.

## 4. Problema de Machine Learning propuesto

**Tarea:** clasificación supervisada para estimar la conversión de un prospecto.

- **Target (Y):** `Converted` (1 = convertido; 0 = no convertido) en el dataset externo de referencia.
- **Predictores (X):** variables disponibles antes del momento de predicción, seleccionadas después de revisar su significado y posibles fugas de información.
- **Modelos iniciales:** regresión logística como línea base y Random Forest como modelo comparativo.
- **Evaluación:** matriz de confusión, precision, recall, F1 y ROC-AUC.

No se afirma que el modelo esté entrenado ni que tenga un rendimiento validado. Los resultados se documentarán después de ejecutar los experimentos.

## 5. Dataset de referencia

Se está utilizando para experimentación el dataset **Leads Dataset – X Education**, publicado en Kaggle. El archivo analizado contiene 9,240 filas y 37 columnas; `Converted` registra 3,561 conversiones y 5,679 no conversiones. Se identificaron 0 filas duplicadas y valores faltantes relevantes.

Este conjunto pertenece al contexto de captación de prospectos de una institución educativa. **No representa clientes ni ventas históricas de MOBBLOG.** Se usa como referencia metodológica; antes de redistribuirlo en este repositorio se verificará la licencia y las condiciones de uso del recurso original.

Fuente: https://www.kaggle.com/datasets/ashydv/leads-dataset

## 6. Metodología

Se seguirá CRISP-DM: comprensión del negocio, comprensión de los datos, preparación, modelado, evaluación y despliegue. La documentación y los resultados se actualizarán conforme avance el prototipo.

## 7. Estado de avance

- [x] Definición inicial del problema y objetivo.
- [x] Identificación preliminar del target del dataset de referencia.
- [x] Diseño conceptual de arquitectura.
- [ ] Diccionario de datos y selección final de variables.
- [ ] Análisis exploratorio y preparación.
- [ ] Entrenamiento y evaluación del modelo.
- [ ] Diseño e implementación de la base MySQL.
- [ ] Agente conversacional y motor de recomendaciones.
- [ ] Dashboard e integración.
- [ ] Pruebas del prototipo.

## 8. Estructura

```text
MOBBLOG-INTELLIGENCE/
├── README.md
├── docs/
│   ├── business_problem.md
│   ├── architecture.md
│   └── dataset_card.md
└── database/
    └── schema.sql
```

## 9. Ejecución

Esta entrega es documentación inicial y esquema de base de datos. Todavía no contiene una aplicación ejecutable. Las instrucciones de instalación se incorporarán cuando se implemente el prototipo.

## 10. Seguridad y datos

No subir claves API, contraseñas, credenciales ni datos personales identificables. Usar variables de entorno y datos anonimizados o autorizados.
