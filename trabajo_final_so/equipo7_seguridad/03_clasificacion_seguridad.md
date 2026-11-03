# Modulo 3: Clasificacion Aplicada a la Seguridad (Tema 6.2)

## 3.1 Teoria: Clasificaciones de Seguridad en Sistemas

### El Libro Naranja (TCSEC) - Trusted Computer System Evaluation Criteria

Publicado por el Departamento de Defensa de EE.UU. en 1983. Clasifica los sistemas
segun su nivel de seguridad:

```
┌────────┬──────────────────────┬──────────────────────────────────────────┐
│ Nivel  │ Nombre               │ Descripcion                              │
├────────┼──────────────────────┼──────────────────────────────────────────┤
│ D      │ Proteccion Minima    │ No cumple ningun requisito de seguridad. │
│        │                      │ Ej: MS-DOS, Windows 3.1                  │
├────────┼──────────────────────┼──────────────────────────────────────────┤
│ C1     │ Proteccion           │ Identificacion de usuarios, permisos     │
│        │ Discrecional         │ basicos. Usuarios separados de datos.    │
│        │                      │ Ej: Unix antiguo, Windows NT basico      │
├────────┼──────────────────────┼──────────────────────────────────────────┤
│ C2     │ Proteccion de        │ Control de acceso mas fino. Auditoria    │
│        │ Acceso Controlado    │ de eventos. Aislamiento de recursos.     │
│        │                      │ Ej: Windows NT C2, algunos Unix          │
├────────┼──────────────────────┼──────────────────────────────────────────┤
│ B1     │ Proteccion de        │ Etiquetas de seguridad en objetos.       │
│        │ Seguridad Etiquetada │ Control de acceso obligatorio (MAC).     │
│        │                      │ Ej: SELinux, AppArmor en modo estricto   │
├────────┼──────────────────────┼──────────────────────────────────────────┤
│ B2     │ Proteccion           │ Modelo formal de politica de seguridad.  │
│        │ Estructurada         │ Canales encubiertos identificados.       │
│        │                      │ Principio de menor privilegio aplicado.  │
├────────┼──────────────────────┼──────────────────────────────────────────┤
│ B3     │ Dominios de          │ Monitor de referencia a prueba de        │
│        │ Seguridad            │ manipulacion. Recuperacion segura.       │
│        │                      │ Alertas en tiempo real.                  │
├────────┼──────────────────────┼──────────────────────────────────────────┤
│ A1     │ Diseno Verificado    │ Demostracion matematica de seguridad.    │
│        │                      │ Verificacion formal del diseno.          │
│        │                      │ Solo sistemas militares especializados.  │
└────────┴──────────────────────┴──────────────────────────────────────────┘
```

### Common Criteria (ISO/IEC 15408)

Reemplazo moderno del Libro Naranja. Estandar internacional usado actualmente:

```
Niveles de Aseguramiento (EAL - Evaluation Assurance Level):

  EAL1 - Probado funcionalmente
          -> El producto funciona como dice. Pruebas basicas.

  EAL2 - Probado estructuralmente
          -> Se revisa el diseno. Pruebas mas detalladas.

  EAL3 - Probado y verificado metodicamente
          -> Ambiente de desarrollo controlado.

  EAL4 - Disenado, probado y revisado metodicamente
          -> Nivel mas alto comercialmente viable.
          -> Windows, Linux con certificaciones llegan aqui.

  EAL5 - Disenado y probado semi-formalmente
          -> Analisis semi-formal del diseno.

  EAL6 - Diseno verificado y probado semi-formalmente
          -> Verificacion semi-formal. Ambiente muy controlado.

  EAL7 - Diseno verificado y probado formalmente
          -> Demostracion matematica. Muy pocos sistemas lo logran.

Ejemplo real:
  - Red Hat Enterprise Linux: certificado EAL4+
  - Windows 10: certificado EAL1
  - Tarjetas inteligentes bancarias: EAL4+ a EAL5+
```

## 3.2 Clasificacion por Tipo de Control de Acceso

