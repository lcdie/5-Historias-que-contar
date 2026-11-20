# Storytelling con Datos: 5 Arquetipos, 5 Historias

**Curso:** Ciencia de Datos Avanzada — **Facultad:** MATCOM, Universidad de La Habana  
**Autor:** Luis Calderón Denis  
**Entrega:** 2026-11-20

Proyecto con **5 historias basadas en datos** (una por arquetipo), notebooks reproducibles, HTML ejecutado e informe crítico. Este README describe **únicamente las formas funcionales disponibles en el estado actual del repositorio** y dónde encontrar cada entregable.

## Entregables y cumplimiento de la consigna

- **5 arquetipos / 5 historias con datos:** desarrolladas en `notebooks/01`–`05` y disponibles ya ejecutadas en `docs_html/`.
- **≥ 2 cuartillas por historia:** cada notebook incluye narrativa analítica extensa (contexto, desarrollo, evidencia con datos, interpretación y cierre), coherente con su dataset; la versión de lectura recomendada es el HTML ejecutado correspondiente.
- **Informe crítico por historia:** [`INFORME_CRITICO_ARQUETIPOS.md`](INFORME_CRITICO_ARQUETIPOS.md) justifica el arquetipo elegido y argumenta por qué cada caso es una historia con datos.
- **Rigor y coherencia con el dataset:** cada historia trabaja sobre el dataset indicado, explicita supuestos/limitaciones y fundamenta conclusiones en evidencia computada; ver además [`FUENTES_Y_DATOS.md`](FUENTES_Y_DATOS.md).
- **Reporte técnico del proyecto:** [`REPORTE_TECNICO.md`](REPORTE_TECNICO.md).

---

## Formas funcionales de ver el proyecto (estado actual)

### 1) Ver el proyecto ya renderizado en HTML (recomendado)
**Estado:** funcional y listo.

- Abre localmente: [`docs_html/index.html`](docs_html/index.html)
- Contenido: las 5 historias/notebooks con narrativa, tablas y salidas/gráficos **ejecutados**.
- No requiere instalar dependencias ni ejecutar código para lectura.

Páginas incluidas:
- `docs_html/01_series_temporales_co2.html`
- `docs_html/02_comparacion_gapminder.html`
- `docs_html/03_outliers_fraude.html`
- `docs_html/04_drilldown_penguins.html`
- `docs_html/05_interseccion_california.html`

### 2) Ejecutar los notebooks localmente con Python (venv + pip)
**Estado:** funcional con el stack núcleo del proyecto.

> Los datasets base están incluidos en `data/raw/` (CO₂, Gapminder, Penguins, California Housing). `data/raw/creditcard.csv` **no se incluye** en el repositorio; puede generarse localmente como **proxy sintético reproducible** (mismo esquema que la referencia ULB/Kaggle) con `python data/download_data.py`, o reemplazarse por el dataset real en `data/raw/creditcard.csv`.

```bash
# Desde la raíz del proyecto
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip

# Dependencias núcleo (suficientes para ejecutar las 5 historias con fallbacks cuando falten extras)
python -m pip install pandas numpy matplotlib seaborn plotly scikit-learn scipy statsmodels jupyter nbconvert ipykernel

# (Opcional) descargar/regenerar/verificar datasets
python data/download_data.py

# Abrir notebooks
jupyter lab notebooks/
# o
jupyter notebook notebooks/
```

**Notas de ejecución:**
- Las notebooks están diseñadas para ejecutarse con las dependencias núcleo; cuando faltan paquetes opcionales (p. ej. `ruptures`, `xgboost`, `shap`, `libpysal/spreg`, `econml`), incluyen rutas de degradación/fallback o se omite el bloque específico.
- Los notebooks fuente no guardan outputs embebidos; las salidas ejecutadas están disponibles en `docs_html/`.

### 3) Regenerar el HTML ejecutado (build local)
**Estado:** funcional.

```bash
# Con el entorno activado (o usando .venv/bin/python)
python build_all.py
```

- Genera/actualiza `docs_html/` (intenta ejecutar cada notebook y aplica fallback a HTML sin ejecutar por notebook si alguna celda falla en otro entorno).
- Genera configuraciones auxiliares de Binder en `.github/` y `runtime.txt`/`jupyterlite_config.json` si aplica.
- **JupyterLite (`docs_lite/`) no se genera en este entorno** si no está disponible la herramienta; en ese caso el build lo omite de forma segura.

---

## Opciones no incluidas como funcionales en este estado

