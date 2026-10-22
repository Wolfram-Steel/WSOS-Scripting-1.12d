# Calidad y seguridad — WSOS Scripting 1.12d

## Ejecutar comprobaciones

Desde la raíz del repositorio y dentro de un entorno virtual:

```bash
python -m pip install -r config/requirements.txt -r requirements-dev.txt
ruff check .
bandit -r core/ app/
safety check -r config/requirements.txt
mypy core/ app/
python -m pytest -q
```

La integración continua ejecuta estos controles en cada `push` y `pull_request`.

## Qué significa cada control

- **Ruff:** reglas de estilo, importaciones y errores estáticos comunes.
- **Bandit:** patrones de código potencialmente inseguros; los resultados deben revisarse en contexto, especialmente los usos intencionados de procesos externos.
- **Safety:** compara dependencias declaradas con su base de vulnerabilidades conocidas. No detecta fallos propios del código y el resultado depende de la base de datos disponible y de la versión de Safety.
- **mypy:** verifica consistencia de tipos dentro de los límites de la configuración actual; no sustituye las pruebas en tiempo de ejecución.
- **pytest:** comprueba regresiones funcionales cubiertas por la suite.

## Estado de verificación de esta entrega

- Suite local `pytest`: **70 passed**.
- `compileall` de `core/`, `app/` y `main.py`: correcto.
- Ruff, Bandit, Safety y mypy: **no ejecutados localmente en el entorno de empaquetado**, porque no había conectividad al índice de paquetes para instalarlos. El workflow de GitHub Actions los ejecuta en un entorno con dependencias instalables; hay que revisar el resultado real del workflow antes de afirmar que pasan.

Ninguna de estas herramientas certifica por sí sola que el software sea seguro. Los hallazgos deben triagarse, corregirse y volver a verificarse.