```
┌─────────────────────────┬───────────────────────────────────────────┐
│ Tipo                    │ Descripcion                               │
├─────────────────────────┼───────────────────────────────────────────┤
│ DAC                     │ El PROPIETARIO del recurso decide quien   │
│ (Discretionary Access   │ puede acceder. El usuario tiene control.  │
│  Control)               │ Ej: chmod en Linux (tu decides permisos)  │
├─────────────────────────┼───────────────────────────────────────────┤
│ MAC                     │ El SISTEMA decide segun politicas         │
│ (Mandatory Access       │ centrales. El usuario NO puede cambiar    │
│  Control)               │ permisos. Ej: SELinux, AppArmor          │
├─────────────────────────┼───────────────────────────────────────────┤
│ RBAC                    │ Acceso basado en ROLES (administrador,    │
│ (Role-Based Access      │ editor, lector). Se asignan roles a       │
│  Control)               │ usuarios, no permisos individuales.       │
│                         │ Ej: sudo groups, Django permissions       │
├─────────────────────────┼───────────────────────────────────────────┤
│ ABAC                    │ Acceso basado en ATRIBUTOS: hora del dia, │
│ (Attribute-Based Access │ ubicacion, tipo de dispositivo, etc.      │
│  Control)               │ Ej: "Solo acceso desde la oficina en      │
│                         │ horario laboral"                          │
└─────────────────────────┴───────────────────────────────────────────┘
```

### Comparacion visual DAC vs MAC

```
DAC (Discretionary):
  Usuario Luis crea archivo "reporte.txt"
  Luis decide: "Maria puede leerlo, Pedro puede editarlo"
  Luis puede cambiar estos permisos cuando quiera
  -> FLEXIBLE pero depende del criterio del usuario

MAC (Mandatory):
  Admin del sistema define: "Archivos con etiqueta CONFIDENCIAL
  solo accesibles por usuarios con clearance CONFIDENCIAL+"
  Luis NO puede compartir aunque sea su archivo
  -> RIGIDO pero mas seguro en ambientes criticos
```

## 3.3 Clasificacion por Nivel de Seguridad de la Informacion

```
Nivel militar/gubernamental:

  TOP SECRET     -> Dano excepcionalmente grave a seguridad nacional
  SECRET         -> Dano serio a seguridad nacional
  CONFIDENTIAL   -> Dano a seguridad nacional
  UNCLASSIFIED   -> Informacion publica

Nivel empresarial:

  RESTRINGIDO    -> Solo personal especifico (nominas, contratos)
  CONFIDENCIAL   -> Solo departamento autorizado (planes estrategicos)
  INTERNO        -> Cualquier empleado (manuales, procedimientos)
  PUBLICO        -> Cualquiera (sitio web, marketing)
```

### Modelo Bell-LaPadula (Confidencialidad)

```
Regla: "No leer arriba, no escribir abajo"

  TOP SECRET ─────────── Nivel mas alto
       │
  SECRET ───────────────
       │
  CONFIDENTIAL ────────
       │
  UNCLASSIFIED ──────── Nivel mas bajo

  Un usuario con clearance SECRET:
    - PUEDE leer: CONFIDENTIAL, UNCLASSIFIED (abajo)
    - PUEDE escribir: SECRET, TOP SECRET (mismo nivel o arriba)
    - NO PUEDE leer: TOP SECRET (arriba)
    - NO PUEDE escribir: CONFIDENTIAL (abajo, evita filtrar info)

  Esto PREVIENE que informacion clasificada "baje" de nivel.
```

### Modelo Biba (Integridad)

```
Regla: "No leer abajo, no escribir arriba" (inverso de Bell-LaPadula)

  ALTA INTEGRIDAD ────── Datos muy confiables (base de datos oficial)
       │
  MEDIA INTEGRIDAD ───── Datos parcialmente verificados
       │
  BAJA INTEGRIDAD ────── Datos no verificados (input de usuario)

  Un proceso con nivel de integridad ALTO:
    - PUEDE leer: datos de alta integridad (mismo nivel o arriba)
    - NO PUEDE leer: datos de baja integridad (podria contaminarse)
    - NO PUEDE escribir: nada de integridad mayor a la suya

  Esto PREVIENE que datos no confiables contaminen datos confiables.
```

## 3.4 Practica: Explorando Clasificaciones en Linux

### Ejercicio 1: DAC en Linux (chmod, chown)

