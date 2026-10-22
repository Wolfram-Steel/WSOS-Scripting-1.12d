# WSOS Scripting 1.12d

**Herramienta de escritorio para búsqueda inteligente de enlaces técnicos y extracción limpia de contenido web.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flet](https://img.shields.io/badge/UI-Flet-purple)](https://flet.dev/)
[![License](https://img.shields.io/badge/License-Educational-orange)](#aviso-legal)
[![Version](https://img.shields.io/badge/Version-1.12d-red)](CHANGELOG.md)
[![Concurrency](https://img.shields.io/badge/Search-Nested%20Parallel-brightgreen)](CHANGELOG.md)

> **Autor:** Wolfram Steel  
> **Idioma de la interfaz:** Español  
> **Plataforma:** Multiplataforma (Windows / Linux / macOS)

---

## ⚡ Instalación rápida

Inicia el proyecto en solo 3 pasos:

```bash
# 1. Clonar o descargar el repositorio
git clone <url-del-repositorio>
cd <carpeta-del-proyecto>

# 2. Configurar entorno y dependencias mediante el script raíz
python3 instalar.py

# 3. Lanzar la aplicación
python3 main.py
```

> **Nota:** El script `instalar.py` (o `python3 app/actualizador.py`) verifica el entorno Python, instala/actualiza las dependencias necesarias desde `config/requirements.txt` y crea la estructura inicial de configuración (`config/webs.json`).

---

## Tabla de contenidos

- [Instalación rápida](#-instalación-rápida)
- [Descripción](#descripción)
- [Novedades de la versión 1.12d](#novedades-de-la-versión-112d)
- [Novedades de la versión 1.12](#novedades-de-la-versión-112)
- [Características principales](#características-principales)
- [Arquitectura del proyecto](#arquitectura-del-proyecto)
- [Requisitos](#requisitos)
- [Guía de uso](#guía-de-uso)
- [Modos de búsqueda avanzados](#modos-de-búsqueda-avanzados)
- [Perfiles de recopilación](#perfiles-de-recopilación)
- [Búsqueda anidada (paralela)](#búsqueda-anidada-paralela)
- [Flujo de trabajo recomendado](#flujo-de-trabajo-recomendado)
- [Estructura de archivos generados](#estructura-de-archivos-generados)
- [Configuración (`config/webs.json`)](#configuración-websjson)
- [Ajuste de rendimiento](#ajuste-de-rendimiento)
- [Solución de problemas](#solución-de-problemas)
- [Aviso legal](#aviso-legal)
- [English summary](#english-summary)

---

## Descripción

**WSOS Scripting** automatiza el ciclo completo de recopilación de información técnica:

1. **Búsqueda** de enlaces relevantes mediante DuckDuckGo (multi-región).
2. **Filtrado** estricto de publicidad, rastreadores, parámetros de tracking y extensiones binarias.
3. **Organización** de URLs en categorías persistentes (`config/webs.json`).
4. **Extracción** de contenido limpio (HTML → texto estructurado), preservando bloques de código; soporte opcional de PDF.
5. **Generación** de datasets por lotes listos para bases de conocimiento, RAG o análisis posterior, con metadatos, Quality Score y manifiesto `.wsos.json`.

Todo desde una interfaz gráfica moderna en modo oscuro, con consola de logs en tiempo real, control de parada segura, **búsqueda anidada en paralelo** y perfiles de recopilación configurables.

---

## Novedades de la versión 1.12d

La versión 1.12d incorpora controles de calidad estática, tipado estricto (mypy) y ejecuta comprobaciones de lint, seguridad, dependencias y tipos en integración continua. La configuración de estas herramientas está en la raíz del repositorio para que los comandos estándar funcionen desde el directorio principal.

### Script de instalación raíz (`instalar.py`)
- Se incluye `instalar.py` en la raíz del proyecto para simplificar y acelerar la puesta en marcha de la aplicación y la actualización automática de dependencias.

1.12c es una versión de **consolidación**: mantiene `ThreadPoolExecutor` y la arquitectura de 1.12, y se concentra en extracción DOM, búsqueda más conservadora, pruebas de regresión y escritura segura. No introduce `asyncio`, Playwright, SQLite, embeddings, plugins ni reorganización mayor.

### Extracción DOM

- `<form>` ya no se elimina por defecto: se conserva cuando contiene contenido documental útil, incluyendo escenarios WebForms.
- `<nav>` y `<aside>` se evalúan **antes de aplanar el HTML**, usando densidad de enlaces y estructura DOM; un bloque `<p>`/`article`/`section` útil no se descarta por ser corto.
- Se conservan líneas técnicas cortas como `CPU`, `HTTP 200` o `E = mc²`.
- La eliminación de secciones finales (`Referencias`, `Notas`, etc.) ya no se decide sobre texto aplanado: solo se elimina una sección DOM cuando existe evidencia suficiente de alta densidad de enlaces.
- Se añadió un corpus local de 20 páginas HTML para regresión de WebForms, navegación, aside, código, tablas, fórmulas y referencias.

### Búsqueda y estabilidad

- La búsqueda anidada se limita a **3 workers** y parte de **1 petición/segundo** mediante un limitador compartido adaptativo; ante errores aumenta temporalmente el intervalo y lo recupera gradualmente.
- La Búsqueda Sucia ya no añade el sufijo `pdf` cuando `allow_pdf=False`. Los redirectores publicitarios continúan bloqueados.
- `fetch_urls_with_fallbacks()` se renombra a `fetch_urls()` porque 1.12c usa un único motor y no contiene fallbacks reales.

### Rendimiento del motor

- La búsqueda DuckDuckGo y la descarga de documentos utilizan **pools separados**: la búsqueda queda limitada a **3 workers** por seguridad frente a rate-limit; las descargas utilizan los workers definidos por el perfil, con un tope global de **16**.
- `core/paralelo.py` mantiene una **ventana acotada de futures**: nunca se encolan más tareas que workers disponibles. Esto reduce memoria y trabajo pendiente en búsquedas masivas/categorías grandes sin cambiar el orden de resultados.
- Las descargas reutilizan `requests.Session()` por worker, mantienen keep-alive/connection pooling y aplican rate limiting independiente por dominio.
- Los manifiestos de dataset incluyen telemetría `stats.timings` (`search_seconds`, `filter_dedup_seconds`, `output_prepare_seconds`, `dataset_seconds`, `total_seconds`) y `stats.parallelism`, para localizar cuellos de botella sin activar herramientas externas de profiling.

### Datasets y ejecución segura

- Cada ejecución automática recibe su propio `Run ID` y directorio `salida/runs/<RUN-ID>/`.
- El dataset se escribe primero en un temporal y se publica mediante `os.replace`; una escritura interrumpida no sustituye un dataset válido anterior.
- Las ejecuciones ya no comparten el mismo `dataset_wsos_*.txt` ni su manifiesto.
- `SCHEMA_VERSION` pasa a `1.12d` y la versión del motor pasa a `1.12d`.

### UI y calidad del proyecto

- La consola Flet utiliza una cola de eventos y actualiza los mensajes en lotes para reducir repintados por cada `print()`.
- El campo **Carpeta de salida** incorpora un **icono pequeño de carpeta** a su derecha; al pulsarlo se abre el selector nativo de carpetas, y la carpeta elegida se escribe automáticamente en el campo y queda guardada en los ajustes.
- Se añade `config/pyproject.toml` con configuración Ruff y GitHub Actions para ejecutar Ruff y la batería offline de tests.
- La batería pasa de 54 a **62 tests**.

---

## Novedades de la versión 1.12b

Versión de **corrección y robustez**: arregla fallos que impedían obtener contenido útil y hace que los perfiles controlen de verdad lo que prometían.

### Correcciones importantes

- **Filtro de ruido**: antes descartaba prácticamente todo el texto (un patrón con `re.I` casaba con cualquier par de letras). Ahora la prosa se conserva y solo se eliminan líneas de menú, copyright, referencias numéricas y secciones finales (*Referencias*, *Enlaces externos*…).
- **Párrafos intactos**: los enlaces y el texto en cursiva ya no parten un párrafo en fragmentos; `<code>` en línea queda como `` `código` ``; se conservan títulos (`#`), listas y tablas.
- **URLs de Wikipedia**: ya no se corta el `)` final de `.../Python_(lenguaje)`; los artículos tipo `/wiki/Node.js` no se confunden con ficheros `.js`.
- **Quality Score recalibrado**: mide variedad, densidad de frases y proporción de texto (no solo longitud). Prosa real: 83–96 puntos; texto repetido o listas de enlaces: menos de 55. Los umbrales de los perfiles (50 / 70 / 80) ahora tienen sentido.
- **Categorías**: `CPU` y `cpu` ya son la misma categoría (antes se creaba una duplicada). Los nombres de archivo salen del nombre exacto de la categoría y se sanean.
- **`config/webs.json` seguro**: escritura atómica, copia `webs.json.corrupt-…` si el JSON está dañado (en vez de cerrar la app) y deduplicación por URL normalizada.
- **Actualizador**: `beautifulsoup4` ya se detecta bien (módulo `bs4`) y no se reinstala en cada ejecución; ahora usa `config/requirements.txt`.

---

## Novedades de la versión 1.12

La versión 1.12 mantiene la arquitectura paralela de 1.11 y añade **robustez, rendimiento y trazabilidad**.

### Control y red

- Parada cooperativa reforzada con checkpoints en búsqueda, descarga y escritura.
- Los `Future` pendientes se cancelan y los `ThreadPoolExecutor` se cierran sin bloquear la interfaz.
- Peticiones HTTP con timeout explícito, hasta 3 intentos y **exponential backoff con jitter**.
- **Rate limiting independiente por dominio** (paraleliza hosts distintos sin saturar uno solo).
- `requests.Session()` **persistente por worker** con connection pooling / keep-alive.
- Barra de progreso determinada conectada al número real de tareas completadas.

### Motor y trazabilidad

- **Perfiles de recopilación**: Rápido, Equilibrado, Seguro y Dataset IA (calidad mínima, workers, rate limit y reintentos).
- **Objetivo del dataset**: Investigación, Educación, Programación, Documentación técnica, Dataset IA, Archivo web o Personalizado.
- **Identidad del proyecto**: autor, proyecto/Project ID, organización, idioma, descripción y **licencia**.
- **Trazabilidad**: cada dataset recibe `Dataset ID`, `Run ID`, fecha y versión del motor.
- **Quality Score** 0–100 por documento antes de entrar al dataset.
- **SHA-256** del contenido y **deduplicación por hash**.
- **Normalización de URLs** (eliminación de `utm_*`, `gclid`, etc.) antes del scraping.
- **Manifiesto WSOS** (`.wsos.json`) con identidad, estadísticas y documentos aceptados.
- **WSOS Engine Report**: calidad media, velocidad y tiempo en la consola.
- Estadísticas finales visibles (válidos, descartados, duplicados, caracteres).

---

## Características principales

| Característica | Detalle |
|----------------|---------|
| **Interfaz Flet** | Modo oscuro, consola en vivo, barra de progreso y botones con animación. |
| **Búsqueda multi-región** | España (`es-es`), USA (`us-en`), UK (`uk-en`) y Global (`wt-wt`). |
| **Búsqueda anidada** | Keywords en paralelo (hasta 3 hilos) con parada segura. |
| **Filtro de URLs** | Bloqueo de dominios publicitarios, trackers y extensiones binarias. |
| **Modo WSOS** | Expansión semántica de keywords + validación de contenido + `dataset_wsos_*.txt`. |
| **Búsqueda Sucia** | Expansión masiva de términos + sin filtro de trackers → máximo volumen. |
| **Perfiles de recopilación** | Rápido / Equilibrado / Seguro / Dataset IA (calidad, workers, rate limit). |
| **Gestión de categorías** | Crear / eliminar desde diálogo modal; persistencia en `config/webs.json`. |
| **Extracción inteligente** | BeautifulSoup + limpieza de ruido y boilerplate; preservación de código Markdown. |
| **Soporte PDF** | Extracción opcional de texto de PDFs con `pypdf`. |
| **Scraping paralelo** | De 5 a 10 descargas HTTP concurrentes según perfil. |
| **Manifiesto WSOS** | `.wsos.json` con Dataset ID, Run ID, Quality Score, SHA-256 y estadísticas. |
| **Parada segura** | `threading.Event` interrumpe búsquedas y descargas (incluida una descarga en curso); una consulta de DuckDuckGo ya lanzada termina antes de parar. |
| **Auto-configurador** | `instalar.py` / `app/actualizador.py` instala dependencias y crea plantilla de `config/webs.json`. |

---

## Arquitectura del proyecto

La raíz se mantiene deliberadamente limpia: los únicos archivos de usuario visibles en ella son `main.py`, `instalar.py`, `README.md` y `CHANGELOG.md`. El código de aplicación, configuración, pruebas y documentación auxiliar se agrupa por responsabilidad.

```text
WSOS Scripting/
├── main.py                 # Punto de entrada; importa la UI desde app/
├── instalar.py             # Script de instalación y configuración rápida en la raíz
├── README.md               # Manual principal
├── CHANGELOG.md            # Historial de cambios
├── app/
│   ├── __init__.py
│   ├── ui.py               # Interfaz Flet, hilos y consola
│   ├── scraping.py         # Orquestador de búsqueda, categorías y dataset
│   └── actualizador.py     # Lógica interna de instalación y verificación
├── core/
│   ├── __init__.py
│   ├── buscadores.py       # Motor DuckDuckGo (DDGS) thread-safe
│   ├── bloqueos.py         # Filtros de URL, trackers y dominios
│   ├── procesador.py       # Descarga HTML/PDF y extracción de texto
│   ├── categorias.py       # Scraping de categorías y particionado
│   ├── config.py           # Persistencia y rutas de config/
│   ├── paralelo.py         # Paralelismo acotado y parada cooperativa
│   ├── version.py          # Versión única 1.12d
│   ├── dataset.py          # Perfiles, calidad, metadatos y manifiestos
│   └── red.py              # Sesiones HTTP, rate limit y reintentos
├── config/
│   ├── webs.json           # Categorías y URLs persistentes
│   ├── settings.json       # Ajustes de UI; se crea al ejecutar
│   ├── requirements.txt    # Dependencias Python
│   └── pyproject.toml      # Configuración Ruff
├── tests/                  # 62 pruebas offline/locales
├── docs/                   # Informes y documentación técnica complementaria
└── .github/
    └── workflows/ci.yml    # CI: dependencias, Ruff y tests
```

---

## Requisitos

- **Python** 3.10 o superior
- Conexión a Internet
- Dependencias (listadas en `config/requirements.txt` e instaladas por `instalar.py`):
  - `flet`
  - `requests`
  - `beautifulsoup4`
  - `lxml`
  - `pypdf` (soporte PDF opcional)
  - `ddgs`

---

## Calidad estática y seguridad (1.12d)

Para ejecutar las comprobaciones de desarrollo desde la raíz del proyecto, instala las herramientas y ejecuta:

```bash
python -m pip install -r config/requirements.txt -r requirements-dev.txt
ruff check .
bandit -r core/ app/
safety check -r config/requirements.txt
mypy core/ app/
python -m pytest -q
```

---

## Guía de uso

### 1. Crear una categoría (obligatorio antes de buscar)

1. Pulsa el botón morado **Categorías** (arriba a la derecha).
2. Escribe un nombre (ej. `python_docs`, `cpu`, `electronica`).
3. Pulsa **Añadir** y cierra el panel.

### 2. Búsqueda de webs

1. En **Selecciona la Operación** elige **Búsqueda webs**.
2. Rellena keywords, región y categoría de destino. Las URLs se guardan directamente en `config/webs.json`.
3. (Opcional) Activa **Modo WSOS** o **Búsqueda Sucia** (excluyentes).
4. Configura el **perfil de recopilación**, objetivo e identidad del proyecto (autor, licencia, etc.).
5. Pulsa **Ejecutar Proceso**.

### 3. Extracción de contenido de una categoría

1. Selecciona la categoría en el desplegable principal.
2. Pulsa **Ejecutar Proceso**.
3. Se aplica el **perfil elegido** y se generan `categoria_part_1.txt`, `categoria_part_2.txt`, … en la carpeta de salida.

---

## Modos de búsqueda avanzados

| Modo | Qué hace | Cuándo usarlo |
|------|----------|---------------|
| **Estándar** | Keywords tal cual + filtro de trackers. ~5 resultados/término. | Búsquedas precisas. |
| **Modo WSOS** | Expande con `documentation`, `github`, `tutorial`, `source code`, `examples`. Valida contenido y Quality Score. Genera `dataset_wsos_*.txt` + manifiesto. | Datasets técnicos de calidad. |
| **Búsqueda Sucia** | Expande con ~19 sufijos. Sin filtro de trackers. Genera `dataset_dirty_*.txt` + manifiesto. | Máximo volumen de enlaces. |

---

## Perfiles de recopilación

Disponibles desde la interfaz (desplegable **Perfil de recopilación**):

| Perfil | Calidad mín. | Chars mín. | Workers | Rate limit | Uso típico |
|--------|--------------|------------|---------|------------|------------|
| **Rápido** | 50 | 250 | 10 | 0.05 s | Exploración rápida |
| **Equilibrado** | 70 | 300 | 8 | 0.10 s | Uso general (por defecto) |
| **Seguro** | 80 | 400 | 5 | 0.20 s | Sitios sensibles / menos agresivo |
| **Dataset IA** | 80 | 1000 | 8 | 0.10 s | Datasets de alta calidad para RAG/IA |

---

## Búsqueda anidada (paralela)

| Fase | Workers por defecto | Archivo |
|------|---------------------|---------|
| Consultas DuckDuckGo por keyword | **hasta 3** | `app/scraping.py` → `MAX_SEARCH_WORKERS` |
| Descarga de páginas (dataset WSOS/Sucia y categorías) | **5–10** según perfil, máximo global 16 | `core/dataset.py` → `PROFILES` + `HARD_WORKER_CAP` |

---

## Flujo de trabajo recomendado

```text
1. Crear categoría(s)          →  Categorías → Añadir
2. Configurar perfil e identidad →  Perfil, autor, licencia, objetivo
3. Buscar enlaces              →  Búsqueda webs + región + categoría destino
4. (Opcional) Revisar `config/webs.json`
5. Extraer contenido           →  Seleccionar categoría → Ejecutar
6. Usar los *_part_N.txt y .wsos.json →  RAG, análisis, documentación, etc.
```

---

## Estructura de archivos generados

| Archivo | Origen | Contenido |
|---------|--------|-----------|
| `config/webs.json` | Búsqueda webs / Persistente | Categorías y URLs encontradas |
| `config/settings.json` | Persistente | Ajustes recordados de la interfaz |
| `salida/runs/<RUN-ID>/dataset_wsos_*.txt` | Modo WSOS | Contenido limpio validado + Quality Score |
| `salida/runs/<RUN-ID>/dataset_dirty_*.txt` | Búsqueda Sucia | Contenido limpio (sin filtro de trackers) |
| `salida/runs/<RUN-ID>/*.wsos.json` | Modo WSOS / Sucia | Manifiesto: metadatos, stats, documentos |
| `<categoria>_part_N.txt` | Extracción de categoría | Texto estructurado por fuente |
| `config/instalacion_log.txt` | `instalar.py` | Log de instalación |

---

## Configuración (`config/webs.json`)

```json
{
    "cpu": [
        "https://es.wikipedia.org/wiki/Unidad_central_de_proceso",
        "https://es.wikipedia.org/wiki/Microprocesador"
    ],
    "programacion": [
        "https://es.wikipedia.org/wiki/Python",
        "https://docs.python.org/3/"
    ]
}
```

---

## Ajuste de rendimiento

Si DuckDuckGo limita peticiones o la red es inestable, elige el perfil **Seguro** o reduce los workers de búsqueda:

```python
# app/scraping.py
MAX_SEARCH_WORKERS = 3   # Búsqueda conservadora; el limitador compartido parte de 1 s
```

---

## Solución de problemas

| Problema | Solución |
|----------|----------|
| `No se encuentra config/webs.json` | Ejecutar `python3 instalar.py` o crear `config/webs.json` manualmente. |
| Error al importar `ddgs` / `flet` / `pypdf` | Reejecutar `python3 instalar.py` o `pip install -r config/requirements.txt`. |
| Pocos resultados | Probar otra región, activar WSOS o Búsqueda Sucia, ampliar keywords. |
| Errores frecuentes en DDGS | Bajar `MAX_SEARCH_WORKERS` o usar perfil **Seguro**. |
| UI no cierra limpia | Usar **Detener Proceso** antes de cerrar si hay una tarea en curso. |

---

## Aviso legal

El autor **no se hace responsable** del mal uso de esta herramienta.  
WSOS Scripting está diseñado **estrictamente con fines educativos, de investigación y de automatización de flujos de desarrollo personales**.

Es responsabilidad del usuario:
- Cumplir los términos de servicio de los sitios web consultados.
- Respetar las leyes aplicables (derechos de autor y privacidad).
- No sobrecargar servidores ajenos con peticiones abusivas.

---

## English summary

**WSOS Scripting 1.12d** is a desktop tool (Flet GUI) that searches technical links, filters trackers/ads, organizes URLs into categories, and extracts clean markdown/text content.

```bash
python3 instalar.py   # Install dependencies & prepare config
python3 main.py       # Launch application
```

- **v1.12d** brings full static typing (`mypy` with 0 errors), automated environment setup via `instalar.py`, and CI integration for linting, security, and tests.