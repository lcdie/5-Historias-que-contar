# Informe crítico: 5 historias con datos, 5 arquetipos

**Curso:** Ciencia de Datos Avanzada — **Facultad:** MATCOM, Universidad de La Habana  
**Autor:** Luis Calderón Denis  
**Fecha de redacción:** 2026-11-20

> **Criterio de evidencia:** este informe justifica la elección de arquetipos y el carácter de “historia con datos” de cada caso. Las **afirmaciones cuantitativas** (coeficientes, métricas, diagnósticos, fechas de quiebre, validaciones) deben leerse en correspondencia 1:1 con las salidas de los notebooks y los HTML ejecutados en el entorno declarado (`docs_html/`, regenerados en entorno núcleo cuando corresponda). Cuando una técnica depende de dependencias opcionales no disponibles, el análisis y este informe se limitan a lo efectivamente calculado y lo declaran explícitamente. Ver `REFERENCIAS_Y_APENDICE_METODOLOGICO.md`.

---

## 1. Introducción: por qué estos arquetipos

La selección de arquetipos responde a preguntas analíticas distintas que exigen decisiones metodológicas distintas, forzadas por la estructura de cada dataset:

| Historia | Arquetipo | Pregunta guía | Dataset (archivo) | Rasgo estructural que motiva el arquetipo |
|---|---|---|---|---|
| 1 | Serie temporal + cambio estructural | ¿Cambia el régimen/tasa de crecimiento en el tiempo? | `co2_mm_mlo.csv` (Mauna Loa) | Serie larga con estacionalidad, tendencia y necesidad de descomposición/validación temporal |
| 2 | Comparación multivariable + paradoja de Simpson/composición | ¿La asociación cambia al desagregar niveles? | `gapminder.csv` | Panel país–año con heterogeneidad entre y dentro de unidades |
| 3 | Outliers + detección de anomalías | ¿Cómo detectar eventos raros con costos asimétricos? | `creditcard.csv` (proxy sintético por defecto; reemplazable por ULB/Kaggle) | Fuerte desbalance, evaluación temporal y métricas operativas (no accuracy) |
| 4 | Drill-down jerárquico + descomposición de varianza | ¿Qué nivel jerárquico explica la variabilidad? | `penguins.csv` | Estructura por grupos (especie/isla/sexo/año) y diseño no balanceado |
| 5 | Intersección multivariable + confounding espacial (observacional) | ¿La asociación ingreso–precio persiste al condicionar por ubicación y covariables? | `california_housing.csv` | Covariables correlacionadas y componente espacial; riesgo de confounding y dependencia |

**Hilo conductor:** en cada historia, la narrativa no se impone al dato; emerge de la interacción entre pregunta, estructura del dataset, método aplicado y limitaciones observadas.

---

## 2. Justificación por historia

### 2.1 Historia 1 — CO₂ Mauna Loa: serie temporal y cambio estructural

**Por qué responde al arquetipo.** El arquetipo exige ir más allá de graficar una tendencia: requiere separar componentes (p. ej. estacionalidad y tendencia), cuantificar tasas de cambio, evaluar posibles quiebres de régimen y contrastar adecuación/validación temporal. La serie de Mauna Loa, por su longitud y estacionalidad, obliga a descomponer antes de interpretar y a tratar explícitamente la inferencia temporal (dependencia serial, elección de ventanas, sensibilidad a métodos de quiebre).

**Por qué es una historia con datos (y no solo análisis técnico).** La pregunta se formula en términos sustantivos (¿se acelera la acumulación observada?) y se responde con evidencia encadenada: dato cargado → descomposición STL → tasas/pendientes e intervalos o comparaciones pre/post → selección/uso de quiebre para ajuste por tramos → validación y diagnósticos → interpretación acotada. El relato explicita que un quiebre estadístico no equivale a atribución causal y que la confianza depende de supuestos y robustez. Los valores concretos (pendientes, fechas, métricas de error, R²/diagnósticos) son los producidos por la ejecución del notebook correspondiente.

**Coherencia con el dataset.** Las conclusiones se anclan en la serie mensual efectivamente utilizada (`co2_mm_mlo.csv`) y en sus propiedades observadas (estacionalidad, tendencia, posibles ausencias/procesamiento de fuente), no en cifras externas insertadas a priori.

