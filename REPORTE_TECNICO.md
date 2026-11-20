# Reporte técnico del proyecto
## Storytelling con Datos: 5 arquetipos, 5 historias

**Fecha:** 2026-11-20  
**Contexto:** Proyecto académico (MATCOM, Ciencia de Datos Avanzada). El objetivo es comunicar hallazgos mediante cinco historias con datos, cada una alineada a un arquetipo analítico, con énfasis en trazabilidad (dato → método → hallazgo → límite), reproducibilidad y coherencia entre narrativa y resultados ejecutados.

---

## 1. Objetivo y alcance

### 1.1 Objetivo
Construir un conjunto reproducible de notebooks, visualizaciones y documentación que sustenten 5 historias con datos, justificadas metodológicamente y coherentes con los datasets utilizados.

### 1.2 Alcance entregado
- **5 notebooks** (`notebooks/01`–`05`) con desarrollo analítico, narrativa y visualización.
- **Informe crítico** (`INFORME_CRITICO_ARQUETIPOS.md`) con justificación por arquetipo e interpretación del carácter “historia con datos”, acotada al alcance inferencial y a la evidencia ejecutada.
- **Documentación de datos y metodología:** `FUENTES_Y_DATOS.md` y `REFERENCIAS_Y_APENDICE_METODOLOGICO.md` (fuentes, procedencia, parámetros/criterios por historia).
- **Código auxiliar** en `src/` (`viz.py`, `stats_helpers.py`, `narrative.py`, `__init__.py`).
- **Pipeline de datos** en `data/download_data.py` (obtención/verificación/preparación y generación local del proxy de fraude cuando aplica).
- **Build de salida estática** con `build_all.py` para generar `docs_html/` (HTML ejecutado).
- **Configuraciones de entorno/despliegue** conservadas en el repositorio (conda/docker/devcontainer/CI, etc.) como soporte de portabilidad.

### 1.3 Fuera de alcance / condicionantes
- Publicación remota automática no configurada en este estado.
- `docs_lite/` (JupyterLite) no generado si la herramienta no está disponible.
- `data/raw/creditcard.csv` no versionado (generable localmente como proxy sintético por defecto o reemplazable por dataset real con el mismo esquema).
- Componentes que dependen de paquetes opcionales solo se reportan cuando se ejecutan; en entorno núcleo se aplica degradación controlada y reporte explícito de indisponibilidad.

---

## 2. Arquitectura del repositorio

| Componente | Ruta(s) | Función |
|---|---|---|
| Narrativa/entregables | `README.md`, `INFORME_CRITICO_ARQUETIPOS.md`, `REPORTE_TECNICO.md` | Guía de uso, justificación crítica y documentación técnica |
| Datos y procedencia | `FUENTES_Y_DATOS.md`, `REFERENCIAS_Y_APENDICE_METODOLOGICO.md`, `data/download_data.py`, `data/raw/` | Trazabilidad de insumos y criterios metodológicos |
| Análisis | `notebooks/01`–`05` | Historias, cómputos, visualizaciones y conclusiones trazables |
| Soporte reusable | `src/` | Visualización, utilidades estadísticas y helpers narrativos |
| Salida ejecutada | `docs_html/` | Evidencia renderizada (narrativa + código + resultados) |
| Construcción | `build_all.py` | Ejecución/conversión a HTML e índice |

---

## 3. Datos y preparación

### 3.1 Datasets por historia
1. **CO₂ Mauna Loa** (`data/raw/co2_mm_mlo.csv`) — serie temporal/cambio estructural.  
2. **Gapminder** (`data/raw/gapminder.csv`) — comparación multivariable y composición/Simpson.  
3. **Credit Card Fraud** (`data/raw/creditcard.csv`, **no versionado**) — outliers/anomalías. Por defecto proxy sintético reproducible (mismo esquema de referencia ULB/Kaggle); sustituible por dataset real.  
4. **Palmer Penguins** (`data/raw/penguins.csv`) — drill-down jerárquico/descomposición de varianza.  
5. **California Housing** (`data/raw/california_housing.csv`) — intersección multivariable/confounding espacial (observacional).

### 3.2 Script de datos (`data/download_data.py`)
- Centraliza obtención/verificación/preparación de insumos en `data/raw/`.
- Genera `creditcard.csv` sintético cuando falta, para permitir ejecución reproducible sin credenciales.
- La interpretación de la Historia 3 depende del insumo cargado (proxy sintético vs real).

