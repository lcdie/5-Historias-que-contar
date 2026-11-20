# Reporte técnico del proyecto
## Storytelling con Datos: 5 arquetipos, 5 historias

**Fecha:** 2026-11-20  
**Contexto:** Proyecto académico (MATCOM, Ciencia de Datos Avanzada) orientado a desarrollar y presentar 5 historias basadas en datos, cada una asociada a un arquetipo analítico distinto, con énfasis en rigor técnico, coherencia narrativa y reproducibilidad.

---

## 1. Objetivo y alcance

### 1.1 Objetivo general
Construir un proyecto reproducible que combine análisis de datos y narrativa para comunicar hallazgos de forma rigurosa, utilizando cinco datasets y cinco arquetipos de análisis complementarios.

### 1.2 Alcance entregado
- **5 notebooks** (`notebooks/01`–`05`) con el desarrollo analítico y narrativo de cada historia.
- **Informe crítico** (`INFORME_CRITICO_ARQUETIPOS.md`) que justifica el arquetipo y por qué cada caso constituye una “historia con datos”.
- **Código auxiliar reutilizable** en `src/` (visualización, utilidades estadísticas y helpers narrativos).
- **Pipeline de datos** en `data/download_data.py` para obtener/verificar/generar datasets.
- **Build de visualización estática** mediante `build_all.py`, con salida ejecutada en `docs_html/`.
- **Configuraciones de entorno/despliegue** (`environment.yml`, `environment-lite.yml`, `Dockerfile`, `docker-compose.yml`, `.devcontainer/`, `.github/workflows/deploy.yml`, `runtime.txt`, etc.).

### 1.3 Fuera de alcance (estado actual)
- Publicación remota automática (no hay remoto configurado en este estado).
- Generación de sitio JupyterLite (`docs_lite/`) en el entorno actual (omitida por disponibilidad de herramientas/dependencias).
- Versionado del dataset `creditcard.csv` (se genera localmente por diseño en este estado del repositorio).

---

## 2. Estructura del repositorio

| Ruta | Descripción |
|---|---|
| `notebooks/` | 5 notebooks de historias (análisis + narrativa + visualización). |
| `INFORME_CRITICO_ARQUETIPOS.md` | Informe crítico por arquetipo/historia. |
| `REPORTE_TECNICO.md` | Este reporte técnico. |
| `README.md` | Guía de uso y formas funcionales de visualización/ejecución. |
| `src/` | Módulos reutilizables (`viz.py`, `stats_helpers.py`, `narrative.py`, `__init__.py`). |
| `data/download_data.py` | Descarga, parsing y/o generación reproducible de datasets en `data/raw/`. |
| `data/raw/` | Datasets base incluidos: `co2_mm_mlo.csv`, `gapminder.csv`, `penguins.csv`, `california_housing.csv` (y `creditcard.csv` generado localmente cuando se solicita). |
| `docs_html/` | Salida HTML estática con notebooks ejecutados (vista funcional inmediata). |
| `reports/` | Artefactos/figuras generados durante ejecuciones (según notebook/configuración). |
| `build_all.py` | Script de construcción para HTML (y tareas auxiliares de configuración). |
| `environment.yml`, `environment-lite.yml` | Definiciones de entorno conda (completo/liviano). |
| `Dockerfile`, `docker-compose.yml`, `.devcontainer/` | Configuraciones para ejecución en contenedores/entornos reproducibles. |
| `.github/workflows/deploy.yml`, `.github/postBuild`, `.github/apt.txt`, `runtime.txt`, `jupyterlite_config.json` | Configuración auxiliar para CI/despliegue/entornos gestionados. |

---

## 3. Datos y preparación

### 3.1 Datasets utilizados (por historia)
1. **CO₂ Mauna Loa** (`data/raw/co2_mm_mlo.csv`)  
   - Arquetipo: serie temporal + cambio estructural.  
   - Uso: análisis de tendencia, estacionalidad, variación temporal y evidencia de cambios de régimen.

2. **Gapminder** (`data/raw/gapminder.csv`)  
   - Arquetipo: comparación multivariable + paradoja de Simpson.  
   - Uso: contraste entre relaciones agregadas y desagregadas (pooled/within/between) y lectura contextual por grupos/países.

