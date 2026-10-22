# Genesis: sistema de análisis preventivo de clientes

Aplicación web desarrollada solo con Python y Streamlit. Genesis evalúa a un cliente de una empresa de servicios, estima la probabilidad de que la abandone y le asigna un nivel de atención (bajo, medio o alto) con una recomendación de seguimiento.

Flujo: formulario web, preparación de datos, modelo de clasificación, resultado visual y registro en el historial (SQLite).

Repositorio: https://github.com/Ndeahxyzlo/Machine-learning

## Secciones de la aplicación

| Sección | Contenido |
|---|---|
| Panel principal | Tarjetas de resumen, cuatro gráficas y las últimas evaluaciones |
| Nueva evaluación | Formulario agrupado, nivel de atención, probabilidad, barra de progreso, recomendación y factores que influyeron |
| Historial | Evaluaciones guardadas con filtros, descarga en CSV y eliminación con confirmación |
| Análisis técnico | Modelo seleccionado, comparación de modelos, matriz de confusión, reporte, validación cruzada, métricas explicadas y limitaciones |

## Ejecución

```bash
pip install -r requirements.txt
python generar_dataset.py
python entrenar.py
streamlit run app.py
```

La aplicación abre en `http://localhost:8501`. Si se reentrena el modelo, hay que reiniciar la aplicación. Los archivos `data/` y `ml/` ya vienen en el repositorio, así que `streamlit run app.py` funciona directamente. Si el archivo del modelo no se puede cargar por una diferencia de versiones, la aplicación lo vuelve a entrenar sola.

## Despliegue en Streamlit Community Cloud

1. Crear una nueva aplicación en https://share.streamlit.io con este repositorio.
2. Rama `main` y archivo principal `app.py`.
3. El historial usa SQLite en disco local. En Streamlit Cloud el disco es temporal, por lo que el historial puede reiniciarse cuando la aplicación se reinicia.

## Estructura

| Archivo | Contenido |
|---|---|
| `generar_dataset.py` | Crea `data/clientes_raw.csv` con 505 filas, nulos y duplicados |
| `entrenar.py` | Exploración con Pandas, limpieza, cuatro modelos, métricas y guardado del seleccionado |
| `app.py` | Interfaz web en Streamlit |
| `utils.py` | Carga del modelo, niveles de atención, recomendaciones y base de datos SQLite |
| `data/` | Datos originales (`clientes_raw.csv`) y datos limpios (`clientes.csv`) |
| `ml/` | Modelo entrenado (`modelo.pkl`) y resultados (`metricas.json`) |
| `assets/` | Logo e ícono de Genesis |
| `docs/` | Documentación del proyecto en DOCX y PDF |
| `.streamlit/config.toml` | Tema visual |
| `.devcontainer/` | Configuración para GitHub Codespaces |

## Modelo

Se entrenan cuatro modelos con los mismos 400 clientes de entrenamiento y se evalúan con los mismos 100 de prueba.

| Modelo | Accuracy | Recall (Abandona) | F1 (Abandona) |
|---|---|---|---|
| Regresión logística (estándar) | 75,0 % | 45,7 % | 0,561 |
| Regresión logística (balanceada) | 73,0 % | 62,9 % | 0,620 |
| Random Forest | 73,0 % | 42,9 % | 0,526 |
| KNN | 74,0 % | 48,6 % | 0,567 |

Genesis usa la regresión logística balanceada. Es una aplicación preventiva y perder a un cliente cuesta más que una llamada de seguimiento de más, así que se priorizó detectar más abandonos. A cambio del recall (de 46 % a 63 %), el accuracy baja 2 puntos y aparecen 8 alertas innecesarias más en la prueba. La regla de selección es: entre los modelos con accuracy a menos de 3 puntos del mejor, se elige el de mayor F1 de la clase Abandona.

## Conceptos clave

- El modelo se entrena una sola vez con `entrenar.py` y se guarda con `joblib`. La aplicación solo lo carga y predice.
- El `StandardScaler` va dentro del `Pipeline` guardado, de modo que la aplicación aplica el mismo escalado del entrenamiento.
- Se usa `predict_proba` para obtener la probabilidad. El nivel de atención es Bajo por debajo de 40 %, Medio entre 40 % y 70 %, y Alto desde 70 %.
- Las columnas se reordenan con `modelo["features"]` antes de predecir, porque un orden distinto produce resultados erróneos sin mostrar errores.
- Al balancear las clases, las probabilidades tienden a ser más altas que la frecuencia real de abandono. Sirven para priorizar clientes, no como cifra exacta.
- Los datos son sintéticos. El abandono depende de la satisfacción, la antigüedad y la frecuencia de compra, más ruido aleatorio.
- Con 100 casos de prueba el accuracy varía unos puntos entre ejecuciones. La validación cruzada de `metricas.json` es una estimación más estable.
- En la página de evaluación, el efecto de cada variable se calcula reemplazando su valor por la mediana de la base y midiendo cuánto cambia la probabilidad. Es una asociación, no una causa.

## Uso de un dataset real

Reemplazar `data/clientes_raw.csv` por un archivo con las columnas `edad`, `ingresos`, `frecuencia_compra`, `cantidad_productos`, `tiempo_cliente`, `satisfaccion` y `abandono` (1 si el cliente se fue, 0 si permanece), y ejecutar de nuevo `entrenar.py`.