```bash
# Crear directorio de prueba
mkdir -p /tmp/clasificacion_seguridad
cd /tmp/clasificacion_seguridad

# Crear archivos con diferentes niveles de acceso
echo "Informacion publica" > publico.txt
echo "Solo para el equipo" > interno.txt
echo "Datos sensibles" > confidencial.txt
echo "Llaves de acceso root" > restringido.txt

# Aplicar permisos DAC segun clasificacion
chmod 644 publico.txt        # rw-r--r-- (todos leen)
chmod 640 interno.txt        # rw-r----- (owner y grupo leen)
chmod 600 confidencial.txt   # rw------- (solo owner)
chmod 400 restringido.txt    # r-------- (solo owner, solo lectura)

# Verificar
ls -la
# publico.txt:      -rw-r--r--  (mundo puede leer)
# interno.txt:      -rw-r-----  (grupo puede leer)
# confidencial.txt: -rw-------  (solo owner)
# restringido.txt:  -r--------  (solo owner, solo lectura)
```

### Ejercicio 2: Simulando RBAC con grupos

```bash
# Crear grupos que representen roles
sudo groupadd rol_admin
sudo groupadd rol_editor
sudo groupadd rol_lector

# Crear usuarios y asignar roles
sudo useradd -m -G rol_admin admin_user
sudo useradd -m -G rol_editor editor_user
sudo useradd -m -G rol_lector lector_user

# Crear recurso compartido
sudo mkdir /tmp/proyecto
echo "Documento importante" | sudo tee /tmp/proyecto/documento.txt

# Aplicar permisos por grupo (RBAC)
sudo chgrp rol_editor /tmp/proyecto/documento.txt
sudo chmod 664 /tmp/proyecto/documento.txt  # rw-rw-r--

# El editor puede escribir (pertenece al grupo)
sudo -u editor_user bash -c 'echo "editado" >> /tmp/proyecto/documento.txt' && echo "Editor: OK"

# El lector solo puede leer
sudo -u lector_user cat /tmp/proyecto/documento.txt && echo "Lector lectura: OK"
sudo -u lector_user bash -c 'echo "intento" >> /tmp/proyecto/documento.txt' 2>&1 || echo "Lector escritura: DENEGADO"
```

### Ejercicio 3: MAC con AppArmor

```bash
# Verificar si AppArmor esta activo (MAC en Ubuntu)
sudo aa-status

# Ver perfiles cargados
sudo aa-status | head -20

# Ejemplo: el perfil de Firefox restringe a que archivos puede acceder
# Aunque el usuario tenga permiso (DAC), AppArmor (MAC) puede bloquearlo

# Ver un perfil de AppArmor
ls /etc/apparmor.d/
# Ejemplo de perfil:
cat /etc/apparmor.d/usr.sbin.tcpdump 2>/dev/null || echo "Perfil no disponible"
```

### Ejercicio 4: Script de clasificacion de archivos

