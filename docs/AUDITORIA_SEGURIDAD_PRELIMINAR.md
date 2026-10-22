# Informe de endurecimiento técnico — WSOS-Scripting 1.12c

**Estado:** revisión preliminar y correcciones locales aplicadas.  
**Fecha:** 2026-10-21.  
**Alcance:** código Python, pruebas automatizadas y configuración incluida en el archivo recibido.

## Cambios realizados

1. **Corrección de una prueba de calidad mal planteada.** La prueba esperaba una puntuación alta para 500 repeticiones de una misma frase, aunque el algoritmo penaliza correctamente el texto repetitivo. Se sustituyó el ejemplo por prosa variada; no se relajó el algoritmo para hacer pasar texto repetido.
2. **Validación temprana de solicitudes HTTP.** `request_with_retry` rechaza esquemas distintos de HTTP/HTTPS, URL sin host, credenciales incrustadas y cantidades de reintentos fuera del intervalo permitido.
3. **Límites de descarga.** `fetch_bounded` valida los límites de bytes y el plazo total para evitar configuraciones no válidas o excesivas.
4. **Instalador de dependencias.** Antes de invocar `pip`, se valida la sintaxis de los requisitos y se rechazan opciones de pip, URL y rutas locales.
5. **Configuración defensiva.** `load_settings` solo acepta valores del tipo esperado, limita cadenas y limita el número de dominios bloqueados personalizados.
6. **Pruebas de regresión.** Se añadieron casos para entradas de red, requisitos potencialmente peligrosos y configuración con tipos incorrectos.
7. **Documentación.** Se añadió `SECURITY.md` con prácticas recomendadas, controles presentes, limitaciones y evidencias que conviene mantener para un SGSI.
8. **Integración continua.** Se añadió un flujo de GitHub Actions para ejecutar la suite de pruebas en cada push y pull request.

## Verificación realizada

- Suite `pytest`: **70 pruebas superadas, 0 fallidas**.
- Compilación sintáctica de `app`, `core` y `main.py` mediante `compileall`: correcta.

Estas comprobaciones son pruebas locales, no una auditoría independiente. No se ejecutó la suite en Windows y no se pudo certificar aquí el comportamiento de la actualización automática en ese sistema.

## Riesgos pendientes / límites de esta revisión

- La validación de esquema HTTP/HTTPS **no constituye una defensa completa contra SSRF**. Para un despliegue que procese URL no confiables hace falta una política explícita para destinos privados, resolución DNS y redirecciones, teniendo en cuenta si el uso legítimo incluye intranets.
- Las redirecciones HTTP siguen habilitadas por `requests`; deben revisarse junto con la política de destinos permitidos antes de usar el programa en un entorno sensible.
- La actualización automática de Windows genera un script `.bat`; necesita pruebas y revisión específica de rutas, permisos, integridad del paquete y recuperación.
- `config/requirements.txt` usa rangos de versiones. Para una cadena de suministro reproducible, se recomienda un lockfile revisado, hashes de distribución y análisis de vulnerabilidades de dependencias en CI.
- No se ha realizado fuzzing extensivo, prueba de penetración, revisión independiente de cada ruta de código ni análisis completo de dependencias.
- La ausencia de hallazgos en esta revisión no implica ausencia de vulnerabilidades.

## ISO/IEC 27001

ISO/IEC 27001 certifica un **sistema de gestión de seguridad de la información de una organización**, no un programa Python aislado. Este repositorio puede aportar evidencias técnicas, pero no demuestra por sí mismo la conformidad ni garantiza una certificación.

Para avanzar hacia una evaluación real, la organización deberá definir el alcance del SGSI, evaluar y tratar riesgos, mantener la declaración de aplicabilidad y políticas pertinentes, asignar responsabilidades, gestionar accesos y cambios, registrar incidentes, controlar proveedores y dependencias, probar copias de seguridad y continuidad, y conservar evidencias de operación y mejora continua.

## Recomendación prioritaria

Antes de declarar el software apto para un entorno sensible, abordar como mínimo la política de SSRF/redirecciones, la actualización de Windows y el bloqueo reproducible de dependencias; después ejecutar análisis estático y de dependencias en CI y realizar una revisión independiente.
