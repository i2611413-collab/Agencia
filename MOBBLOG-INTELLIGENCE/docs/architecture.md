# Arquitectura propuesta

## Componentes

### 1. Interfaz
Chat para el prospecto y panel administrativo para el equipo de MOBBLOG.

### 2. Backend Python
Recibe solicitudes, valida datos, coordina el agente, aplica reglas de negocio, consulta MySQL y entrega resultados a la interfaz.

### 3. MySQL
Almacena prospectos, conversaciones, respuestas, diagnósticos, recomendaciones, propuestas y resultados de seguimiento.

### 4. Motor de IA
Un LLM interpreta mensajes y redacta respuestas. RAG permite consultar documentación controlada de MOBBLOG. Las reglas comerciales delimitan qué servicios se pueden recomendar y bajo qué condiciones.

### 5. Pipeline de Ciencia de Datos
Python/Pandas prepara los datos. scikit-learn permite entrenar y evaluar modelos de clasificación cuando se disponga de datos etiquetados adecuados.

### 6. Dashboard
Streamlit es la alternativa inicial para mostrar métricas y registros consultados desde MySQL. El dashboard es una interfaz de consulta, no una fase tecnológica que deba esperar a que termine el Machine Learning.

## Flujo operativo

1. El prospecto inicia una conversación.
2. El agente pregunta y recopila información.
3. Python valida y estructura las respuestas.
4. MySQL guarda el prospecto y el historial.
5. El motor de IA consulta el conocimiento y genera un diagnóstico preliminar.
6. Las reglas relacionan necesidades con estrategias y servicios.
7. La propuesta se presenta para revisión y aprobación humana.
8. El resultado comercial se registra.
9. Los datos etiquetados podrán alimentar análisis y modelos predictivos.

## Flujo de Machine Learning

MySQL/CSV → extracción → limpieza y transformación → selección de variables → separación entrenamiento/prueba → entrenamiento → evaluación → predicción.

## Nota metodológica

La predicción de conversión no determina por sí sola qué estrategia causará una venta. Para evaluar el efecto de estrategias se necesitarían diseños experimentales u otros métodos de inferencia causal.
