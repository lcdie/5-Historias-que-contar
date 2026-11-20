# Referencias y apéndice metodológico

Este documento complementa `INFORME_CRITICO_ARQUETIPOS.md`, `REPORTE_TECNICO.md` y los notebooks con (i) referencias formales de datos y métodos, (ii) versiones/fuentes de datos usadas en el proyecto y (iii) parámetros/criterios metodológicos clave empleados en las historias. Su objetivo es mejorar la trazabilidad y la evaluación crítica de los resultados.

> **Nota de alcance:** los resultados numéricos definitivos son los producidos por los notebooks/HTML ejecutados en el entorno declarado. Cuando una técnica depende de paquetes opcionales no disponibles, el notebook debe reportarlo explícitamente y limitar sus conclusiones a lo efectivamente calculado.

---

## 1. Referencias de datos (fuentes y procedencia)

| Dataset (archivo) | Historia | Fuente/procedencia | Acceso en este proyecto | Observaciones de versión/uso |
|---|---|---|---|---|
| `data/raw/co2_mm_mlo.csv` | 1 | NOAA Global Monitoring Laboratory (GML), Mauna Loa CO₂ records; programa histórico de mediciones atmosféricas (Keeling/Scripps-NOAA). | Incluido en `data/raw/`; preparado/normalizado mediante `data/download_data.py`. | Serie mensual utilizada tal como se carga en el notebook; interpretación sujeta a documentación de la fuente (interpolaciones, tendencias, metadatos). No equivale a promedio global. |
| `data/raw/gapminder.csv` | 2 | Gapminder (compilación de indicadores de desarrollo por país-año; fuentes subyacentes habituales incluyen bancos de datos internacionales). | Incluido en `data/raw/`; obtenido/preparado vía `data/download_data.py`. | Panel país-año usado para comparaciones pooled/within/between. Asociaciones observacionales, no identificación causal. |
| `data/raw/creditcard.csv` | 3 | **Referencia canónica:** ULB/Kaggle Credit Card Fraud Detection (Dal Pozzolo et al., 2015), esquema `Time, V1–V28, Amount, Class`. **En este repositorio (por defecto):** proxy sintético PCA-like reproducible generado localmente. | **No versionado**; se genera con `python data/download_data.py` o se reemplaza manualmente por el dataset real en la misma ruta y esquema. | Las métricas dependen del archivo cargado. Con proxy sintético, los resultados son de **simulación/pipeline**, no desempeño real en fraude. |
| `data/raw/penguins.csv` | 4 | Palmer Archipelago (Antarctica) penguin data (Horst, Hill & Gorman / Palmer LTER). | Incluido en `data/raw/`; preparado vía `data/download_data.py`. | Datos observacionales con estructura jerárquica y diseño no balanceado; posibles valores faltantes. |
| `data/raw/california_housing.csv` | 5 | California Housing derivado del censo de 1990 (Pace & Barry, 1997), difundido también vía scikit-learn. | Incluido en `data/raw/`; preparado vía `data/download_data.py`. | Datos agregados por *block group* (MAUP), antigüedad 1990, potencial *top-coding* en la variable objetivo según versión; inferencia observacional. |

### Citas de datos y trabajos de referencia (formato sugerido)
- NOAA Global Monitoring Laboratory. *Trends in Atmospheric Carbon Dioxide* (Mauna Loa CO₂). https://gml.noaa.gov/ccgg/trends/ (consultar fecha de acceso según ejecución).
- Gapminder Foundation. *Gapminder Data*. https://www.gapminder.org/data/ (y documentación de indicadores subyacentes según variables usadas).
- Dal Pozzolo, A., Caelen, O., Johnson, R. A., & Bontempi, G. (2015). *Calibrating Probability with Undersampling for Unbalanced Classification*. (dataset de referencia: Credit Card Fraud Detection, ULB/Kaggle).
- Horst, A. M., Hill, A. P., & Gorman, K. B. (2020). *palmerpenguins: Palmer Archipelago (Antarctica) penguin data*. https://allisonhorst.github.io/palmerpenguins/ ; datos originales asociados al Palmer LTER.
- Pace, R. K., & Barry, R. (1997). Sparse spatial autoregressions. *Statistics & Probability Letters*, 33(3), 291–297. (base de California Housing).

---

## 2. Referencias metodológicas (selección)

