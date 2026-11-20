# Storytelling con Datos: 5 Arquetipos, 5 Historias

**Curso:** Ciencia de Datos Avanzada — **Facultad:** MATCOM, Universidad de La Habana  
**Autor:** Luis Calderón Denis  
**Entrega:** 2026-11-20

Proyecto con **5 historias basadas en datos** (una por arquetipo), notebooks reproducibles, informe crítico y salida HTML ejecutada. Este README describe las formas **funcionales** de ver/ejecutar el proyecto en su estado actual y la política de reproducibilidad (entorno núcleo vs completo).

## Cumplimiento de la consigna (resumen)

- **5 arquetipos / 5 historias con datos:** desarrolladas en `notebooks/01`–`05` y disponibles en `docs_html/` como HTML ejecutado.
- **Informe crítico:** [`INFORME_CRITICO_ARQUETIPOS.md`](INFORME_CRITICO_ARQUETIPOS.md) justifica, por historia, el arquetipo elegido y por qué constituye una historia con datos (con criterios de trazabilidad y alcance inferencial).
- **Coherencia narrativa y evidencia:** los notebooks vinculan dato → método → hallazgo → límite. Las afirmaciones cuantitativas deben corresponder a los resultados efectivamente producidos en la ejecución del entorno declarado (ver “Niveles de ejecución”).
- **Fuentes, datos y metodología:** [`FUENTES_Y_DATOS.md`](FUENTES_Y_DATOS.md) y [`REFERENCIAS_Y_APENDICE_METODOLOGICO.md`](REFERENCIAS_Y_APENDICE_METODOLOGICO.md).
- **Reporte técnico:** [`REPORTE_TECNICO.md`](REPORTE_TECNICO.md).

> **Extensión por historia:** cada notebook integra contexto, desarrollo analítico, visualización, interpretación y cierre con limitaciones/próximos pasos. La lectura de extensión y evidencia se realiza preferentemente sobre el HTML ejecutado (`docs_html/`), que incluye narrativa, código y salidas.

---

## Niveles de ejecución y alineación evidencia–narrativa

| Nivel | Dependencias | Qué garantiza | Qué puede no incluir |
|---|---|---|---|
| **Núcleo (declarado)** | `requirements.txt` (pandas, numpy, scipy, matplotlib, seaborn, plotly, scikit-learn, statsmodels, jupyter/nbconvert/ipykernel) | Ejecución de las 5 historias con pipeline base, métricas/diagnósticos principales disponibles en estas librerías y **degradación controlada** cuando falten opcionales. | Resultados que dependen de paquetes opcionales (p. ej. `ruptures`, `prophet`, `pmdarima`, `xgboost`, `shap`, `libpysal/esda/splot/spreg`, `econml`). |
| **Completo (opcional)** | Núcleo + paquetes opcionales según historia | Análisis complementarios (detección de quiebres avanzada, modelos supervisados/interpretabilidad, modelos espaciales, estimaciones de heterogeneidad condicional, etc.). | — (si están instalados y se reejecuta). |

**Regla:** si un componente no se calcula en la ejecución (por dependencia ausente o condición no satisfecha), el notebook/HTML debe indicarlo y **no** afirmarlo como resultado. `docs_html/` debe regenerarse en el entorno que se quiera reportar.

---

## Formas funcionales de ver y ejecutar el proyecto

### 1) Ver el proyecto ya renderizado en HTML (recomendado)
**Estado:** funcional.

- Abrir: [`docs_html/index.html`](docs_html/index.html)
- Contenido: las 5 historias/notebooks con narrativa, tablas y salidas/gráficos ejecutados.
- No requiere instalar dependencias para lectura.

Páginas:
- [`docs_html/01_series_temporales_co2.html`](docs_html/01_series_temporales_co2.html)
- [`docs_html/02_comparacion_gapminder.html`](docs_html/02_comparacion_gapminder.html)
- [`docs_html/03_outliers_fraude.html`](docs_html/03_outliers_fraude.html)
- [`docs_html/04_drilldown_penguins.html`](docs_html/04_drilldown_penguins.html)
- [`docs_html/05_interseccion_california.html`](docs_html/05_interseccion_california.html)

### 2) Ejecutar localmente con Python (venv + pip, entorno núcleo)
**Estado:** funcional con el stack núcleo.

Datasets base incluidos en `data/raw/`: `co2_mm_mlo.csv`, `gapminder.csv`, `penguins.csv`, `california_housing.csv`.  
`data/raw/creditcard.csv` **no se versiona**: por defecto se genera localmente como **proxy sintético reproducible** (mismo esquema de referencia ULB/Kaggle) con `python data/download_data.py`, o puede reemplazarse por el dataset real en la misma ruta. Cuando se usa proxy sintético, la Historia 3 se interpreta como **simulación/pipeline metodológico** (sin extrapolación a desempeño real).

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# (Opcional) verificar/regenerar datasets; genera creditcard.csv proxy si falta
python data/download_data.py

