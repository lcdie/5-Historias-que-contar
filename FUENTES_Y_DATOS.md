# Fuentes y datos

Este documento resume la procedencia, el rol narrativo y las consideraciones de uso de los datasets empleados en las 5 historias del proyecto. El objetivo es hacer explícita la relación entre **arquetipo, evidencia y dataset**, y favorecer la reproducibilidad y la lectura crítica.

> Nota: las conclusiones de cada historia se interpretan sobre el **dataset efectivamente cargado/analizado** en su notebook/HTML. Donde existen variantes posibles (p. ej. dataset real vs. proxy sintético), se indica de forma explícita.

## Resumen por historia

| Historia | Arquetipo | Archivo(s) en `data/raw/` | Fuente / procedencia | Uso en la narrativa |
|---|---|---|---|---|
| 1. La curva que no miente | Serie temporal + cambio estructural | `co2_mm_mlo.csv` | Registro de CO₂ atmosférico de Mauna Loa (NOAA GML / Scripps CO₂ Program, Curva de Keeling), obtenido/procesado mediante `data/download_data.py` | Analizar tendencia, estacionalidad, variabilidad interanual y evidencia de cambios de régimen/aceleración en una serie temporal larga |
| 2. Cuando el promedio miente | Comparación multivariable + paradoja de Simpson | `gapminder.csv` | Dataset Gapminder (indicadores por país-año: esperanza de vida, PIB per cápita, población, continente), preparado vía `data/download_data.py` | Contrastar relaciones agregadas y desagregadas (pooled/within/between), evidenciar heterogeneidad y riesgo de inferencias por agregación |
| 3. La aguja en el pajar financiero | Outliers + detección de anomalías | `creditcard.csv` *(generado localmente, no versionado)* | **Por defecto:** proxy sintético PCA-like reproducible generado por `data/download_data.py` con el mismo esquema que la referencia ULB/Kaggle Credit Card Fraud (`Time`, `Amount`, `V1`–`V28`, `Class`). **Alternativa:** reemplazo manual por el dataset real ULB/Kaggle en la misma ruta | Estudiar detección de eventos raros bajo fuerte desbalance, costos asimétricos, validación temporal y comparación no supervisado/supervisado |
| 4. Pingüinos como termómetros | Drill-down jerárquico + descomposición de varianza | `penguins.csv` | Palmer Penguins (palmerpenguins / Horst, Hill & Gorman), preparado vía `data/download_data.py` | Explorar jerarquías (especie/isla/sexo, etc.) y cuantificar contribuciones de niveles a la variabilidad morfológica |
| 5. ¿Ingreso causa precio o es la playa? | Intersección multivariable / confounding espacial | `california_housing.csv` | California Housing (derivado del censo de California 1990; disponible en scikit-learn / fuentes públicas), preparado vía `data/download_data.py` | Analizar relaciones multivariadas y confounding espacial entre ingreso, localización y valor de la vivienda, con énfasis en efectos parciales y heterogeneidad |

## Detalle y consideraciones por dataset

### 1) CO₂ Mauna Loa — `co2_mm_mlo.csv`
- **Contenido típico:** fecha/periodo y mediciones de concentración de CO₂ (ppm), con posibles campos de tendencia/interpolación según formato.
- **Relevancia para el arquetipo:** serie observacional larga y regularmente muestreada, adecuada para descomposición temporal y análisis de cambios estructurales.
- **Consideraciones:** valores faltantes o ajustes/interpolaciones documentados por la fuente; diferencias entre mediciones y tendencia desestacionalizada; el registro puntual de Mauna Loa no equivale exactamente a un promedio global.
- **Referencia general:** NOAA Global Monitoring Laboratory — Trends in Atmospheric Carbon Dioxide (Mauna Loa); Scripps CO₂ Program.

### 2) Gapminder — `gapminder.csv`
- **Contenido típico:** país, continente, año, esperanza de vida, PIB per cápita y población.
- **Relevancia para el arquetipo:** estructura comparativa y longitudinal (panel) que permite observar agregación, heterogeneidad entre grupos y paradojas de composición/Simpson.
- **Consideraciones:** calidad y comparabilidad histórica entre países; transformaciones (p. ej. escala logarítmica de ingreso) influyen en la interpretación; correlación observacional no implica causalidad.
- **Referencia general:** Gapminder Foundation / gapminder.org (compilación de indicadores de desarrollo).

### 3) Credit Card Fraud — `creditcard.csv` (local, no versionado)
- **Contenido esperado:** `Time`, `V1`–`V28` (componentes PCA anonimizadas), `Amount`, `Class` (0/1).
- **Relevancia para el arquetipo:** problema canónico de eventos raros con fuerte desbalance, donde importan métricas operativas, umbrales y validación temporal.
- **Consideraciones clave:**
  - En este repositorio, por defecto se usa un **proxy sintético reproducible** generado localmente para permitir ejecución sin credenciales y mantener el esquema del dataset de referencia.
  - Las métricas absolutas dependen del dataset cargado (sintético o real); la historia enfatiza el razonamiento metodológico del arquetipo y sus trade-offs.
  - Si se emplea el dataset real (ULB/Kaggle), deben respetarse sus términos de uso y el contexto original (anonimización PCA, horizonte temporal limitado, etc.).
- **Referencia general:** ULB Machine Learning Group / Kaggle — *Credit Card Fraud Detection* (dataset de referencia).

### 4) Palmer Penguins — `penguins.csv`
- **Contenido típico:** especie, isla, medidas morfológicas (pico, aleta, masa corporal), sexo y año de observación.
- **Relevancia para el arquetipo:** datos con estructura jerárquica/niveles naturales y desbalance de diseño, útiles para drill-down y descomposición de varianza.
- **Consideraciones:** valores faltantes en algunas variables; diseño observacional (no experimental); no todas las combinaciones especie-isla están igualmente representadas.
- **Referencia general:** Horst AM, Hill AP, Gorman KB (2020). *palmerpenguins*; datos originales del Palmer Station LTER.

### 5) California Housing — `california_housing.csv`
- **Contenido típico:** variables socioeconómicas y geográficas por bloque/grupo censal (ingreso mediano, edad de vivienda, habitaciones, ocupación, latitud, longitud) y valor mediano de vivienda.
- **Relevancia para el arquetipo:** escenario multivariable con fuerte componente espacial, adecuado para discutir confounding, dependencia espacial y heterogeneidad de efectos.
- **Consideraciones:** datos censales de 1990 (contexto histórico); variables agregadas por área (riesgo de falacia ecológica/MAUP); posible tope/censura en valores (según versión); asociaciones no equivalen a causalidad.
- **Referencia general:** Pace, R. Kelley and Ronald Barry (1997), *Sparse Spatial Autoregressions*; versión ampliamente difundida vía scikit-learn (`fetch_california_housing`).

## Reproducibilidad de los datos

- **Script:** `python data/download_data.py` (verifica/descarga/prepara datasets y genera el proxy sintético de fraude cuando corresponde).
- **Ubicación:** `data/raw/`.
- **Versionado:** los datasets base (CO₂, Gapminder, Penguins, California Housing) se incluyen en el repositorio; `creditcard.csv` se excluye del control de versiones y debe generarse localmente o reemplazarse manualmente.

## Citas y atribución

- Este proyecto es de carácter académico. Se recomienda citar las fuentes originales de cada dataset al reutilizar resultados, figuras o análisis derivados.
- Las bibliotecas y metodologías específicas empleadas en cada notebook se documentan en el propio notebook, en el informe crítico y en el reporte técnico del proyecto.