### 2.2 Historia 2 — Gapminder: comparación multivariable y paradoja de Simpson/composición

**Por qué responde al arquetipo.** El arquetipo se caracteriza porque la asociación marginal puede diferir de la condicional al agregar grupos heterogéneos. Un panel país–año con niveles (país, continente, tiempo) es el entorno natural para comparar estimaciones *pooled*, *between* y *within*, y para discutir composición mediante especificaciones con efectos y descomposiciones.

**Por qué es una historia con datos.** La narrativa confronta una intuición agregada con evidencia desagregada: mismas variables, distinto nivel de análisis, distinto coeficiente/lectura. El valor narrativo está en mostrar cómo la estructura del panel cambia la conclusión y en documentar las especificaciones empleadas (OLS, efectos fijos, mixtos o descomposición según lo ejecutado), junto con sus límites. La interpretación se mantiene en clave **asociacional/condicional**: controlar heterogeneidad entre unidades reduce confusión por composición, pero no identifica por sí sola un efecto causal.

**Coherencia con el dataset.** `gapminder.csv` provee la variación entre países, entre continentes y en el tiempo necesaria para que la paradoja/composición sea demostrable empíricamente dentro del proyecto.

### 2.3 Historia 3 — Fraude en transacciones: outliers/anomalías como pipeline de decisión (simulación por defecto)

**Por qué responde al arquetipo.** La detección de anomalías en eventos raros exige (i) métricas adecuadas al desbalance (PR-AUC, recall/precision, Fβ, costo esperado), (ii) umbrales orientados a decisiones y (iii) validación que respete la dimensión temporal. El esquema de datos (`Time, V1–V28, Amount, Class`) permite implementar ese protocolo aun bajo anonimización (PCA) y desbalance.

**Por qué es una historia con datos.** La historia no es “entrenar un modelo”, sino mostrar cómo los datos imponen un marco de evaluación: por qué *accuracy* falla, cómo se elige y justifica un umbral por costos, qué informa un *split* temporal y qué aporta (o no) un comparador supervisado cuando está disponible. La trazabilidad es explícita: datos cargados → partición temporal → modelos/scores → métricas y costos → decisión e incertidumbre.

**Delimitación crítica (coherencia y alcance).** En el estado por defecto del repositorio, `creditcard.csv` se genera localmente como **proxy sintético reproducible** (no versionado). En consecuencia, la historia debe leerse como **demostración de metodología y pipeline** sobre el insumo utilizado; sus métricas **no se extrapolan** a desempeño real de fraude. Si se sustituye por el dataset real ULB/Kaggle (mismo esquema), el pipeline se reejecuta y las conclusiones deben actualizarse a esos resultados. Esta delimitación es parte central de la honestidad narrativa.

### 2.4 Historia 4 — Palmer Penguins: drill-down jerárquico y descomposición de varianza

**Por qué responde al arquetipo.** El arquetipo requiere cuantificar contribuciones de distintos niveles jerárquicos a la variabilidad y mostrar cómo la inferencia cambia al desagregar. Palmer Penguins ofrece niveles naturales (especie, isla, sexo, año, individuo) y un diseño incompleto que impide confundir análisis con un ANOVA balanceado ideal.

**Por qué es una historia con datos.** El recorrido analítico (descriptivos por niveles, tablas de diseño, ICC/tamaños de efecto y modelos o comparaciones según ejecución, además de validaciones por grupo cuando aplica) convierte la estructura del muestreo en el eje de la narrativa: qué explica más variabilidad, qué combinaciones existen realmente y qué no puede separarse limpiamente. El “hallazgo” incluye la limitación del diseño, sustentada en los datos observados.

**Coherencia con el dataset.** La descomposición y el drill-down solo tienen sentido por las variables y la organización jerárquica presentes en `penguins.csv`; la historia depende de ese recorrido empírico.

### 2.5 Historia 5 — California Housing: intersección multivariable y confounding espacial (observacional)

**Por qué responde al arquetipo.** La relación ingreso–precio de vivienda está entrelazada con localización y otras covariables. El arquetipo exige condicionar, diagnosticar posible dependencia espacial y explorar heterogeneidad, reconociendo que con datos observacionales transversales la identificación causal es limitada.

