<<<<<<< HEAD
# 5-Historias-que-contar
=======
# Storytelling con Datos: 5 Arquetipos, 5 Historias

**Curso:** Ciencia de Datos Avanzada — **Facultad:** MATCOM, Universidad de La Habana  
**Entrega:** 2026-11-20

Proyecto con 5 historias basadas en datos (una por arquetipo), notebooks reproducibles y un informe crítico. Este README describe **únicamente las formas funcionales disponibles en el estado actual del repositorio**.

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

| Historia | Arquetipo | Dataset (en `data/raw/`) | Enfoque de la historia |
|---|---|---|---|
| 1. La curva que no miente | Serie temporal + cambio estructural | CO₂ Mauna Loa (`co2_mm_mlo.csv`) | Tendencia, estacionalidad, quiebres y aceleración |
| 2. Cuando el promedio miente | Comparación multivariable + paradoja de Simpson | Gapminder (`gapminder.csv`) | Pooled vs within/between, agregación y heterogeneidad |
| 3. La aguja en el pajar financiero | Outliers + detección de anomalías | Credit Card Fraud (`creditcard.csv`, proxy sintético reproducible generado localmente por defecto) | Desbalance, métricas PR/costo, validación temporal, no supervisado vs supervisado |
| 4. Pingüinos como termómetros | Drill-down jerárquico + descomposición de varianza | Palmer Penguins (`penguins.csv`) | Jerarquías, varianza por niveles, diseño no balanceado |
| 5. ¿Ingreso causa precio o es la playa? | Intersección multivariable / confounding espacial | California Housing (`california_housing.csv`) | Efectos parciales, dependencia espacial, heterogeneidad y validación |

- **Informe crítico:** [`INFORME_CRITICO_ARQUETIPOS.md`](INFORME_CRITICO_ARQUETIPOS.md)
- **Notebooks:** [`notebooks/`](notebooks/)
- **Código reutilizable:** [`src/`](src/)
- **Script de datos:** [`data/download_data.py`](data/download_data.py)

---

## Estructura principal

```text
.
├── README.md
├── INFORME_CRITICO_ARQUETIPOS.md
├── build_all.py
├── data/
│   ├── download_data.py
│   └── raw/                         # Datasets incluidos
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
