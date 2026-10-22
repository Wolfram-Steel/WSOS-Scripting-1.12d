# Seguridad de WSOS-Scripting

Este documento describe controles técnicos del proyecto; no constituye una certificación ni una declaración de conformidad ISO/IEC 27001.

## Alcance y uso seguro

- Utiliza una versión de Python mantenida y un entorno virtual dedicado.
- Instala dependencias únicamente desde fuentes confiables y revisa los cambios de `config/requirements.txt`.
- No ejecutes el programa con privilegios de administrador si no es imprescindible.
- Trata las URL, páginas descargadas, documentos y configuraciones como entradas no confiables.
- No introduzcas credenciales, tokens ni datos personales en informes de errores.
- Conserva copias de seguridad antes de actualizar o modificar datos persistentes.

## Controles técnicos implementados

- Las descargas HTTP tienen límites de tamaño y plazo total.
- Se rechazan URL que no sean HTTP/HTTPS y URL con credenciales embebidas.
- El número de intentos de red está acotado.
- La escritura JSON utiliza archivo temporal, `fsync` y reemplazo atómico.
- La instalación de dependencias rechaza opciones de pip, URL y rutas locales en los requisitos.
- La suite de pruebas incluye comprobaciones de límites y validación de entradas.

## Límites conocidos

- La aplicación descarga contenido web y, por tanto, debe tratar respuestas remotas como hostiles. Las validaciones de esquema no equivalen a una defensa completa contra SSRF o DNS rebinding.
- La actualización automática para Windows requiere revisión y pruebas específicas en Windows; no se considera validada por las pruebas ejecutadas en otros sistemas.
- La versión de dependencias declarada con rangos no garantiza instalaciones reproducibles. Para despliegues controlados, genera y revisa un archivo de bloqueo con hashes mediante un proceso de cadena de suministro aprobado.
- No se ha realizado una auditoría independiente ni una prueba de penetración exhaustiva.

## Notificación de vulnerabilidades

Comunica los hallazgos al mantenedor de forma privada, incluyendo versión, impacto y pasos mínimos de reproducción. Evita publicar datos sensibles o pruebas que afecten a terceros.

## Evidencias recomendadas para un SGSI basado en ISO/IEC 27001

La organización responsable debe mantener, según su alcance y evaluación de riesgos: inventario de activos, metodología y registro de riesgos, declaración de aplicabilidad, gestión de cambios, revisión de código, análisis de dependencias, gestión de vulnerabilidades, control de accesos, copias de seguridad, respuesta a incidentes, continuidad y evidencias de formación. La aplicabilidad y eficacia de cada control deben ser evaluadas por la organización; este repositorio no demuestra por sí mismo dichos requisitos.