- Cleveland, R. B., Cleveland, W. S., McRae, J. E., & Terpenning, I. (1990). STL: A seasonal-trend decomposition procedure based on loess. *J. Off. Stat.*
- Bai, J., & Perron, P. (1998, 2003). Estimating and testing linear models with multiple structural changes. *Econometrica* / *J. Appl. Econometrics* (según implementación utilizada).
- Killick, R., Fearnhead, P., & Eckley, I. A. (2012). Optimal detection of changepoints with a linear computational cost (PELT). *JASA*. (si `ruptures`/PELT disponible).
- Hyndman, R. J., & Koehler, A. B. (2006). Another look at measures of forecast accuracy. *International Journal of Forecasting* (MASE).
- Simpson, E. H. (1951). The interpretation of interaction in contingency tables. *JRSS B*.
- Mundlak, Y. (1978). On the pooling of time series and cross section data. *Econometrica* (descomposición within-between, según uso).
- Hausman, J. A. (1978). Specification tests in econometrics. *Econometrica* (comparación FE/RE, cuando aplica).
- Breiman, L. (2001). Random Forests. *Machine Learning*; Liu, F. T., Ting, K. M., & Zhou, Z.-H. (2008). Isolation Forest. *ICDM*.
- Saito, T., & Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLOS ONE*.
- Moran, P. A. P. (1950). Notes on continuous stochastic phenomena. *Biometrika* (autocorrelación espacial; si se calcula).
- Oster, E. (2019). Unobservable selection and coefficient stability: Theory and evidence. *JBES* (sensibilidad; interpretación exploratoria).
- Athey, S., & Wager, S. (2019). Estimating treatment effects with causal forests. *PNAS* (si Causal Forest/econml disponible).
- Wager, S., & Athey, S. (2018). Estimation and inference of heterogeneous treatment effects using random forests. *JASA*.

> Las referencias anteriores se incluyen como marco metodológico; la aplicabilidad concreta depende de las funciones/modelos efectivamente ejecutados en cada notebook y entorno.

---

## 3. Apéndice metodológico: parámetros y criterios por historia

### Historia 1 — Serie temporal + cambio estructural (CO₂ Mauna Loa)
- **Datos/variables:** serie mensual derivada de `data/raw/co2_mm_mlo.csv` (selección de columna de valor y construcción de índice temporal según el notebook).
- **Descomposición:** STL con periodo estacional 12 (mensual) y ajuste robusto (parámetros en notebook: `period=12, seasonal=13, robust=True`).
- **Tasas/pendientes:** crecimiento interanual (`diff` con periodo 12) y pendientes por ventanas móviles OLS (p. ej. ventana 120 meses = 10 años) sobre la tendencia; suavizado auxiliar (Savitzky–Golay) para visualización.
- **Contraste pre/post:** comparación de medias de pendientes en ventanas pre-2000 y post-2000 con IC bootstrap e inferencia (Welch) según funciones de `src/stats_helpers.py`.
- **Quiebres:** intento de detección con PELT (`ruptures`, si disponible) y/o Bai-Perron (`statsmodels`, según disponibilidad/API); selección de breakpoint usada en ajuste por tramos con regla explícita en el notebook y **fallback documentado** si no hay estimación automática disponible.
- **Modelo por tramos:** regresión lineal por segmentos alrededor del breakpoint seleccionado.
- **Validación:** *rolling-origin forecast* (ventana/horizonte/paso definidos en notebook, p. ej. ARIMA(1,1,1) como baseline) y métricas como MAE/MASE cuando se calculan.
- **Diagnósticos:** pruebas/estadísticos sobre residuos (p. ej. Ljung-Box, Breusch-Pagan, normalidad/asimetría-curtosis) reportados según ejecución.
- **Criterio de reporte:** solo se afirman magnitudes/fechas/métricas calculadas en la ejecución.

### Historia 2 — Comparación multivariable + paradoja de Simpson (Gapminder)
- **Datos/variables:** `country, continent, year, lifeExp, gdpPercap, pop`; transformación `log_gdp = log(gdpPercap)`.
- **Especificaciones comparadas:** OLS *pooled* (`lifeExp ~ log_gdp`), FE por continente (`+ C(continent)`), *between* (promedios por continente), FE por país/año según celdas, y descomposición *within-between* (Mundlak) vía `src/stats_helpers.py`.
- **Modelos mixtos/jerárquicos:** cuando se ejecutan, MixedLM con agrupaciones (continente/país o combinaciones) y componentes de varianza/ICC según implementación disponible.
- **Comparación FE/RE:** test de Hausman cuando la especificación y objetos son compatibles (reporte condicionado a disponibilidad).
- **Validación:** Leave-One-Country-Out (LOOCV por país) con la especificación aproximada implementada en el notebook (documentada en código).
- **Criterio de reporte:** coeficientes/IC/diagnósticos y ordenamientos entre niveles según resultados calculados; interpretación asociacional/condicional.