Para evitar confusión, **no se listan como opciones de visualización/ejecución funcionales ahora mismo**:
- **JupyterLite (`docs_lite/`)**: no está generado en el repositorio (no hay sitio estático JupyterLite listo para abrir).
- **Enlaces/badges externos dependientes de publicación** (Binder, GitHub Pages público, Codespaces con URL del repositorio): requieren subir el proyecto a un repositorio propio y, en su caso, configuración/compilación remota; no son formas de visualización funcionales en el estado local actual.

> Los archivos de configuración para despliegue/entornos alternativos (`Dockerfile`, `docker-compose.yml`, `.devcontainer/`, `.github/workflows/deploy.yml`, `environment.yml`, `environment-lite.yml`) se conservan en el repositorio, pero no se presentan como vías verificadas/funcionales de visualización en este estado.

---

## Contenido del proyecto

| Historia | Arquetipo | Dataset (en `data/raw/`) | Enfoque de la historia | Notebook | Lectura (HTML) |
|---|---|---|---|---|---|
| 1. La curva que no miente | Serie temporal + cambio estructural | CO₂ Mauna Loa (`co2_mm_mlo.csv`) | Tendencia, estacionalidad, quiebres y aceleración | [`notebooks/01_series_temporales_co2.ipynb`](notebooks/01_series_temporales_co2.ipynb) | [`docs_html/01_series_temporales_co2.html`](docs_html/01_series_temporales_co2.html) |
| 2. Cuando el promedio miente | Comparación multivariable + paradoja de Simpson | Gapminder (`gapminder.csv`) | Pooled vs within/between, agregación y heterogeneidad | [`notebooks/02_comparacion_gapminder.ipynb`](notebooks/02_comparacion_gapminder.ipynb) | [`docs_html/02_comparacion_gapminder.html`](docs_html/02_comparacion_gapminder.html) |
| 3. La aguja en el pajar financiero | Outliers + detección de anomalías | Credit Card Fraud (`creditcard.csv`, proxy sintético reproducible generado localmente por defecto) | Desbalance, métricas PR/costo, validación temporal, no supervisado vs supervisado | [`notebooks/03_outliers_fraude.ipynb`](notebooks/03_outliers_fraude.ipynb) | [`docs_html/03_outliers_fraude.html`](docs_html/03_outliers_fraude.html) |
| 4. Pingüinos como termómetros | Drill-down jerárquico + descomposición de varianza | Palmer Penguins (`penguins.csv`) | Jerarquías, varianza por niveles, diseño no balanceado | [`notebooks/04_drilldown_penguins.ipynb`](notebooks/04_drilldown_penguins.ipynb) | [`docs_html/04_drilldown_penguins.html`](docs_html/04_drilldown_penguins.html) |
| 5. ¿Ingreso causa precio o es la playa? | Intersección multivariable / confounding espacial | California Housing (`california_housing.csv`) | Efectos parciales, dependencia espacial, heterogeneidad y validación | [`notebooks/05_interseccion_california.ipynb`](notebooks/05_interseccion_california.ipynb) | [`docs_html/05_interseccion_california.html`](docs_html/05_interseccion_california.html) |

- **Informe crítico (arquetipos/narrativa):** [`INFORME_CRITICO_ARQUETIPOS.md`](INFORME_CRITICO_ARQUETIPOS.md)
- **Fuentes y datos:** [`FUENTES_Y_DATOS.md`](FUENTES_Y_DATOS.md)
- **Reporte técnico del proyecto:** [`REPORTE_TECNICO.md`](REPORTE_TECNICO.md)
- **Código reutilizable:** [`src/`](src/)
- **Script de datos:** [`data/download_data.py`](data/download_data.py)

---

## Estructura principal

```text
.
├── README.md
├── INFORME_CRITICO_ARQUETIPOS.md
├── REPORTE_TECNICO.md
├── FUENTES_Y_DATOS.md
├── requirements.txt
├── build_all.py
├── data/
│   ├── download_data.py
│   └── raw/                         # Datasets base incluidos (creditcard.csv se genera localmente)
├── notebooks/                       # 5 historias
├── src/                             # viz, stats_helpers, narrative
├── docs_html/                       # HTML estático con salidas ejecutadas (funcional)
├── reports/                         # Figuras/artefactos generados en ejecuciones
├── environment.yml
├── environment-lite.yml
├── Dockerfile
├── docker-compose.yml
├── .devcontainer/
└── .github/
```