```python
#!/usr/bin/env python3
"""
Simulacion de un sistema de clasificacion de seguridad.
Demuestra como diferentes niveles de clearance acceden a recursos.
"""
import os
import stat
from dataclasses import dataclass
from enum import IntEnum

class NivelSeguridad(IntEnum):
    """Niveles de seguridad (modelo Bell-LaPadula simplificado)."""
    PUBLICO = 0
    INTERNO = 1
    CONFIDENCIAL = 2
    RESTRINGIDO = 3

@dataclass
class Recurso:
    nombre: str
    nivel: NivelSeguridad
    contenido: str

@dataclass
class Usuario:
    nombre: str
    clearance: NivelSeguridad

def puede_leer(usuario: Usuario, recurso: Recurso) -> bool:
    """Bell-LaPadula: puede leer si clearance >= nivel del recurso."""
    return usuario.clearance >= recurso.nivel

def puede_escribir(usuario: Usuario, recurso: Recurso) -> bool:
    """Bell-LaPadula: puede escribir si clearance <= nivel del recurso."""
    return usuario.clearance <= recurso.nivel

def main():
    # Definir recursos con diferentes clasificaciones
    recursos = [
        Recurso("Sitio Web", NivelSeguridad.PUBLICO, "Bienvenido a la empresa"),
        Recurso("Manual Empleados", NivelSeguridad.INTERNO, "Politicas internas..."),
        Recurso("Plan Estrategico", NivelSeguridad.CONFIDENCIAL, "Q3: expandir a..."),
        Recurso("Claves Root", NivelSeguridad.RESTRINGIDO, "root:Xk9$mP2!..."),
    ]

    # Definir usuarios con diferentes clearances
    usuarios = [
        Usuario("Visitante", NivelSeguridad.PUBLICO),
        Usuario("Empleado", NivelSeguridad.INTERNO),
        Usuario("Gerente", NivelSeguridad.CONFIDENCIAL),
        Usuario("SysAdmin", NivelSeguridad.RESTRINGIDO),
    ]

    # Modelo Bell-LaPadula: verificar acceso
    print("=" * 70)
    print("SIMULACION BELL-LAPADULA: CONTROL DE ACCESO POR NIVEL")
    print("=" * 70)

    print("\n--- LECTURA (No leer arriba) ---")
    print(f"{'Usuario':<15} {'Recurso':<20} {'Nivel Recurso':<15} {'Acceso'}")
    print("-" * 65)

    for usuario in usuarios:
        for recurso in recursos:
            acceso = "PERMITIDO" if puede_leer(usuario, recurso) else "DENEGADO"
            marca = "+" if puede_leer(usuario, recurso) else "X"
            print(f"  [{marca}] {usuario.nombre:<13} {recurso.nombre:<20} "
                  f"{recurso.nivel.name:<15} {acceso}")
        print()

    print("\n--- ESCRITURA (No escribir abajo) ---")
    print(f"{'Usuario':<15} {'Recurso':<20} {'Nivel Recurso':<15} {'Acceso'}")
    print("-" * 65)

    for usuario in usuarios:
        for recurso in recursos:
            acceso = "PERMITIDO" if puede_escribir(usuario, recurso) else "DENEGADO"
            marca = "+" if puede_escribir(usuario, recurso) else "X"
            print(f"  [{marca}] {usuario.nombre:<13} {recurso.nombre:<20} "
                  f"{recurso.nivel.name:<15} {acceso}")
        print()

    # Demostrar el punto clave
    print("=" * 70)
    print("PUNTO CLAVE:")
    print("  - El SysAdmin puede LEER todo pero solo ESCRIBIR en RESTRINGIDO")
    print("  - El Visitante puede ESCRIBIR en todos los niveles pero solo LEER PUBLICO")
    print("  - Esto evita que informacion clasificada 'baje' de nivel")
    print("=" * 70)

if __name__ == "__main__":
    main()
```

Guarda como `clasificacion_seguridad.py` y ejecuta:

```bash
python3 clasificacion_seguridad.py
```

### Limpieza

```bash
# Limpiar usuarios y grupos de prueba
sudo userdel -r admin_user 2>/dev/null
sudo userdel -r editor_user 2>/dev/null
sudo userdel -r lector_user 2>/dev/null
sudo groupdel rol_admin 2>/dev/null
sudo groupdel rol_editor 2>/dev/null
sudo groupdel rol_lector 2>/dev/null
rm -rf /tmp/clasificacion_seguridad
```

## 3.5 Resumen del Modulo

```
TCSEC (Libro Naranja): D -> C1 -> C2 -> B1 -> B2 -> B3 -> A1
Common Criteria: EAL1 a EAL7 (estandar actual)

Tipos de control de acceso:
  DAC - El propietario decide (chmod en Linux)
  MAC - El sistema decide (SELinux, AppArmor)
  RBAC - Basado en roles (grupos, sudo)
  ABAC - Basado en atributos (hora, ubicacion)

Modelos formales:
  Bell-LaPadula - Confidencialidad (no leer arriba, no escribir abajo)
  Biba - Integridad (no leer abajo, no escribir arriba)
```

## 3.6 Preguntas de Repaso

1. Cual es la diferencia entre DAC y MAC? Da un ejemplo de cada uno en Linux.
2. En que nivel TCSEC clasificarias un Ubuntu con AppArmor habilitado?
3. Segun Bell-LaPadula, puede un usuario CONFIDENCIAL escribir en un recurso PUBLICO? Por que?
4. Que ventaja tiene RBAC sobre DAC en una empresa grande?
5. Que nivel EAL tiene RHEL? Por que importa en ambientes empresariales?