### Historia 3 — Outliers + detección de anomalías (fraude, simulación/pipeline por defecto)
- **Datos/variables:** `Time, V1–V28, Amount, Class` desde `data/raw/creditcard.csv` (proxy sintético por defecto o dataset real si se reemplaza).
- **Preprocesamiento:** uso de `V1–V28`, `log1p(Amount)` y escalado de `Time` según notebook.
- **Partición:** **split temporal** (p. ej. entrenamiento con `Time < 86400`, prueba con el resto) para evitar fuga temporal.
- **No supervisado:** Isolation Forest (`n_estimators` y `contamination` según notebook; `contamination` acotada a rango válido y alineada a prevalencia de entrenamiento cuando aplica).
- **Supervisado (opcional):** XGBoost si está instalado; ponderación por desbalance (`scale_pos_weight`) y evaluación en el mismo test temporal.
- **Métricas:** PR-AUC/Average Precision, curva Precision-Recall, matriz de confusión, Recall/Precision en umbral operativo, Fβ (p. ej. F2) y **costo esperado** con matriz `C_FN/C_FP` definida en notebook (ej. C_FN=100, C_FP=1).
- **Umbral:** selección por minimización de costo esperado sobre *scores* (convención: mayor score ⇒ más anómalo) y análisis de sensibilidad a `contamination`.
- **Criterio de reporte:** resultados válidos para el dataset cargado; con proxy sintético, **no extrapolables** a desempeño real.

### Historia 4 — Drill-down jerárquico + descomposición de varianza (Palmer Penguins)
- **Datos/variables:** morfometría y factores (`species, island, sex, year`, etc.) con manejo de valores faltantes según análisis.
- **Exploración jerárquica:** agregaciones y comparaciones por niveles (isla/especie/sexo), tablas de contingencia para evaluar diseño (balance/combinaciones presentes).
- **Partición de varianza:** ICC "naked" por agrupaciones (especie, isla, año) y modelos/ANOVA o modelos mixtos según celdas ejecutadas; tamaños de efecto (p. ej. Cohen's d, η² parcial) cuando se calculan.
- **Modelado:** especificaciones mixtas/OLS con efectos según disponibilidad y estructura del diseño (p. ej. especie fija + isla aleatoria) y reporte de componentes/ICC condicionales cuando aplica.
- **Validación:** Leave-One-Island-Out (u otra validación por grupo implementada) con métricas RMSE/R² según ejecución.
- **Criterio de reporte:** magnitudes y conclusiones derivadas de los cálculos realizados; atención explícita a confusión por diseño incompleto.

### Historia 5 — Intersección multivariable + confounding espacial (California Housing)
- **Datos/variables:** variables de vivienda/ingreso y coordenadas (`MedInc`, `HouseAge`, `AveRooms`, `AveBedrms`, `Population`, `AveOccup`, `Latitude`, `Longitude`, `MedHouseVal`).
- **Modelos base:** OLS simple y OLS con controles/ubicación; inspección de residuos y mapas.
- **Diagnóstico espacial:** Moran's I sobre residuos (k vecinos) **solo si** `libpysal/esda` disponibles y resultado finito.
- **Modelos espaciales/ML (opcionales):** SAR/spatial lag (`spreg/libpysal`), SHAP, Causal Forest (`econml`) **solo si** dependencias disponibles; heterogeneidad explorada con PDP y, cuando aplica, estimaciones condicionales.
- **Sensibilidad:** Oster δ como análisis exploratorio de sensibilidad a confounders no observados (basado en comparación de coeficientes/R² entre especificaciones), no como prueba causal.
- **Validación:** *Spatial Block CV* cuando está disponible; en su defecto, fallback documentado (p. ej. KFold) con reporte explícito del modo de validación.
- **Criterio de reporte:** interpretación asociacional/condicional y predictiva; no se afirman diagnósticos o efectos avanzados no calculados en la ejecución.

---

## 4. Niveles de entorno y reproducibilidad de resultados

- **Núcleo (declarado y reproducible con `requirements.txt`):** `pandas, numpy, scipy, matplotlib, seaborn, plotly, scikit-learn, statsmodels, jupyter/nbconvert/ipykernel`. Debe permitir ejecutar las 5 historias con salidas base y degradación controlada cuando falten opcionales.
- **Completo (opcional):** añade dependencias como `ruptures`, `prophet`, `pmdarima`, `xgboost`, `shap`, `libpysal`, `esda`, `splot`, `spreg`, `econml` (según historia). Habilita análisis adicionales; los resultados **deben** regenerarse y documentarse en ese entorno si se citan.

**Recomendación de trazabilidad:** al reportar resultados, indicar explícitamente el entorno (núcleo/completo), fecha de ejecución y si el dataset de fraude fue proxy sintético o real.