### 3.3 Consideraciones de coherencia de datos
- Las conclusiones deben ser consistentes con el archivo efectivamente analizado y con sus limitaciones (medición, agregación, anonimización, antigüedad, diseño de muestreo, etc.).
- Para fraude, el uso de proxy implica un alcance de **simulación/pipeline metodológico**, no de desempeño en producción real.

---

## 4. Entornos, dependencias y niveles de resultados

### 4.1 Entorno núcleo (declarado)
- Instalación: `venv + pip` con `requirements.txt`.
- Paquetes base: `numpy`, `pandas`, `scipy`, `matplotlib`, `seaborn`, `plotly`, `scikit-learn`, `statsmodels`, `jupyter`, `notebook`, `nbconvert`, `ipykernel`.
- Objetivo: ejecutar las 5 historias y producir resultados base verificables, con manejo explícito de funcionalidades no disponibles.

### 4.2 Entorno completo (opcional)
- Añade dependencias según necesidad analítica (p. ej. `ruptures`, `prophet`, `pmdarima`, `xgboost`, `shap`, `libpysal`, `esda`, `splot`, `spreg`, `econml`).
- Los resultados dependientes de estas librerías deben generarse y reportarse únicamente si el entorno las incluye y la ejecución las produce.

### 4.3 Degradación controlada y alineación evidencia–narrativa
- Los notebooks incluyen comprobaciones/fallbacks para dependencias o pasos opcionales.
- Regla de rigor: **no afirmar resultados no calculados** (p. ej. diagnósticos/modelos espaciales o comparadores supervisados ausentes). La narrativa debe reflejar el estado real de la ejecución.

---

## 5. Proceso de construcción y validación

### 5.1 Build (`build_all.py`)
1. Configura entorno de ejecución (`PYTHONPATH`, directorios de caché, etc.).
2. Convierte/ejecuta notebooks a HTML en `docs_html/` con `jupyter nbconvert --execute` y timeout.
3. Aplica fallback a conversión sin ejecución por notebook en caso de fallo puntual.
4. Genera `docs_html/index.html`.
5. Omite pasos no disponibles (p. ej. JupyterLite) de forma controlada.

### 5.2 Validación esperada
- `docs_html/` contiene las 5 salidas HTML y el índice.
- Las métricas/diagnósticos mostrados en HTML corresponden a la ejecución realizada.
- Diferencias entre entorno núcleo y completo se reflejan en disponibilidad de resultados, no en afirmaciones ficticias.

### 5.3 Reproducibilidad operativa
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python data/download_data.py   # genera creditcard.csv proxy si falta
python build_all.py            # regenera docs_html/
```

---

## 6. Decisiones técnicas y calidad

- **Trazabilidad:** notebooks como fuente de cómputo y narrativa; `docs_html/` como evidencia ejecutada; apéndice metodológico con parámetros/criterios.
- **Robustez:** manejo de dependencias opcionales y rutas de fallback para mantener ejecutabilidad del núcleo.
- **Separación de responsabilidades:** datos (`data/`), utilidades (`src/`), análisis (`notebooks/`), documentación (md) y publicación local (`docs_html/`, `build_all.py`).

## 7. Limitaciones conocidas

- Resultados avanzados no disponibles sin dependencias opcionales.
- Historia 3 basada por defecto en proxy sintético (alcance metodológico, no externo).
- Portabilidad de todos los targets alternativos (Docker/devcontainer/CI/JupyterLite) no verificada de extremo a extremo en este entorno.
- La interpretación causal en datos observacionales (especialmente H2/H5) está limitada por identificación y supuestos; los notebooks priorizan asociaciones condicionales, diagnósticos y sensibilidad cuando aplica.

## 8. Resumen ejecutivo

El proyecto integra cinco historias con datos en una estructura reproducible y documentada, con un flujo de build que produce evidencia HTML ejecutada. La versión actual prioriza la alineación entre narrativa y resultados efectivamente computados en el entorno declarado, la explicitación de niveles núcleo/completo, y la delimitación del alcance (incluida la simulación/pipeline en la historia de fraude por defecto), fortaleciendo la solidez metodológica y la trazabilidad del entregable.
