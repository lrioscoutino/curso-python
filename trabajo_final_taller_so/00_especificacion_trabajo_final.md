# Trabajo final — Video por equipos: reproducción de una práctica real del taller

**Materia:** Taller de Sistemas Operativos (SCA-1026)

## Idea central

A diferencia de una materia teórica, en un *taller* lo que se evalúa es la capacidad de **operar** sistemas reales, no de explicarlos. Por eso el trabajo final no parte de un tema libre ni de una exposición: cada equipo **elige una de las prácticas que ya se hicieron en el curso** y produce un video donde la **reproduce de principio a fin, en vivo, sobre un entorno propio** (no copiando pantallas del documento del curso).

Si el equipo no puede ejecutarla de verdad en su propia máquina/VM, no hay toma que grabar — eso es lo que hace imposible aprobar sin haber tocado el sistema real.

---

## 1. Prácticas disponibles para elegir

| # | Práctica | Unidad | De qué se trata |
|---|---|---|---|
| 1 | [Fundamentos de la terminal de Linux](https://github.com/lrioscoutino/taller_sistemas_operativos_u1/blob/main/04_practica_terminal_linux.md) | 1 | Navegación del sistema de archivos, manejo de procesos y texto desde la línea de comandos |
| 2 | [Instalación de Docker y administración básica de contenedores](https://github.com/lrioscoutino/taller_sistemas_operativos_u1/blob/main/05_practica_docker.md) | 1 | Instalar Docker, correr/administrar contenedores como si fueran servidores ligeros |
| 3 | [Automatización de tareas con Cron](https://github.com/lrioscoutino/taller_sistemas_operativos_u1/blob/main/07_practica_cron.md) | 1 | Programar tareas repetitivas (respaldos, limpieza, reportes) sin intervención manual |
| 4 | [Usuarios, grupos y permisos en Linux](https://github.com/lrioscoutino/taller_sistemas_operativos_u1/blob/main/08_practica_usuarios_grupos_permisos.md) | 1 | Multiusuario real: dueños, grupos, permisos, y por qué un usuario no puede tocar los archivos de otro |
| 5 | [Administrar un servidor Linux ya instalado](https://github.com/lrioscoutino/taller_sistemas_operativos_u3/blob/main/02_practica_administracion_servidor_linux.md) | 3 | Niveles de ejecución, servicios, usuarios/grupos aislados, y recuperación de una falla real |
| 6 | [Interoperabilidad con Samba](https://github.com/lrioscoutino/taller_sistemas_operativos_u4/blob/main/02_practica_samba.md) | 4 | Levantar un servidor Samba real, compartir una carpeta y conectarse desde un cliente (como `\\servidor\carpeta` en Windows) |
| 7 | [Servicios de nube local con Floci](https://github.com/lrioscoutino/taller_sistemas_operativos_u4/blob/main/05_practica_cloud_local_floci.md) | 4 (extra) | Emular servicios de nube (S3, DynamoDB, SQS) en la propia máquina, sin cuenta ni tarjeta |

**Regla de asignación:** no puede haber dos equipos con la misma práctica si hay 7 equipos o menos — cada práctica elegida se "apaga" para los demás hasta que todas tengan dueño; solo si hay más de 7 equipos se permite repetir, y en ese caso los dos equipos deben usar un escenario/datos distintos entre sí (no pueden grabar lo mismo). El profesor confirma la asignación final para evitar choques de último momento.

**Por qué elegir y no tema libre:** limitar a estas 7 opciones garantiza que todo lo mostrado ya fue validado como ejecutable de verdad en este curso (cada documento indica qué se verificó y en qué entorno) — un tema completamente libre podría llevar a un equipo a elegir algo que ni ellos ni el profesor puedan verificar a tiempo.

---

## 2. Qué debe demostrar el video (según la práctica elegida)

No basta con seguir los pasos del documento al pie de la letra — el equipo debe demostrar que **entendió** lo que hizo, no solo que lo copió:

- Ejecutar la práctica completa (o su núcleo técnico, si es muy larga) en un entorno propio: su propia VM, WSL2, o contenedor — nunca una captura de pantalla del documento del curso.
- En al menos **un punto del video, cambiar deliberadamente algo del escenario original** (otro usuario, otro puerto, otro nombre de carpeta compartida, otro horario de cron, otra imagen de contenedor, otro bucket) y mostrar que el resultado sigue siendo correcto — esto es lo que separa "lo reproduje de memoria" de "lo entendí".
- Si algo falla (un permiso, un puerto ocupado, un servicio que no arrancó), **mostrar el error real y cómo lo diagnosticaron y corrigieron** — un error resuelto en pantalla vale más que una toma perfecta sin tropiezos, porque es evidencia de que de verdad estaban operando el sistema.

## 3. Reglas del video

- **Duración:** 6 a 10 minutos.
- **Evidencia en pantalla obligatoria:** al menos 70% del tiempo debe ser grabación real de terminal/sistema (screen recording) — nada de diapositivas narradas como sustituto de la demostración. Diapositivas solo para introducir el tema en el primer minuto.
- **Participación individual verificable:** cada integrante debe aparecer ejecutando al menos una parte distinta de la demostración desde su propia terminal/sesión (se nota el usuario, el hostname, o la voz explicando lo que hace).
- **Cierre individual de 20-30 segundos por persona:** qué parte entendieron mejor y qué fue lo que más les costó — en sus palabras, no un guion leído igual por todos.

## 4. Entregables

1. El video (enlace privado o archivo en la plataforma del curso).
2. Un documento corto con: en qué entorno lo corrieron (SO, versión, VM/contenedor), los comandos exactos ejecutados y las salidas reales obtenidas — suficiente para que el profesor reproduzca el mismo resultado.
3. Una tabla de reparto de tareas: quién ejecutó qué parte y quién editó el video.

## 5. Rúbrica (100 puntos)

| Criterio | Puntos | Qué se evalúa |
|---|---|---|
| **Correctud técnica** | 35 | Lo mostrado corre de verdad, sin cortes que oculten fallas, y corresponde al núcleo técnico de la práctica elegida. El documento de reproducción debe permitir obtener el mismo resultado. |
| **Variación propia sobre el escenario original** | 20 | El cambio deliberado (sección 2) es real, visible en pantalla, y el equipo explica por qué sigue funcionando — no es solo cambiar un nombre cosmético sin entender qué dependía de él. |
| **Evidencia práctica vs. narración** | 15 | Proporción real de pantalla de sistema vs. diapositivas o cara hablando sin demostrar nada. |
| **Participación individual** | 15 | Cada integrante ejecuta algo propio y distinto; el cierre individual demuestra comprensión real. |
| **Manejo de errores reales** | 10 | Si algo falló durante la grabación, se diagnosticó y resolvió en pantalla en vez de cortarse y reiniciar sin explicación. Si no hubo ningún error real, este criterio se evalúa sobre qué tan bien explican los posibles puntos de falla del sistema que mostraron. |
| **Documento de reproducción** | 5 | Comandos y salidas completos y suficientes para reproducir el resultado. |

**Regla de corte:** si el documento de reproducción no permite reproducir al menos el 80% de lo mostrado en el video, "Correctud técnica" no puede calificarse arriba de 20/35, sin importar qué tan bien se vea el video — no hay forma de verificar que fue real.

## 6. Calendario sugerido

| Semana | Actividad |
|---|---|
| 1 | Equipos definidos, elección de práctica confirmada por el profesor (sin choques) |
| 2-3 | Montaje del entorno propio y primera corrida completa de la práctica (sin grabar aún) |
| 4 | Definición de la variación propia a demostrar (sección 2) y ensayo de la grabación |
| 5 | Grabación, edición y entrega del video + documento de reproducción |
| 6 | Defensa breve en vivo (ver sección 7) |

## 7. Defensa breve en vivo (obligatoria)

Después de entregar el video, cada equipo pasa 5 minutos frente al profesor (puede ser en el mismo entorno grabado): se le hace **una pregunta técnica al azar por integrante** sobre la práctica elegida (ej. "¿qué pasa si quitas este permiso?", "¿por qué este puerto y no otro?"). Esto evita que el video se apruebe sin que cada integrante pueda sostener lo que se ve en pantalla.
