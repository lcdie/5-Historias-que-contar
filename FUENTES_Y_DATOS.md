# Fuentes y datos

Este documento describe la procedencia, el rol analítico y las consideraciones de uso de los datasets empleados en las 5 historias. Complementa al informe crítico y al apéndice metodológico.

- Referencias formales y citas sugeridas: [`REFERENCIAS_Y_APENDICE_METODOLOGICO.md`](REFERENCIAS_Y_APENDICE_METODOLOGICO.md)
- Parámetros/criterios metodológicos por historia: [`REFERENCIAS_Y_APENDICE_METODOLOGICO.md`](REFERENCIAS_Y_APENDICE_METODOLOGICO.md)

> **Principio de coherencia:** las conclusiones de cada historia se interpretan sobre el **dataset efectivamente cargado y procesado** en la ejecución del notebook/HTML. Cuando existen variantes (p. ej. proxy sintético vs. dataset real), esto se declara y condiciona el alcance de los resultados.

## Resumen por historia

| Historia | Arquetipo | Archivo(s) en `data/raw/` | Fuente / procedencia | Uso en la narrativa | Alcance/advertencias clave |
|---|---|---|---|---|---|
| 1. La curva que no miente | Serie temporal + cambio estructural | `co2_mm_mlo.csv` | Registros de CO₂ atmosférico de Mauna Loa (NOAA GML / tradición de mediciones de Keeling), preparados vía `data/download_data.py` | Descomposición temporal, tasas de cambio, contraste de regímenes y validación/diagnóstico | Serie de estación específica (no promedio global); posibles interpolaciones/procesamiento de fuente |
| 2. Cuando el promedio miente | Comparación multivariable + paradoja de Simpson/composición | `gapminder.csv` | Dataset Gapminder (indicadores país-año), preparado vía `data/download_data.py` | Comparación pooled/within/between y sensibilidad a la agregación | Asociación observacional; comparabilidad histórica y transformaciones influyen en la lectura |
| 3. La aguja en el pajar financiero | Outliers + detección de anomalías | `creditcard.csv` *(no versionado; generado localmente)* | **Por defecto:** proxy sintético PCA-like reproducible (`data/download_data.py`) con esquema de referencia ULB/Kaggle. **Alternativa:** reemplazo manual por dataset real ULB/Kaggle | Pipeline de detección bajo desbalance: métricas PR/costo, umbrales y validación temporal | Con proxy: **simulación/pipeline**, no desempeño real. Con datos reales: respetar términos/licencias y releer métricas |
| 4. Pingüinos como termómetros | Drill-down jerárquico + descomposición de varianza | `penguins.csv` | Palmer Penguins (Horst, Hill & Gorman / Palmer LTER), preparado vía `data/download_data.py` | Análisis jerárquico y partición de variabilidad morfológica | Diseño observacional no balanceado; valores faltantes; combinaciones especie–isla incompletas |
| 5. ¿Ingreso y precio: asociación o confounding espacial? | Intersección multivariable + confounding espacial (observacional) | `california_housing.csv` | California Housing (censo 1990; Pace & Barry, 1997), preparado vía `data/download_data.py` | Asociaciones condicionales ingreso–precio, estructura espacial y heterogeneidad | Datos agregados (MAUP), antigüedad (1990), posible *top-coding*; no identificación causal sin estrategia adicional |

## Detalle por dataset

### 1) CO₂ Mauna Loa — `co2_mm_mlo.csv`
- **Contenido típico:** variables temporales y mediciones/derivados de concentración de CO₂ (ppm) según el esquema cargado.
- **Relevancia:** permite analizar estacionalidad, tendencia y variación de tasas en una serie larga.
- **Consideraciones:** distinguir mediciones y series procesadas/interpoladas según columnas disponibles; una estación no representa exactamente un promedio global.
- **Referencia:** NOAA GML — Mauna Loa CO₂ (ver apéndice de referencias).

### 2) Gapminder — `gapminder.csv`
- **Contenido típico:** `country`, `continent`, `year`, `lifeExp`, `gdpPercap`, `pop`.
- **Relevancia:** estructura de panel adecuada para contrastar agregación y desagregación (pooled/within/between).
- **Consideraciones:** comparabilidad entre países/épocas, transformaciones (p. ej. logaritmo de ingreso) y naturaleza observacional (sin identificación causal por defecto).
- **Referencia:** Gapminder Foundation (ver apéndice).

### 3) Credit Card Fraud — `creditcard.csv` (local, no versionado)
- **Esquema esperado:** `Time`, `V1`–`V28`, `Amount`, `Class`.
- **Por defecto en este repositorio:** proxy sintético PCA-like reproducible generado por `data/download_data.py` para ejecución sin credenciales.
- **Alternativa:** reemplazar el archivo por el dataset real ULB/Kaggle manteniendo ruta y esquema.
- **Consideraciones:** (i) variables PCA anonimizadas limitan interpretación sustantiva de *features*; (ii) el desbalance exige métricas y validación temporal adecuadas; (iii) **si el insumo es sintético, los resultados cuantitativos son demostrativos del pipeline y no generalizables a fraude real**.
- **Referencia canónica:** Dal Pozzolo et al. (2015) / ULB-Kaggle Credit Card Fraud Detection.

### 4) Palmer Penguins — `penguins.csv`
- **Contenido típico:** especie, isla, sexo, año y medidas morfométricas (pico, aleta, masa corporal).
- **Relevancia:** permite drill-down jerárquico y análisis de varianza en datos de campo.
- **Consideraciones:** valores faltantes, muestreo observacional y diseño no balanceado (no todas las combinaciones especie–isla presentes).
- **Referencia:** Horst, Hill & Gorman; Palmer LTER.

### 5) California Housing — `california_housing.csv`
- **Contenido típico:** variables socioeconómicas y geográficas por *block group* y valor mediano de vivienda.
- **Relevancia:** escenario multivariable con componente espacial para estudiar condicionamiento, dependencia y heterogeneidad.
- **Consideraciones:** datos de 1990, agregación espacial (MAUP/falacia ecológica potencial), posibles límites/censura en la variable objetivo según versión; asociaciones no implican causalidad.
- **Referencia:** Pace & Barry (1997); distribución habitual vía scikit-learn.

## Reproducibilidad de datos

- **Script:** `python data/download_data.py`
- **Ubicación:** `data/raw/`
- **Versionado:** se incluyen `co2_mm_mlo.csv`, `gapminder.csv`, `penguins.csv`, `california_housing.csv`; `creditcard.csv` se excluye del control de versiones y debe generarse localmente o sustituirse.
- **Trazabilidad de ejecución:** al reportar resultados, indicar si el entorno fue núcleo/completo y, para Historia 3, si el dataset fue proxy sintético o real.

## Citación y atribución

- Citar las fuentes originales de los datasets y, cuando corresponda, los métodos empleados (ver `REFERENCIAS_Y_APENDICE_METODOLOGICO.md`).
- Mantener coherencia entre: archivo de datos usado, parámetros/criterios metodológicos aplicados y resultados mostrados en notebooks/HTML.