3. **Credit Card Fraud** (`data/raw/creditcard.csv`, **generado localmente por defecto**)  
   - Arquetipo: outliers + detección de anomalías.  
   - Uso: análisis en escenario de fuerte desbalance, evaluación con métricas apropiadas (PR/costo), partición temporal y comparación de enfoques no supervisados/supervisados.  
   - Nota técnica: en este estado del repositorio el archivo no se versiona; `data/download_data.py` puede generar un **proxy sintético reproducible** con el mismo esquema (`Time`, `Amount`, `V1`–`V28`, `Class`) o aceptar reemplazo por el dataset real.

4. **Palmer Penguins** (`data/raw/penguins.csv`)  
   - Arquetipo: drill-down jerárquico + descomposición de varianza.  
   - Uso: exploración por niveles (especie/isla/sexo, etc.) y cuantificación de variabilidad entre y dentro de grupos.

5. **California Housing** (`data/raw/california_housing.csv`)  
   - Arquetipo: intersección multivariable / confounding espacial.  
   - Uso: análisis de relaciones multivariadas con componente espacial, efectos parciales y evaluación de supuestos/heterogeneidad.

### 3.2 Script de datos (`data/download_data.py`)
- Centraliza la obtención/verificación de datasets en `data/raw/`.
- Incluye lógica de parsing/normalización para el caso de CO₂ (formato NOAA) y mecanismos de fallback/generación cuando corresponde.
- Permite regenerar localmente el dataset sintético de fraude para ejecución reproducible sin credenciales externas.

### 3.3 Consideraciones de reproducibilidad de datos
- La presencia de datasets base en `data/raw/` facilita la ejecución local y la revisión.
- El dataset de fraude se maneja como artefacto generable localmente (no versionado), por lo que su disponibilidad depende de ejecutar el script de datos cuando sea necesario.
- Las conclusiones de la historia de fraude se interpretan en función del dataset efectivamente cargado (proxy sintético por defecto o dataset real si se reemplaza).

---

## 4. Arquitectura técnica y componentes

### 4.1 Notebooks (capa analítica/narrativa)
Cada notebook implementa el flujo de una historia: contextualización, carga/preparación de datos, análisis exploratorio y/o modelado, visualización, interpretación y síntesis de hallazgos/limitaciones. La narrativa se apoya en resultados del propio dataset y en utilidades comunes del proyecto.

### 4.2 Módulo `src/` (capa de soporte)
- **`src/viz.py`**: utilidades de estilo y soporte para visualización consistente.
- **`src/stats_helpers.py`**: funciones auxiliares para cálculos estadísticos/modelado y compatibilidad entre escenarios de ejecución (incluye manejo robusto en casos donde faltan dependencias opcionales o cambian APIs de librerías).
- **`src/narrative.py`**: utilidades para estructurar mensajes/hallazgos/conclusiones narrativas en celdas.
- **`src/__init__.py`**: exposición/importación tolerante de utilidades del paquete para reducir acoplamiento rígido y fallos por dependencias opcionales.

### 4.3 Script de build (`build_all.py`) (capa de publicación local)
- Ejecuta notebooks y genera HTML estático en `docs_html/`.
- Usa entorno Python disponible (`.venv`/intérprete activo) y configura variables de entorno relevantes para ejecución (p. ej. rutas de importación y caché de matplotlib).
- Implementa tolerancia a fallos por notebook (fallback a conversión sin ejecución cuando aplica) y omite pasos no disponibles en el entorno (p. ej. JupyterLite).
- Actualiza/produce artefactos auxiliares de configuración cuando corresponde.

---

## 5. Entorno, dependencias y compatibilidad

