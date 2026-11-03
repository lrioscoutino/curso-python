# Tutorial: Proteccion y Seguridad en Sistemas Operativos

Tutorial teorico-practico de nivel medio sobre proteccion y seguridad en SO.
Incluye teoria, diagramas, ejemplos en Python y practicas en Linux.

## Contenido

| Modulo | Tema | Descripcion |
|--------|------|-------------|
| 01 | [Introduccion a la Seguridad](01_introduccion_seguridad.md) | Triada CIA, superficie de ataque, auditoria inicial |
| 02 | [Concepto y Objetivos (6.1)](02_conceptos_proteccion_seguridad.md) | Proteccion vs seguridad, dominios de proteccion, objetivos |
| 03 | [Clasificacion de Seguridad (6.2)](03_clasificacion_seguridad.md) | TCSEC, Common Criteria, DAC/MAC/RBAC, Bell-LaPadula, Biba |
| 04 | [Funciones del Sistema de Proteccion (6.3)](04_funciones_sistema_proteccion.md) | Autenticacion, autorizacion, auditoria, aislamiento, PAM |
| 05 | [Matrices de Acceso (6.4)](05_matrices_acceso.md) | ACL, Capability Lists, tabla de autorizacion, Linux capabilities |
| 06 | [Proteccion Basada en el Lenguaje (6.5)](06_proteccion_basada_lenguaje.md) | Type safety, memory safety, sandboxing, Rust ownership |
| 07 | [Validacion y Amenazas (6.6)](07_validacion_amenazas.md) | Input validation, SQL injection, XSS, STRIDE, deteccion |
| 08 | [Cifrado (6.7)](08_cifrado.md) | Simetrico/asimetrico, hash, firma digital, cifrado hibrido |

## Requisitos

- Ubuntu 22.04 LTS o superior (recomendado en VM para practicas)
- Acceso a terminal con privilegios sudo
- Python 3.10+
- `pip install cryptography` (para modulo 08)
- Conocimientos basicos de Linux (navegacion, edicion de archivos)

## Como usar este tutorial

1. Sigue los modulos en orden secuencial
2. Lee la seccion teorica antes de la practica
3. Ejecuta los scripts Python para ver los conceptos en accion
4. Responde las preguntas de repaso al final de cada modulo