# Ejecutar notebooks de forma interactiva
jupyter lab notebooks/
# o
jupyter notebook notebooks/
```

### 3) Regenerar el HTML ejecutado (build local)
**Estado:** funcional.

```bash
# Con el entorno activado (núcleo o completo)
python build_all.py
```

- Ejecuta notebooks y genera/actualiza `docs_html/` (con fallback a conversión sin ejecución por notebook si alguna celda falla).
- **JupyterLite (`docs_lite/`)** se omite si la herramienta no está disponible.

---

## Opciones no incluidas como funcionales en este estado

- **JupyterLite (`docs_lite/`)**: no generado/listo por defecto en este entorno.
- **Publicaciones remotas** (Binder, GitHub Pages público, etc.): requieren configuración/publicación externa; no se presentan como vías locales verificadas aquí.
- Archivos de entorno/despliegue alternativos (`Dockerfile`, `docker-compose.yml`, `.devcontainer/`, `.github/workflows/deploy.yml`, `environment.yml`, `environment-lite.yml`) se conservan como soporte de portabilidad, sin garantizarse como flujos verificados en este estado.

---

## Contenido del proyecto

| Historia | Arquetipo | Dataset (en `data/raw/`) | Enfoque | Notebook | HTML |
|---|---|---|---|---|---|
| 1. La curva que no miente | Serie temporal + cambio estructural | CO₂ Mauna Loa (`co2_mm_mlo.csv`) | Tendencia, estacionalidad, quiebres, tasas y validación temporal | [`notebooks/01_series_temporales_co2.ipynb`](notebooks/01_series_temporales_co2.ipynb) | [`docs_html/01_series_temporales_co2.html`](docs_html/01_series_temporales_co2.html) |
| 2. Cuando el promedio miente | Comparación multivariable + paradoja de Simpson/composición | Gapminder (`gapminder.csv`) | Asociaciones pooled/within/between, heterogeneidad y agregación | [`notebooks/02_comparacion_gapminder.ipynb`](notebooks/02_comparacion_gapminder.ipynb) | [`docs_html/02_comparacion_gapminder.html`](docs_html/02_comparacion_gapminder.html) |
| 3. La aguja en el pajar financiero | Outliers + detección de anomalías | Credit Card Fraud (`creditcard.csv`, **proxy sintético por defecto**, no versionado) | Desbalance, PR/costo, umbral operativo, split temporal (simulación/pipeline) | [`notebooks/03_outliers_fraude.ipynb`](notebooks/03_outliers_fraude.ipynb) | [`docs_html/03_outliers_fraude.html`](docs_html/03_outliers_fraude.html) |
| 4. Pingüinos como termómetros | Drill-down jerárquico + descomposición de varianza | Palmer Penguins (`penguins.csv`) | Niveles, ICC/efectos, diseño no balanceado y validación por grupos | [`notebooks/04_drilldown_penguins.ipynb`](notebooks/04_drilldown_penguins.ipynb) | [`docs_html/04_drilldown_penguins.html`](docs_html/04_drilldown_penguins.html) |
| 5. ¿Ingreso y precio: asociación o confounding espacial? | Intersección multivariable + confounding espacial (observacional) | California Housing (`california_housing.csv`) | Asociaciones condicionales, diagnóstico espacial, heterogeneidad y sensibilidad | [`notebooks/05_interseccion_california.ipynb`](notebooks/05_interseccion_california.ipynb) | [`docs_html/05_interseccion_california.html`](docs_html/05_interseccion_california.html) |

---

## Documentación clave

- Informe crítico: [`INFORME_CRITICO_ARQUETIPOS.md`](INFORME_CRITICO_ARQUETIPOS.md)
- Fuentes y datos: [`FUENTES_Y_DATOS.md`](FUENTES_Y_DATOS.md)
- Referencias y apéndice metodológico (parámetros/criterios): [`REFERENCIAS_Y_APENDICE_METODOLOGICO.md`](REFERENCIAS_Y_APENDICE_METODOLOGICO.md)
- Reporte técnico: [`REPORTE_TECNICO.md`](REPORTE_TECNICO.md)
- Código reutilizable: [`src/`](src/)
- Script de datos: [`data/download_data.py`](data/download_data.py)
- Build: [`build_all.py`](build_all.py)

## Estructura principal

```text
.
├── README.md
├── INFORME_CRITICO_ARQUETIPOS.md
├── REPORTE_TECNICO.md
├── FUENTES_Y_DATOS.md
├── REFERENCIAS_Y_APENDICE_METODOLOGICO.md
├── requirements.txt
├── build_all.py
├── data/
│   ├── download_data.py
│   └── raw/                  # Datasets base; creditcard.csv se genera localmente
├── notebooks/                # 5 historias
├── src/                      # viz, stats_helpers, narrative
├── docs_html/                # HTML estático con salidas ejecutadas
├── reports/
└── (configs de entorno/despliegue)
```
