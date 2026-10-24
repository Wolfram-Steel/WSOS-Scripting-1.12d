<div align="center">

# WSOS Scripting 1.12d

Búsqueda inteligente de enlaces técnicos y extracción limpia de contenido web, con interfaz gráfica.

Busca → filtra → organiza → extrae → genera datasets listos para RAG, IA o archivo.

[![Versión](https://img.shields.io/badge/versión-1.12d-e63946?style=for-the-badge)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Licencia](https://img.shields.io/badge/licencia-MIT-2ea44f?style=for-the-badge)](LICENSE)

[![Windows](https://img.shields.io/badge/Windows-ejecutable-0078D6?logo=windows&logoColor=white)](#-descargas)
[![Linux](https://img.shields.io/badge/Linux-ejecutable-FCC624?logo=linux&logoColor=black)](#-descargas)
[![UI](https://img.shields.io/badge/UI-Flet-8A2BE2)](https://flet.dev/)
[![Compilado con](https://img.shields.io/badge/compilado%20con-Nuitka-informational)](https://nuitka.net/)

[**⬇️ Descargas**](#-descargas) · [**🚀 Inicio rápido**](#-inicio-rápido) · [**📖 Guía de uso**](#-guía-de-uso) · [**🧬 Arquitectura**](#-arquitectura) · [**🇬🇧 English**](#-english-summary)

</div>

---

## ✨ Qué hace

| | Paso | Detalle |
|:-:|---|---|
| 🔎 | **Buscar** | Enlaces relevantes con DuckDuckGo, multi-región y en paralelo. |
| 🧹 | **Filtrar** | Bloquea publicidad, trackers, parámetros `utm_*`/`gclid` y extensiones binarias. |
| 🗂️ | **Organizar** | Guarda las URLs en categorías persistentes (`config/webs.json`). |
| 📄 | **Extraer** | HTML → texto limpio (conserva código, tablas y títulos). PDF opcional. |
| 📦 | **Generar** | Datasets por lotes con metadatos, *Quality Score*, SHA-256 y manifiesto `.wsos.json`. |

Todo desde una interfaz en modo oscuro con consola en tiempo real, parada segura y perfiles de recopilación configurables.

---

## ⬇️ Descargas

La forma más sencilla: **no necesitas instalar Python**. Descarga el ejecutable de tu sistema desde la página de [**Releases**](../../releases/latest).

| Sistema | Archivo | Cómo ejecutarlo |
|---|---|---|
| 🪟 **Windows** (64 bits) | `WSOS-Scripting-1.12d-windows.exe` | Doble clic. |
| 🐧 **Linux** (64 bits) | `WSOS-Scripting-1.12d-linux` | `chmod +x WSOS-Scripting-1.12d-linux && ./WSOS-Scripting-1.12d-linux` |

Ambos binarios están compilados con [Nuitka](https://nuitka.net/) a partir de este mismo código fuente.

> [!NOTE]
> En Windows, al ser un ejecutable sin firma digital, SmartScreen puede mostrar un aviso la primera vez. Pulsa **Más información → Ejecutar de todas formas**.
> Si prefieres no ejecutar binarios de terceros, puedes lanzar el programa desde el código fuente (ver abajo).

---
ale el programa en python es WSOS-Scripting los otros son los compilados para Windows y Linux... en el WSOS está el readme.md pero no 
## 🚀 Inicio rápido

### Opción A · Ejecutable (Windows / Linux)

1. Descarga el binario desde [Releases](../../releases/latest).
2. Ejecútalo.
3. Crea una categoría y lanza tu primera búsqueda ([guía de uso](#-guía-de-uso)).

### Opción B · Desde el código fuente (Windows / Linux / macOS)

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/WSOS-Scripting.git
cd WSOS-Scripting

# 2. Instalar dependencias y preparar la configuración
python3 instalar.py

# 3. Lanzar la aplicación
python3 main.py
```

> `instalar.py` (o `python3 app/actualizador.py`) instala las dependencias de `config/requirements.txt` y crea la plantilla inicial `config/webs.json`.

**Requisitos:** Python 3.10+, conexión a Internet y estas dependencias: `flet`, `requests`, `beautifulsoup4`, `lxml`, `pypdf` (PDF opcional) y `ddgs`.

---

## 📖 Guía de uso

### 1 · Crear una categoría *(obligatorio antes de buscar)*
1. Pulsa el botón morado **Categorías** (arriba a la derecha).
2. Escribe un nombre (`python_docs`, `cpu`, `electronica`…) y pulsa **Añadir**.

### 2 · Buscar webs
1. En **Selecciona la Operación** elige **Búsqueda webs**.
2. Indica keywords, región y categoría de destino. Las URLs se guardan en `config/webs.json`.
3. *(Opcional)* Activa **Modo WSOS** o **Búsqueda Sucia** (son excluyentes).
4. Elige el **perfil de recopilación**, el objetivo y la identidad del proyecto (autor, licencia…).
5. Pulsa **Ejecutar Proceso**.

### 3 · Extraer el contenido de una categoría
1. Selecciona la categoría en el desplegable principal.
2. Pulsa **Ejecutar Proceso**.
3. Se aplica el perfil elegido y se generan `categoria_part_1.txt`, `categoria_part_2.txt`… en la carpeta de salida.

```text
Crear categoría  →  Configurar perfil  →  Buscar enlaces  →  (revisar webs.json)  →  Extraer  →  Usar los *_part_N.txt y .wsos.json
```

---

## 🎛️ Modos de búsqueda

| Modo | Qué hace | Úsalo para |
|---|---|---|
| **Estándar** | Keywords tal cual + filtro de trackers (~5 resultados/término). | Búsquedas precisas. |
| **Modo WSOS** | Expande con `documentation`, `github`, `tutorial`, `source code`, `examples`; valida contenido y Quality Score. Genera `dataset_wsos_*.txt` + manifiesto. | Datasets técnicos de calidad. |
| **Búsqueda Sucia** | Expande con ~19 sufijos y **sin** filtro de trackers. Genera `dataset_dirty_*.txt` + manifiesto. | Máximo volumen de enlaces. |

**Regiones:** España (`es-es`) · USA (`us-en`) · UK (`uk-en`) · Global (`wt-wt`).

## ⚙️ Perfiles de recopilación

| Perfil | Calidad mín. | Chars mín. | Workers | Rate limit | Uso típico |
|---|:-:|:-:|:-:|:-:|---|
| **Rápido** | 50 | 250 | 10 | 0.05 s | Exploración rápida |
| **Equilibrado** *(defecto)* | 70 | 300 | 8 | 0.10 s | Uso general |
| **Seguro** | 80 | 400 | 5 | 0.20 s | Sitios sensibles, menos agresivo |
| **Dataset IA** | 80 | 1000 | 8 | 0.10 s | Alta calidad para RAG/IA |

La búsqueda en DuckDuckGo usa **hasta 3 workers** con un limitador adaptativo (parte de 1 petición/s); la descarga de páginas usa los workers del perfil, con tope global de **16**.

---

## 🧬 Arquitectura

```text
WSOS-Scripting/
├── main.py              # Punto de entrada
├── instalar.py          # Instalador rápido de dependencias
├── app/
│   ├── ui.py            # Interfaz Flet, hilos y consola
│   ├── scraping.py      # Orquestador de búsqueda, categorías y dataset
│   └── actualizador.py  # Verificación e instalación del entorno
├── core/
│   ├── buscadores.py    # Motor DuckDuckGo (thread-safe)
│   ├── bloqueos.py      # Filtros de URL, trackers y dominios
│   ├── procesador.py    # Descarga HTML/PDF y extracción de texto
│   ├── categorias.py    # Scraping de categorías y particionado
│   ├── dataset.py       # Perfiles, calidad, metadatos y manifiestos
│   ├── red.py           # Sesiones HTTP, rate limit y reintentos
│   ├── paralelo.py      # Paralelismo acotado y parada cooperativa
│   ├── config.py        # Persistencia y rutas
│   └── version.py       # Versión única
├── config/              # webs.json · settings.json · requirements.txt
├── tests/               # Batería offline + corpus de 20 páginas HTML
└── docs/                # Seguridad, calidad y estructura
```

### Archivos que genera

| Archivo | Origen | Contenido |
|---|---|---|
| `config/webs.json` | Búsqueda webs | Categorías y URLs encontradas |
| `config/settings.json` | Ajustes de la UI | Preferencias recordadas |
| `salida/runs/<RUN-ID>/dataset_wsos_*.txt` | Modo WSOS | Contenido limpio validado + Quality Score |
| `salida/runs/<RUN-ID>/dataset_dirty_*.txt` | Búsqueda Sucia | Contenido limpio sin filtro de trackers |
| `salida/runs/<RUN-ID>/*.wsos.json` | WSOS / Sucia | Manifiesto: metadatos, estadísticas, documentos |
| `<categoria>_part_N.txt` | Extracción de categoría | Texto estructurado por fuente |

Formato de `config/webs.json`:

```json
{
    "cpu": [
        "https://es.wikipedia.org/wiki/Unidad_central_de_proceso",
        "https://es.wikipedia.org/wiki/Microprocesador"
    ]
}
```

---

## 🆕 Novedades de la 1.12d

- **`instalar.py`** en la raíz: instalación y puesta en marcha en un solo comando.
- **Calidad estática:** `ruff`, `bandit`, `safety` y `mypy` integrados en CI; tipado verificado con 0 errores en mypy.
- **Ejecutables** para Windows y Linux compilados con Nuitka.
- Escritura de datasets **atómica** y un directorio por ejecución (`salida/runs/<RUN-ID>/`).

Historial completo en el [CHANGELOG](CHANGELOG.md).

---

## 🛠️ Desarrollo y calidad

```bash
python -m pip install -r config/requirements.txt
ruff check .
bandit -r core/ app/
mypy core/ app/
python -m pytest -q
```

Más detalle en [`docs/CALIDAD_Y_SEGURIDAD_1.12d.md`](docs/CALIDAD_Y_SEGURIDAD_1.12d.md) y [`docs/SECURITY.md`](docs/SECURITY.md).

---

## 🩺 Solución de problemas

| Problema | Solución |
|---|---|
| No se encuentra `config/webs.json` | Ejecuta `python3 instalar.py` o créalo manualmente. |
| Error al importar `ddgs` / `flet` / `pypdf` | Reejecuta `python3 instalar.py` o `pip install -r config/requirements.txt`. |
| Pocos resultados | Cambia de región, activa WSOS o Búsqueda Sucia, amplía las keywords. |
| Errores frecuentes de DuckDuckGo | Usa el perfil **Seguro** o baja `MAX_SEARCH_WORKERS` en `app/scraping.py`. |
| La ventana no cierra limpia | Pulsa **Detener Proceso** antes de cerrar si hay una tarea en curso. |
| El binario de Linux no arranca | Comprueba que tiene permiso de ejecución: `chmod +x`. |

---

## ⚖️ Aviso legal

Proyecto bajo licencia [MIT](LICENSE). WSOS Scripting está pensado **con fines educativos, de investigación y de automatización de flujos personales**. El autor no se hace responsable de su mal uso. Es responsabilidad del usuario:

- Cumplir los términos de servicio de los sitios consultados.
- Respetar la legislación aplicable (derechos de autor, privacidad).
- No sobrecargar servidores ajenos con peticiones abusivas.

---

## 🇬🇧 English summary

**WSOS Scripting** is a desktop app (Flet GUI) that searches technical links via DuckDuckGo, filters ads/trackers, organizes URLs into categories and extracts clean text/Markdown into datasets with quality scores and manifests.

- **Windows / Linux:** download the prebuilt binary (compiled with Nuitka) from [Releases](../../releases/latest).
- **From source:**

```bash
python3 instalar.py   # install dependencies & prepare config
python3 main.py       # launch the app
```

---

<div align="center">

Hecho por **Wolfram Steel** · [MIT License](LICENSE)

</div>
