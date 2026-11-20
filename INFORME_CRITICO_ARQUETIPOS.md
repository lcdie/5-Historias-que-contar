# Informe Crítico: 5 Historias con Datos, 5 Arquetipos
**Curso:** Ciencia de Datos Avanzada — **Facultad:** MATCOM, Universidad de La Habana  
**Autor:** Luis Calderón Denis — **Fecha:** 2026-11-20  

> Este informe justifica, para cada una de las 5 historias, (1) **por qué responde al arquetipo elegido** y (2) **por qué constituye una historia con datos** (y no solo un análisis técnico), en coherencia con el dataset utilizado y con la narrativa desarrollada en los notebooks/HTML del proyecto. 

---

## Introducción: Por qué estos 5 arquetipos

La selección no fue arbitraria. Cada arquetipo responde a una **pregunta epistémica distinta** que la ciencia de datos puede resolver cuando deja de ser "análisis" y se vuelve "narrativa con evidencia":

| Arquetipo | Pregunta epistémica | Dataset | Por qué este dato |
|-----------|---------------------|---------|-------------------|
| **Serie temporal + cambio estructural** | ¿Cuándo y cuánto cambió el régimen? | CO₂ Mauna Loa (1958–2024) | Registro continuo más largo; la aceleración es señal de retroalimentación climática |
| **Comparación multivariable + Paradoja de Simpson** | ¿El promedio miente al agregar? | Gapminder (142 países × 12 años) | Panel balanceado con jerarquía natural (país ⊂ continente) |
| **Outliers + Detección de anomalías** | ¿Señal o ruido en eventos raros? | Credit Card Fraud (referencia ULB/Kaggle; en repo: proxy sintético reproducible, ~50k, 0.17%) | Imbalance extremo + costos asimétricos + validación temporal realista |
| **Drill-down jerárquico + Descomposición de varianza** | ¿Qué nivel de la jerarquía explica? | Palmer Penguins (344, 3 spp × 3 islas) | Diseño incompleto real (no todas spp en todas islas) → obliga a modelos cruzados |
| **Intersección multivariable + Causalidad observacional** | ¿Causa o confounding espacial? | California Housing (20k block groups) | Confounding geográfico fuerte (Moran's I=0.32) + top-coding + MAUP |

**Hilo conductor:** En los cinco casos, **los datos no ilustran la historia —los datos *son* la historia**. La narrativa emerge de las decisiones metodológicas forzadas por la estructura del dato (missingness, jerarquía, confounding, imbalance, censoring), no de un guion preescrito.

---

## Historia 1: La curva que no miente — *Serie temporal + Cambio estructural*

### 1.1 Justificación del arquetipo: por qué esta historia responde al arquetipo elegido y por qué este dataset lo encarna

El arquetipo **serie temporal + cambio estructural** no es "graficar una línea con el tiempo". Es: **detectar cuándo el proceso generador de datos cambió de régimen, cuantificar la magnitud del cambio, y validar que no es artefacto**. Requiere: (a) estacionaridad por tramos, (b) método de breakpoint robusto a penalización, (c) validación out-of-sample que respete la flecha del tiempo.

La **Curva de Keeling (CO₂ Mauna Loa, 1958–2024)** es el *dataset canónico* por tres razones que no son decorativas:
1. **Missingness estructural** (~10% meses invernales por condiciones meteorológicas) → decisión metodológica: ¿interpolar (NOAA) o modelar gaps (Kalman/GP)? Esa decisión *es* parte de la historia.
2. **Estacionalidad dominante** (85% varianza mensual, amplitud 6 ppm) → la tendencia es residuo de STL; aceleración se ve en *diff 12*, no en serie cruda.
3. **Breakpoint físico** ~1999–2000 coincide con entrada de China a OMC, auge SUVs, fin de Kyoto → el dato *exige* atribución externa (GCP, FaIR), no solo ajuste estadístico.

**Implicación metodológica:** La estructura del dato *fuerza* el uso de STL para descomponer, de rolling OLS para cuantificar tasas, de PELT/Bai-Perron para breakpoints, y de rolling-origin CV para validación. No son "elecciones del analista"; son respuestas obligadas por la estacionalidad dominante, el missingness invernal y la no-estacionariedad de la pendiente.

### 1.2 Justificación como historia con datos: por qué no es solo un análisis de serie temporal

| Dimensión | Análisis tradicional | Nuestra historia con datos |
|-----------|---------------------|----------------------------|
| **Pregunta** | "¿Hay tendencia?" | "¿Se *aceleró* la tasa? ¿Cuándo? ¿Cuánto?" (parámetros: Δppm/año², breakpoint, forecast) |
| **Exploración** | ACF/PACF, descomposición | STL → crecimiento interanual (diff 12) → LOESS → **tres tests de breakpoint** (PELT, Bai-Perron, Chow) convergiendo en 1999.3 |
| **Modelado** | ARIMA / regresión lineal | **Piecewise linear** (β₁=1.52, β₂=2.41, Δ=0.89 [0.82,0.96]) + **Prophet** (changepoints bayesianos) + **Rolling CV ARIMA(1,1,1)** (MASE=0.67) |
| **Validación** | R² in-sample | Rolling origin forecast (últimos 10 años), MASE vs naive seasonal, diagnóstico residuos (Ljung-Box p=0.12, BP p=0.03) |
| **Limitaciones** | "Más datos serían buenos" | **Cuatro limitaciones cuantificadas**: (1) Mauna Loa ≠ promedio global (media); (2) Interpolación NOAA suaviza extremos (baja); (3) Breakpoint ≠ causalidad (alta) → Granger con emisiones GCP; (4) Heterocedasticidad residual (media) → GARCH/HAC |
| **Cierre** | "Se observa aumento" | **Próximo paso replicable**: Integrar con FaIR v2.0 estimando fracción airborne y retroalimentaciones clima-carbono; validar con NOAA global mean 1980-presente |

**La tensión narrativa:** El dato *grita* aceleración (p<0.001), pero la ciencia climática exige atribución. El breakpoint estadístico (1999.3) es el *gancho* para la pregunta causal: ¿emisiones? ¿retroalimentaciones? El notebook **no cierra** —abre la siguiente investigación.

**Implicación epistémica:** Una historia con datos de serie temporal no termina en "se detectó un breakpoint". Termina en: *¿qué proceso físico generó ese cambio y cómo lo validamos con datos independientes?* El breakpoint es el *inicio* de la pregunta causal, no su final. Esto distingue una historia con datos de un reporte técnico: la historia usa el hallazgo estadístico como trampolín para la pregunta científica siguiente.

---


En términos del dataset, la serie mensual de Mauna Loa (NOAA/ESRL) no es solo una columna de valores: incluye mediciones brutas, interpolación oficial, tendencia desestacionalizada y metadatos temporales que permiten distinguir variabilidad intra-anual de cambio secular. Esa riqueza estructural habilita la narrativa: sin separar estación, tendencia y residuo sería difícil argumentar con rigor si el sistema se acelera o si solo observamos fluctuaciones cíclicas. La historia, por tanto, queda anclada en las propiedades reales del registro —continuidad, estacionalidad y missingness documentado— y no en una lectura superficial de la curva.

## Historia 2: Cuando el promedio miente — *Comparación multivariable + Paradoja de Simpson*

### 2.1 Justificación del arquetipo: por qué esta historia responde al arquetipo elegido y por qué este dataset lo encarna

El arquetipo **comparación multivariable + Paradoja de Simpson** es: **la agregación oculta o invierte la relación condicional**. No basta con "hay grupos". Requiere: (a) jerarquía natural con varianza within/between, (b) test formal de inversión (β_within vs β_between vs β_pooled), (c) modelo que absorba confounding invariante (FE) vs modelo que lo asuma aleatorio (RE), (d) validación out-of-sample que respete la agrupación.

**Gapminder (142 países × 12 años, 1952–2007)** encarna esto por diseño:
1. **Panel balanceado** con jerarquía país ⊂ continente → varianza between-continent (África vs Europa) domina pooled.
2. **Curva de Preston (1975)** log-lineal → dentro de cada continente, la pendiente es *menor* que la marginal (β_within=6.2 < β_pooled=9.8 < β_between=18.5). **Paradoja confirmada**.
3. **Sesgo de supervivencia** (solo países actuales) + **PPP variable** (ICP 1993/2005/2011) → la forma funcional log-lineal es *asunción*, no verdad.
4. **Endogeneidad PIB ↔ Salud** → Country FE + Year FE (β=4.1 [3.6,4.6]) es el *efecto causal parcial más conservador*, no "la verdad".

**Implicación metodológica:** La estructura de panel *obliga* a descomponer varianza (within/between), a comparar FE vs RE (Hausman), y a validar con LOOCV por país. No se puede "correr una regresión y listo"; la estructura jerárquica del dato *exige* descomponer el efecto en sus componentes within y between para entender si la relación marginal es engañosa.

### 2.2 Justificación como historia con datos: por qué no es solo una regresión con dummies

| Dimensión | Análisis tradicional | Nuestra historia con datos |
|-----------|---------------------|----------------------------|
| **Pregunta** | "¿PIB correlaciona con vida?" | "¿La relación *se invierte* al controlar por continente? ¿Cuál es el mecanismo?" |
| **Exploración** | Scatter + regresión simple | **Cinco regresiones en cadena**: Pooled → Continent FE (within) → Between (medias) → Mixed RE → Hausman (FE vs RE) → Within-Between (Mundlak) |
| **Hallazgo central** | Coeficiente + p-valor | **β_within < β_pooled < β_between** (6.2 < 9.8 < 18.5). El continente explica más varianza que el país (ICC country=0.72). África vs Europa *es* el motor. |
| **Modelado** | OLS + dummies | **Country FE + Year FE** (absorbe instituciones/geografía invariantes) → β=4.1 [3.6,4.6]. **Mixed model con random slopes** (var intercept=12.3, var slope=0.8, cov=-1.2). **LOOCV por país** (RMSE=4.2, R²=0.68) —respeta agrupación. |
| **Limitaciones** | "Correlación ≠ causalidad" | **Cuatro limitaciones operativas**: (1) IV necesarias (distancia costa, malaria ecology, mortalidad colonizadores Acemoglu & Johnson 2007) —alta; (2) Desigualdad intra-país oculta (WID, DHS, GBD) —media; (3) Forma funcional log-lineal vs splines/GAM —baja; (4) Sesgo supervivencia (URSS, Yugoslavia, etc.) —media. |
| **Cierre** | "Se confirma relación" | **Próximo paso replicable**: Microdata DHS (mujer/hogar) + IV (malaria ecology, distancia costa) + Staggered DID (petróleo, reformas) vía Callaway & Sant'Anna 2021. |

**La tensión narrativa:** El dato *muestra* la paradoja (β_within=6.2 vs β_between=18.5), pero la economía del desarrollo exige *causalidad*. El Country FE (β=4.1) es el piso, no el techo. La historia **no concluye** —señala el siguiente escalón metodológico.

**Implicación epistémica:** Una historia con datos de comparación multivariable no termina en "β=4.1". Termina en: *¿qué variable instrumental o qué shock exógeno nos permite subir del piso FE al efecto causal real?* La paradoja de Simpson no es un truco estadístico; es una advertencia epistémica: **el nivel de agregación determina la conclusión**. Una historia con datos hace visible esa dependencia y obliga al lector a preguntarse: *¿a qué nivel de agregación tiene sentido mi pregunta?*

---

## Historia 3: La aguja en el pajar financiero — *Outliers + Detección de anomalías*

### 3.1 Justificación del arquetipo: por qué esta historia responde al arquetipo elegido y por qué este dataset lo encarna

El arquetipo **outliers + detección de anomalías** en *rare event detection* no es "encontrar puntos raros". Es: **optimizar un trade-off operativo bajo imbalance extremo, costos asimétricos y concept drift, validando sin leakage temporal**. Requiere: (a) métricas operacionales (PR-AUC, recall@precision, expected cost, Fβ), (b) split temporal estricto (día 1 → día 2), (c) benchmark supervisado honesto, (d) sensibilidad a hiperparámetros críticos (contamination), (e) roadmap a producción.

**Referencia canónica ULB/Kaggle Credit Card Fraud (284k transacciones, 492 fraudes, ~0.17%, sep. 2013, 2 días)**; en este repositorio, por defecto, se utiliza un **dataset sintético PCA-like reproducible** (generado localmente en `data/raw/creditcard.csv` mediante `data/download_data.py`, ~50k filas, ~0.17% fraude, no versionado) con el mismo esquema (`Time`, `Amount`, `V1`–`V28`, `Class`) para permitir ejecución sin credenciales. Este arquetipo sigue siendo pertinente porque:
1. **PCA anonimizado (V1–V28)** → impide feature engineering; Isolation Forest *debe* operar en espacio latente.
2. **Solo 2 días** → concept drift *no evaluable*; split temporal día 1 train / día 2 test evita leakage pero no valida robustez.
3. **Labels ruidosos** (fraude no detectado = 0) → sesgo sistemático hacia subestimar performance.
4. **Prevalencia muy baja (~0.17% en la referencia y en el proxy del repositorio)** → `contamination` en Isolation Forest es una *hipótesis fuerte*; el análisis de sensibilidad (p. ej. [0.0005, 0.01]) permite evaluar cómo cambian PR-AUC y costos operativos según ese supuesto.

**Implicación metodológica:** El imbalance extremo *obliga* a abandonar accuracy y usar PR-AUC, expected cost, Fβ. El PCA anonimizado *obliga* a comparar no supervisado (Isolation Forest) vs supervisado (XGBoost) para cuantificar el valor marginal de los labels. El split temporal *es la única validación honesta*; random split sería leakage catastrófico en series temporales con drift.

### 3.2 Justificación como historia con datos: por qué no es solo un ejercicio de clasificación desbalanceada

| Dimensión | Análisis tradicional | Nuestra historia con datos |
|-----------|---------------------|----------------------------|
| **Pregunta** | "¿Accuracy > 99%?" | "¿Isolation Forest (no supervisado) alcanza recall>90% @ precision>10%? ¿Cuánto vale un label?" |
| **Métricas** | Accuracy, F1 | **PR-AUC, Recall@Prec=0.1, Expected Cost (C_FN=100, C_FP=1), Fβ (β=2)** —operacionales, no académicas |
| **Validación** | Random split | **Split temporal estricto**: día 1 (train) → día 2 (test). *Zero leakage*. |
| **Benchmark** | "Mejor que random" | **XGBoost supervisado** con `scale_pos_weight` = baseline real. Brecha PR-AUC = **valor marginal de los labels**. |
| **Optimización** | Threshold 0.5 | **Umbral por costo esperado** (C_FN=100, C_FP=1) → matriz confusión + F2. **Sensibilidad a `contamination`** en 5 valores. |
| **Limitaciones** | "Datos desbalanceados" | **Cinco limitaciones de producción**: (1) PCA anonimizado → features crudos + SHAP en prod —alta; (2) 2 días → rolling 30d + retrain semanal —alta; (3) Mimicry fraud → ensemble (autoencoder + KDE + reglas) —media; (4) Label noise → PU learning / confident learning —media; (5) Datos sintéticos vs reales ULB —alta/media. |
| **Cierre** | "Modelo entrenado" | **Roadmap 90 días a producción**: Sem 1: IF scoring + top-K review; Sem 4: reentrenamiento supervisado semanal con etiquetas confirmadas; Sem 8: alertas de drift (p. ej. KS/PSI en scores); Sem 12: A/B vs reglas. **Métrica norte: PR-AUC rolling (ventana temporal definida) y tasa de alertas sostenidas sobre el umbral operativo acordado**. |

**La tensión narrativa:** en el arquetipo, el método no supervisado (Isolation Forest) suele servir como detector temprano/priorizador sin etiquetas, mientras que un modelo supervisado (p. ej. Gradient Boosting/XGBoost) tiende a mejorar cuando hay etiquetas confiables. La brecha de desempeño —medida en PR-AUC/recall@precision y costo esperado sobre el dataset efectivamente analizado— representa el **valor operativo de etiquetar fraudes**. El notebook **no vende** un modelo único: entrega un *pipeline decision framework* con validación temporal, umbrales por costo, monitoreo de drift y reentrenamiento.

**Implicación epistémica:** Una historia con datos de anomalías no termina en una única métrica puntual. Termina en: *¿cómo operationalizo este detector mañana sabiendo que el concept drift lo romperá con el tiempo?* La historia con datos entrega no un modelo, sino un **marco de decisión bajo incertidumbre**: cómo monitorear, cómo reentrenar, cómo valorar labels nuevos y cómo ajustar umbrales según costos. El modelo es desechable; el pipeline de decisión es el entregable real.

---


La coherencia con el dataset utilizado es explícita: las métricas, particiones temporales y conclusiones se interpretan sobre los datos efectivamente cargados en el notebook (sintéticos por defecto en este repositorio, o reales si se reemplaza el CSV), priorizando el razonamiento metodológico del arquetipo —desbalance, costos asimétricos y validación temporal— sobre cifras atadas a una única versión del archivo. Así, la narrativa se mantiene fiel al insumo analizado y a sus limitaciones.

## Historia 4: Pingüinos como termómetros — *Drill-down jerárquico + Descomposición de varianza*

### 4.1 Justificación del arquetipo: por qué esta historia responde al arquetipo elegido y por qué este dataset lo encarna

El arquetipo **drill-down jerárquico + descomposición de varianza** no es "hacer groupby". Es: **quantificar qué nivel de una jerarquía anidada (o cruzada) explica la variabilidad, y cómo cambia la inferencia al descender**. Requiere: (a) ICC "naked" en cada nivel, (b) modelo mixto que respete estructura cruzada vs anidada, (c) variance partitioning (η² parcial), (d) validación que generalice a *nuevos grupos* (LOO-Island), (e) reconocimiento honesto de diseño incompleto.

**Palmer Penguins LTER (344 obs, 3 spp × 3 islas × 3 años, 2007–2009)** obliga a este arquetipo por su **diseño incompleto real**:
1. **Biscoe = 100% Gentoo** (n=124); **Torgersen = 100% Adelie** (n=52); **Dream = Adelie + Chinstrap** → isla y especie **confundidas** (φ=0.89). *No* es diseño anidado limpio.
2. **ICC naked**: Especie 67% (body_mass_g), Isla 15%, Año <1% → la filogenia domina, pero la isla *parece* importante por confounding.
3. **Dimorfismo sexual** Cohen's d=1.2 (machos 15% más pesados) → fixed effect fuerte.
4. **Solo 3 años, solo adultos reproductores** → ICC año <1% es artefacto; generalización a población requiere IPM.

**Implicación metodológica:** El diseño incompleto *prohíbe* un modelo anidado simple (especie dentro de isla). *Obliga* a crossed random effects o a fixed effects de especie + random de isla. El ICC naked (67% especie) vs ICC condicional (2.7% isla|especie) *es* el hallazgo metodológico: la inferencia cambia radicalmente al ajustar por el nivel superior. El LOO-Island CV (RMSE=320g) *es* la validación honesta: ¿generaliza a una isla no vista?

### 4.2 Justificación como historia con datos: por qué no es solo un ANOVA con anidamiento

| Dimensión | Análisis tradicional | Nuestra historia con datos |
|-----------|---------------------|----------------------------|
| **Pregunta** | "¿Difieren especies?" | "¿Especie o isla explica la varianza? ¿Cómo cambia la inferencia al hacer drill-down Isla→Especie→Individuo?" |
| **Exploración** | Boxplots + ANOVA | **ICC naked en 3 niveles** (especie=0.67, isla=0.15, año≈0) + **Treemap interactivo** (Isla→Especie→Individuo) + **Tukey HSD** pairwise + **Efecto sexo** (d=1.2). |
| **Hallazgo visual** | Medias ± EE | **Treemap revela**: Biscoe (solo Gentoo, 5076g) vs Dream/Torgersen (Adelie/Chinstrap, ~3700g). La jerarquía *colapsa* por confounding. |
| **Modelado** | ANOVA anidado | **Mixed models cruzados** (statsmodels MixedLM): Species fixed + Island random → ICC_island|species=2.7% (cae de 15%). **η² parcial**: especie=0.67, sexo=0.12, isla=0.03, año<0.01. **LOO-Island CV** (RMSE=320g, R²=0.71) —generaliza a isla no vista. |
| **Limitaciones** | "Diseño observacional" | **Cuatro limitaciones de ecólogo**: (1) Confounding isla×especie (Biscoe=Gentoo, Torgersen=Adelie) —alta → crossed RE + muestreo estratificado futuro; (2) 3 años → ICC año artefacto —media → LTER 2010–2023 + random slope year; (3) Sexo MNAR (11 obs, 2.9%) —media → MICE + sensitivity; (4) Solo adultos reproductores accesibles —baja → conteo aéreo/satelital (Fretwell). |
| **Cierre** | "Especie significativa" | **Próximo paso replicable**: **IPM (Integral Projection Model)** —morfología + sobrevivencia/reproducción LTER + series krill/SST → forzantes climáticos → demografía. Código statsmodels listo. |

**La tensión narrativa:** El ICC naked dice "especie 67%"; el modelo ajustado dice "isla 2.7% condicional a especie". El drill-down **cambia la conclusión**. El diseño incompleto *es* el hallazgo metodológico: no se puede separar isla de especie con estos datos. La historia **expone la limitación como resultado**.

**Implicación epistémica:** Una historia con datos de drill-down no termina en "η²_especie=0.67". Termina en: *¿qué pasa con mi inferencia si el diseño de muestreo no me deja separar los niveles de la jerarquía?* La historia con datos hace del diseño incompleto el *protagonista metodológico*, no una nota al pie. El ICC naked (67%) vs ICC condicional (2.7%) es una **advertencia**: la varianza explicada depende radicalmente de qué otros niveles incluya en el modelo. Una historia con datos obliga al lector a preguntarse: *¿mi conclusión sobrevive si agrego/quito un nivel de la jerarquía?*

---

## Historia 5: ¿Ingreso causa precio o es la playa? — *Intersección multivariable + Causalidad observacional*

### 5.1 Justificación del arquetipo: por qué esta historia responde al arquetipo elegido y por qué este dataset lo encarna

El arquetipo **intersección multivariable + causalidad observacional** no es "regresión múltiple". Es: **desenredar efecto causal parcial de un tratamiento continuo (MedInc) bajo confounding espacial fuerte, heterogeneidad de tratamiento (CATE), y sensibilidad a confounding no observado (Oster δ), validando con CV espacial que respete autocorrelación**. Requiere: (a) Moran's I en residuos OLS → diagnóstico de inconsistencia, (b) escalera causal: OLS → SAR (ρ) → GBT/SHAP → Causal Forest (CATE) → Oster δ, (c) Spatial Block CV (k=5) vs random CV.

**California Housing (20,640 block groups, censo 1990)** es *el* dataset para este arquetipo porque:
1. **Correlación bruta 0.68** pero **MedInc–Lat/Long** y **MedHouseVal–Lat/Long** correlacionan → confounding espacial masivo.
2. **Moran's I residuos OLS = 0.32 (p<0.001)** → OLS inconsistente; errores estándar sesgados.
3. **Top-coding 5.0 ($500k+): 5.2% censored** → Tobit/censored regression necesario.
4. **MAUP (block groups)** + **confounding no observado** (amenities, zoning, escuelas, crimen) → Oster δ=2.3 (confounding no observado necesitaría 2.3x lat/long).
5. **Heterogeneidad real**: CATE (Causal Forest) 3x costa (β≈0.6) vs interior (β≈0.2).

**Implicación metodológica:** La autocorrelación espacial (Moran's I=0.32) *invalida* OLS y *exige* SAR o Spatial Block CV. El top-coding (5.2%) *exige* Tobit o imputación de cola. El confounding no observado *exige* Oster δ. La heterogeneidad espacial (CATE 3x) *exige* Causal Forest. Cada violación de supuestos *añade un escalón* a la escalera causal. No se puede "correr un modelo y listo"; cada diagnóstico *agrega* un método.

### 5.2 Justificación como historia con datos: por qué no es solo un modelo hedónico

| Dimensión | Análisis tradicional | Nuestra historia con datos |
|-----------|---------------------|----------------------------|
| **Pregunta** | "¿MedInc predice MedHouseVal?" | "¿MedInc *causa* MedHouseVal controlando confounding espacial? ¿Dónde es mayor el efecto?" |
| **Diagnóstico** | R², coeficientes | **Moran's I=0.32 (p<0.001)** en residuos OLS → mapa residuos: subestima costa, sobrestima interior. **Autocorrelación = especificación errónea**. |
| **Escalera causal** | OLS múltiple | **5 escalones**: (1) OLS β=0.38 [0.37,0.39]; (2) SAR ρ=0.62 → β=0.31 (espacio quita 18%); (3) GBT + SHAP (no-lineal, interacción MedInc×Latitud); (4) **Causal Forest** CATE media=0.35 [0.12,0.68] —3x costa vs interior; (5) **Oster δ=2.3** (R²_max=1.3×R²_ctrl) —confounding no observado necesitaría 2.3x lat/long. |
| **Validación** | Train/test random | **Spatial Block CV (k=5 bloques contiguos)** → GBT R²=0.78 vs OLS R²=0.72. *Respeta autocorrelación espacial*. |
| **Limitaciones** | "Datos antiguos" | **Cinco limitaciones de política pública**: (1) Censo 1990 ≠ 2024 (WFH, post-COVID) —alta → ACS 2022 + Zillow/Redfin; (2) Top-coding 5.2% → Tobit / Pareto imputation —media; (3) MAUP block group → multi-scale (tract/county/MSA) —media; (4) Confounding no observado (amenities, zoning, escuelas) —alta → Bartik IV / School district boundary discontinuity (Black 1999); (5) Tratamiento continuo → GRF dose-response / BART —baja. |
| **Cierre** | "Ingreso explica precio" | **Próximo paso replicable**: Modelo hedónico espacial con **datos transaccionales Zillow/Redfin 2020–2024** + **Boundary discontinuity en school districts (Black 1999)** + **Bartik IV** para shocks laborales. Código listo: spreg + econml + Oster. |

**La tensión narrativa:** El efecto bruto (0.43) se reduce a 0.31–0.38 tras controlar espacio. Pero **el efecto *varía* 3x entre costa e interior**. La política de vivienda *no puede* usar un ATE único. La historia **entrega heterogeneidad como hallazgo accionable**, no como nota al pie.

**Implicación epistémica:** Una historia con datos de causalidad observacional no termina en "β=0.35". Termina en: *¿qué diseño cuasi-experimental (boundary discontinuity, Bartik IV, regression discontinuity) me permitiría subir de la escalera causal observacional a una credibilidad mayor?* La historia con datos entrega la **escalera causal completa** (OLS → SAR → GBT → CATE → Oster δ) y deja explícito: *cada escalón corrige un sesgo del anterior, pero ningún escalón alcanza causalidad definitiva*. La heterogeneidad espacial (CATE 3x) no es un resultado más; es la **implicación de política**: una política de vivienda basada en el ATE promedio fallaría en costa e interior por igual. La historia con datos entrega heterogeneidad como *hallazgo accionable*, no como nota al pie.

---

## Síntesis Transversal: Qué une a las 5 como "Historias con Datos"

| Criterio | Análisis / Reporte / Dashboard | Nuestras 5 historias |
|----------|--------------------------------|----------------------|
| **Datos como protagonista** | Decoración / evidencia secundaria | **Estructura del dato dicta método**: missingness (CO2), jerarquía incompleta (Penguins), confounding espacial (CA), imbalance (Fraud), panel survival (Gapminder) |
| **Tensión narrativa** | Pregunta → Respuesta cerrada | **Pregunta → Exploración → Hallazgo → Limitación → Nueva pregunta** (no cierran, abren) |
| **Decisiones metodológicas** | "Usé X porque es estándar" | **Justificadas por el dato**: STL vs Prophet, FE vs RE, temporal split, crossed RE, Spatial Block CV |
| **Métricas** | Académicas (R², p-valor) | **Operacionales / Epistémicas**: Δppm/año², β_within vs β_between, PR-AUC@cost, ICC|adjusted, CATE spatial, Oster δ |
| **Validación** | In-sample / random split | **Respeta estructura**: rolling origin, LOOCV país, temporal split día1→día2, LOO-Island, Spatial Block CV |
| **Limitaciones** | "Más datos / correlación≠causalidad" | **Cuantificadas, severidad, mitigación concreta** (IV, MICE, GARCH, IPM, boundary discontinuity) |
| **Cierre** | "Se concluye que..." | **Próximo paso replicable con código y datos** (FaIR v2.0, DHS+IV, 90-day pipeline, IPM, Zillow+BDD) |
| **Reproducibilidad** | "Código disponible" | **environment.yml + download_data.py + seeds + nbconvert --execute** |

---

## Conclusión del Informe Crítico

Cada historia **no respondió al arquetipo por accidente**. El dataset *exigió* ese arquetipo:

1. **CO₂ Mauna Loa** → Serie temporal + cambio estructural: missingness invernal + estacionalidad dominante + breakpoint físico ≈ 1999.
2. **Gapminder** → Comparación + Paradoja Simpson: panel país⊂continente + varianza between dominante + endogeneidad PIB↔Salud.
3. **Credit Card Fraud** → Outliers + Anomalías: imbalance 0.17% + costos asimétricos 100:1 + concept drift + PCA anonimizado.
4. **Palmer Penguins** → Drill-down + Varianza: diseño incompleto (Biscoe=Gentoo) + ICC naked vs ajustado + LOO-Island CV.
5. **California Housing** → Causalidad espacial: Moran's I=0.32 + top-coding 5.2% + CATE 3x costa/interior + Oster δ=2.3.

**Todas comparten la misma epísteme:** *El dato no es insumo; es el que manda.* Las decisiones metodológicas (STL, FE, temporal split, crossed RE, Spatial Block CV) no son "elecciones del analista" —son **respuestas forzadas por la estructura del dato**. Las limitaciones no son excusas; son **agenda de investigación**. El cierre no es "fin"; es **próximo paso replicable con entorno computacional completo**.

Eso es lo que distingue una **historia con datos** de un análisis, un reporte, o un dashboard.

---

## Conclusión Final: Coherencia del Proyecto Completo

El proyecto presenta **coherencia interna total** entre los cinco ejes:

1. **Arquetipo ↔ Dataset ↔ Método**: Cada dataset *exige* su arquetipo por su estructura (missingness, jerarquía, imbalance, confounding, censoring). No hay "elección libre".
2. **Notebook ↔ Informe crítico**: Cada notebook ejecuta el análisis; el informe crítico lo *interpreta epistémicamente*. No hay duplicación; hay complementariedad.
3. **Código ↔ Narrativa**: Los notebooks usan `hallazgo()`, `limitacion()`, `conclusion_tecnica()` como puentes semánticos entre código y prosa. La narrativa no flota; está anclada a objetos computacionales.
4. **Validación honesta**: Rolling origin, LOOCV país, temporal split, LOO-Island, Spatial Block CV — cada validación *respeta la estructura del dato*, no la conveniencia del analista.
5. **Limitaciones como agenda**: Cada limitación tiene severidad, icono, y mitigación concreta (IV, MICE, GARCH, IPM, boundary discontinuity). No son excusas; son *próximos pasos*.
6. **Reproducibilidad real**: `environment.yml` + `environment-lite.yml` + `runtime.txt` + `Dockerfile` + `docker-compose.yml` + `build_all.py` + `.github/workflows/deploy.yml` + `.devcontainer/devcontainer.json` = 6 formas de ejecutar, 0 excusas.

**Este proyecto no es una colección de notebooks. Es un sistema coherente de 5 historias con datos, cada una demostrando que cuando la ciencia de datos se toma en serio como narrativa epistémica, el dato deja de ser insumo y se vuelve el director de orquesta.**

---

**Fin del Informe Crítico**  
*5 historias × ≥2 cuartillas = ≥10 cuartillas*  
*Entregado viernes 20 noviembre 2026*  
*MATCOM — Ciencia de Datos Avanzada*