### 5.1 Estrategia de entorno adoptada
- **Ejecución principal validada:** `venv` + `pip` (stack núcleo).
- **Dependencias núcleo empleadas:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly`, `scikit-learn`, `scipy`, `statsmodels`, `jupyter`, `nbconvert`, `ipykernel`.
- **Dependencias opcionales/avanzadas (no requeridas para la ejecución núcleo validada):** `ruptures`, `xgboost`, `shap`, `prophet`, `pmdarima`, `libpysal`, `spreg`, `econml`, `esda`, `splot`, entre otras.

### 5.2 Compatibilidad y degradación controlada
- Los notebooks y/o utilidades contemplan rutas de fallback para continuar la ejecución cuando faltan paquetes opcionales.
- Se priorizó compatibilidad con el entorno núcleo para asegurar generación de resultados reproducibles en `docs_html/`.
- Se conservaron archivos de entorno alternativo (conda/docker/devcontainer/CI) como soporte de portabilidad, aunque no todos los flujos externos fueron verificados en este entorno.

---

## 6. Proceso de construcción y validación

### 6.1 Flujo de build
1. Preparación del entorno de ejecución (`PYTHONPATH`, directorios de trabajo/caché).
2. Conversión/ejecución de notebooks a HTML (`nbconvert --execute`) con timeout configurado.
3. Fallback a HTML sin ejecución por notebook en caso de error puntual (mecanismo de resiliencia del build).
4. Generación de índice/artefactos HTML en `docs_html/`.
5. Intento/omisión controlada de pasos opcionales (p. ej. JupyterLite) según disponibilidad.

### 6.2 Resultado de validación (estado actual)
- `docs_html/` contiene la salida estática de las 5 historias/notebooks y un `index.html` de acceso.
- El proyecto queda en estado funcional para:
  - **Visualización inmediata** de resultados mediante `docs_html/`.
  - **Ejecución local** con entorno Python núcleo.
  - **Regeneración local** de HTML con `build_all.py`.

### 6.3 Artefactos generados
- **HTML estático ejecutado:** `docs_html/01_series_temporales_co2.html` … `docs_html/05_interseccion_california.html`, `docs_html/index.html`.
- **Figuras/reportes auxiliares:** en `reports/` (según ejecución de notebooks).

---

## 7. Calidad, coherencia y mantenimiento técnico

### 7.1 Decisiones técnicas relevantes
- **Robustez de ejecución:** se priorizó que las historias puedan ejecutarse con un stack núcleo común, reduciendo bloqueos por dependencias pesadas u opcionales.
- **Trazabilidad narrativa-datos:** la historia de fraude distingue explícitamente entre dataset canónico de referencia y proxy sintético local para mantener coherencia con el insumo analizado.
- **Separación de responsabilidades:** notebooks para análisis/comunicación, `src/` para utilidades reutilizables, `data/` para preparación de insumos y `build_all.py` para construcción de entregables visuales.

### 7.2 Limitaciones conocidas
- **Dependencias opcionales ausentes:** algunos métodos/modelos avanzados pueden no ejecutarse en su variante completa y se recurre a alternativas/fallbacks.
- **Dataset de fraude no versionado:** requiere generación local (`data/download_data.py`) para ejecutar esa historia desde cero si no existe el CSV.
- **Portabilidad de despliegue no verificada extremo a extremo en todos los targets:** existen configuraciones (Docker/devcontainer/CI/JupyterLite) pero no todas fueron validadas como flujo funcional en este entorno.
- **Notebooks fuente sin outputs embebidos:** la evidencia de ejecución se entrega principalmente vía `docs_html/`.

### 7.3 Recomendaciones de evolución
- Añadir `requirements.txt` (núcleo y opcional) para instalación pip más directa y reproducible.
- Incorporar pruebas automatizadas básicas (smoke tests de importación/ejecución de notebooks) en CI.
- Parametrizar el manejo de datasets opcionales (descarga/generación) en el flujo de build para entornos limpios.
- Documentar una matriz de compatibilidad (qué funciones dependen de paquetes opcionales y sus fallbacks).

---

## 8. Resumen ejecutivo

El proyecto integra cinco historias de datos con enfoques analíticos distintos, soportadas por notebooks, utilidades de código, pipeline de datos y un build que produce HTML ejecutado para revisión inmediata. La implementación prioriza reproducibilidad práctica y robustez en un entorno núcleo, manteniendo configuraciones adicionales para portabilidad futura y dejando documentadas las limitaciones y dependencias del estado actual.