**Por qué es una historia con datos.** La narrativa se construye por capas trazables: asociación bruta → asociación condicional (controles/ubicación) → inspección de residuos y estructura espacial → modelos flexibles o diagnósticos adicionales **solo cuando están disponibles y calculados** → validación y sensibilidad exploratoria (p. ej. Oster) → límites inferenciales (confounders no observados, MAUP, antigüedad de datos). Se distingue explícitamente entre asociación condicional, capacidad predictiva y causalidad: sin estrategia cuasi-experimental, no se reclaman efectos causales identificados.

**Coherencia con el dataset.** `california_housing.csv` (censo 1990, unidades espaciales) obliga a tratar la geografía como parte del problema analítico; las conclusiones válidas son las que se derivan de las especificaciones y diagnósticos efectivamente ejecutados sobre este archivo.

---

## 3. Síntesis transversal: qué hace que sean historias con datos

| Dimensión | Criterio aplicado en el proyecto |
|---|---|
| Pregunta con sentido | Cada historia parte de una pregunta interpretable en el dominio del dataset, no de una técnica aislada. |
| Trazabilidad | Cadena explícita: dato → decisión metodológica → resultado calculado → interpretación → límite. |
| Método forzado por el dato | Estacionalidad/tiempo, jerarquía, desbalance, composición/agregación y estructura espacial dictan el enfoque. |
| Evidencia ejecutada | Figuras, tablas, métricas y diagnósticos citables provienen de la ejecución de notebooks/HTML en el entorno declarado. |
| Validación acorde a la estructura | Temporal (*rolling-origin*, *split* cronológico), por grupos (*leave-one-out*), o espacial/bloques cuando corresponde y está disponible. |
| Limitaciones y próximos pasos | Las restricciones de datos, supuestos y herramientas se reportan como parte del resultado, no como anexo retórico. |
| Reproducibilidad | Datos incluidos o generables según política del repo, entorno núcleo documentado, build de HTML y declaración de componentes opcionales. |

---

## 4. Niveles de resultados y reproducibilidad

- **Entorno núcleo (base):** dependencias en `requirements.txt`; permite ejecutar las 5 historias con degradación controlada cuando falten paquetes opcionales. Los HTML en `docs_html/` deben corresponder a una ejecución coherente con el entorno declarado.
- **Entorno completo (opcional):** incorpora librerías adicionales (p. ej. detección de quiebres avanzada, modelos supervisados/interpretabilidad, análisis espacial o causal) que habilitan análisis complementarios. Cualquier resultado que dependa de ellas debe regenerarse y reportarse indicando el entorno.

Esta separación evita presentar como evidencia resultados no computados en la ejecución disponible.

---

## 5. Limitaciones transversales del proyecto

1. **Dependencia de paquetes opcionales:** algunas técnicas avanzadas no se ejecutan en entorno núcleo; los notebooks deben (y en esta versión buscan) reflejarlo explícitamente.
2. **Naturaleza observacional:** en historias 2 y 5, en particular, las conclusiones son asociacionales/condicionales salvo identificación cuasi-experimental explícita y ejecutada.
3. **Dataset de fraude por defecto:** el proxy sintético es útil para reproducibilidad y enseñanza del pipeline, pero no sustituye evidencia empírica de fraude real.
4. **Datos históricos/agregados:** CO₂ (estación específica), Gapminder y California (censo 1990) imponen límites de generalización temporal, espacial o de unidad de análisis.

---

## 6. Conclusión

Las cinco historias cumplen el objetivo del arquetipo correspondiente cuando se evalúan por su **coherencia dato–método–pregunta** y por la **trazabilidad** de sus afirmaciones a resultados ejecutados. La solidez del proyecto no depende de presentar cifras fijas desligadas del entorno, sino de sostener cada afirmación con evidencia reproducible, declarar el alcance inferencial (asociación, predicción, sensibilidad, simulación de pipeline) y explicitar las limitaciones propias de los datos y de las herramientas disponibles. Bajo esos criterios, el conjunto constituye un trabajo de *storytelling con datos* metodológicamente defendible y alineado con la consigna de la asignatura.

---

## Referencias

Las referencias de datos, métodos y el apéndice de parámetros/criterios por historia se documentan en `REFERENCIAS_Y_APENDICE_METODOLOGICO.md` y en `FUENTES_Y_DATOS.md`.
