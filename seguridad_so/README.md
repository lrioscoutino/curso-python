# Tutorial: Seguridad en Sistemas Operativos Ubuntu

Tutorial teorico-practico de seguridad en Ubuntu para administradores de sistemas.

## Contenido

| Modulo | Tema | Descripcion |
|--------|------|-------------|
| 01 | [Introduccion a la Seguridad](01_introduccion_seguridad.md) | Triada CIA, superficie de ataque, auditoria inicial |
| 02 | [Gestion de Usuarios y Permisos](02_gestion_usuarios_permisos.md) | Usuarios, passwords, permisos rwx, SUID/SGID, sudo |
| 03 | [Firewall - UFW e iptables](03_firewall_iptables_ufw.md) | Netfilter, reglas UFW, iptables avanzado |
| 04 | [SSH Seguro](04_ssh_seguro.md) | Claves SSH, hardening sshd, Fail2Ban |
| 05 | [Actualizaciones y Hardening](05_actualizaciones_hardening.md) | Updates automaticos, sysctl, AIDE, CIS Benchmark |
| 06 | [Logs, Auditoria y Monitoreo](06_logs_auditoria.md) | journalctl, auditd, analisis de logs |
| 07 | [Cifrado y Proteccion de Datos](07_cifrado_datos.md) | GPG, LUKS, OpenSSL, verificacion de integridad |
| 08 | [Seguridad de Red](08_seguridad_red.md) | nmap, tcpdump, IDS, DNS seguro, WireGuard |
| 09 | [AppArmor y Seguridad de Aplicaciones](09_apparmor_seguridad_aplicaciones.md) | MAC, perfiles AppArmor, Firejail, Docker seguro |
| 10 | [Proyecto Final](10_proyecto_final.md) | Hardening completo de un servidor con verificacion |

## Requisitos

- Ubuntu 22.04 LTS o superior (recomendado en VM para practicas)
- Acceso a terminal con privilegios sudo
- Conocimientos basicos de Linux (navegacion, edicion de archivos)

## Como usar este tutorial

1. Sigue los modulos en orden secuencial
2. Lee la seccion teorica antes de la practica
3. Ejecuta los comandos en una VM de pruebas (nunca en produccion sin entender lo que hacen)
4. Completa los ejercicios practicos de cada modulo
5. Termina con el proyecto final del Modulo 10
