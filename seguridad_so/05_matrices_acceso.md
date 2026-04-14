# Modulo 5: Implantacion de Matrices de Acceso (Tema 6.4)

## 5.1 Teoria: La Matriz de Acceso

La matriz de acceso es el modelo teorico fundamental del control de acceso.
Define que operaciones puede realizar cada sujeto sobre cada objeto.

```
Estructura:
  - Filas:    Sujetos (usuarios, procesos)
  - Columnas: Objetos (archivos, dispositivos, puertos)
  - Celdas:   Conjunto de operaciones permitidas (derechos de acceso)

Ejemplo:

                  archivo1.txt   archivo2.txt   impresora   /dev/sda
  ┌──────────────┬──────────────┬──────────────┬───────────┬──────────┐
  │              │ archivo1.txt │ archivo2.txt │ impresora │ /dev/sda │
  ├──────────────┼──────────────┼──────────────┼───────────┼──────────┤
  │ root         │ rwx          │ rwx          │ control   │ rwx      │
  ├──────────────┼──────────────┼──────────────┼───────────┼──────────┤
  │ luis         │ rw           │ r            │ imprimir  │          │
  ├──────────────┼──────────────┼──────────────┼───────────┼──────────┤
  │ maria        │ r            │ rw           │ imprimir  │          │
  ├──────────────┼──────────────┼──────────────┼───────────┼──────────┤
  │ proceso_web  │ r            │              │           │          │
  └──────────────┴──────────────┴──────────────┴───────────┴──────────┘

  Lectura de la tabla:
  - luis puede leer y escribir archivo1, solo leer archivo2, usar impresora
  - maria puede solo leer archivo1, leer y escribir archivo2
  - proceso_web solo puede leer archivo1
  - luis NO tiene acceso al disco /dev/sda (celda vacia)
```

## 5.2 Problema: La Matriz es Enorme

```
En un sistema real:
  - 1000 usuarios x 100,000 archivos = 100,000,000 celdas
  - La mayoria de celdas estan VACIAS (sin acceso)
  - Almacenar toda la matriz es ineficiente

Solucion: NO almacenar la matriz completa.
Usar representaciones compactas que solo guardan los permisos que existen.
```

## 5.3 Implementacion 1: Listas de Control de Acceso (ACL)

Almacenar la matriz POR COLUMNAS (por objeto/recurso):

```
Cada objeto tiene una lista de quien puede acceder y como:

  archivo1.txt -> [(root, rwx), (luis, rw), (maria, r), (proceso_web, r)]
  archivo2.txt -> [(root, rwx), (luis, r), (maria, rw)]
  impresora    -> [(root, control), (luis, imprimir), (maria, imprimir)]
  /dev/sda     -> [(root, rwx)]

Ventajas:
  + Facil saber QUIEN puede acceder a un recurso
  + Facil revocar acceso a un recurso (borrar de la lista)
  + Se almacena junto al recurso

Desventajas:
  - Dificil saber TODOS los permisos de un usuario
  - Revisar accesos de un usuario requiere recorrer todos los objetos
```

### ACL en Linux

```
Linux usa una ACL simplificada de 3 entradas por archivo:
  owner (u), group (g), others (o)

  -rw-r--r-- 1 luis devs archivo.txt

  Esto equivale a la ACL:
    [(luis, rw-), (devs, r--), (*, r--)]

Con ACLs extendidas (setfacl/getfacl):
  Se puede agregar entradas para usuarios/grupos especificos:
    [(luis, rw-), (maria, r--), (devs, r--), (*, ---)]
```

## 5.4 Implementacion 2: Listas de Capacidades (Capability Lists)

Almacenar la matriz POR FILAS (por sujeto/usuario):

```
Cada sujeto tiene una lista de lo que puede hacer:

  root        -> [(archivo1, rwx), (archivo2, rwx), (impresora, control), (/dev/sda, rwx)]
  luis        -> [(archivo1, rw), (archivo2, r), (impresora, imprimir)]
  maria       -> [(archivo1, r), (archivo2, rw), (impresora, imprimir)]
  proceso_web -> [(archivo1, r)]

Ventajas:
  + Facil saber TODO lo que un usuario puede hacer
  + Eficiente para verificar permisos rapidamente
  + Natural para sistemas distribuidos

Desventajas:
  - Dificil saber QUIEN tiene acceso a un recurso especifico
  - Revocar acceso requiere recorrer todas las listas de capacidad
  - Las capacidades deben ser infalsificables
```

### Capabilities en Linux

```
Linux moderno tiene "capabilities" del kernel: permisos granulares
que reemplazan el modelo "todo o nada" de root.

En lugar de: "el proceso es root y puede hacer TODO"
Se usa:      "el proceso tiene SOLO estas capacidades especificas"

Ejemplos de capabilities:
  CAP_NET_BIND_SERVICE  -> Bindear puertos < 1024
  CAP_SYS_ADMIN         -> Operaciones de administracion
  CAP_NET_RAW           -> Usar sockets raw (ping)
  CAP_CHOWN             -> Cambiar owner de archivos
  CAP_DAC_OVERRIDE      -> Ignorar permisos DAC

Ejemplo practico:
  Nginx necesita bindear puerto 80 (< 1024, requiere root)
  En vez de ejecutar nginx como root (peligroso):
    setcap cap_net_bind_service=+ep /usr/sbin/nginx
  Ahora nginx puede usar puerto 80 SIN ser root.
```

## 5.5 Implementacion 3: Tabla de Autorizacion (Cerradura-Llave)

```
Se almacena como una tabla de triplas:
  (sujeto, objeto, derechos)

  (root,        archivo1, rwx)
  (root,        archivo2, rwx)
  (luis,        archivo1, rw)
  (luis,        archivo2, r)
  (maria,       archivo1, r)
  (maria,       archivo2, rw)
  (proceso_web, archivo1, r)

Ventajas:
  + Eficiente en espacio (solo almacena permisos que existen)
  + Facil de buscar por cualquier combinacion
  + Natural para bases de datos

Desventajas:
  - Requiere busqueda en cada acceso
  - Sin optimizacion puede ser lenta
```

## 5.6 Comparacion de Implementaciones

```
┌────────────────┬──────────────┬──────────────┬──────────────────┐
│ Criterio       │ ACL          │ Capabilities │ Tabla Autoriz.   │
├────────────────┼──────────────┼──────────────┼──────────────────┤
│ Organizada por │ Objeto       │ Sujeto       │ Triplas          │
├────────────────┼──────────────┼──────────────┼──────────────────┤
│ "Quien accede  │ FACIL        │ DIFICIL      │ FACIL            │
│  a recurso X?" │              │              │                  │
├────────────────┼──────────────┼──────────────┼──────────────────┤
│ "Que puede     │ DIFICIL      │ FACIL        │ FACIL            │
│  hacer user Y?"│              │              │                  │
├────────────────┼──────────────┼──────────────┼──────────────────┤
│ Revocar acceso │ FACIL        │ DIFICIL      │ FACIL            │
│ a un recurso   │              │              │                  │
├────────────────┼──────────────┼──────────────┼──────────────────┤
│ Ejemplo real   │ chmod/setfacl│ Linux caps   │ BD permisos      │
│                │ en Linux     │ (setcap)     │ (Django, etc.)   │
└────────────────┴──────────────┴──────────────┴──────────────────┘
```

## 5.7 Practica: Implementando Matrices de Acceso

### Ejercicio 1: Implementacion en Python

```python
#!/usr/bin/env python3
"""
Implementacion de las tres representaciones de la matriz de acceso:
1. ACL (por objeto)
2. Capability List (por sujeto)
3. Tabla de autorizacion (triplas)
"""
from collections import defaultdict
from dataclasses import dataclass, field


class MatrizAcceso:
    """Matriz de acceso base (representacion completa)."""

    def __init__(self):
        # matriz[sujeto][objeto] = set de permisos
        self.matriz: dict[str, dict[str, set[str]]] = defaultdict(
            lambda: defaultdict(set)
        )

    def otorgar(self, sujeto: str, objeto: str, *permisos: str):
        """Otorga permisos a un sujeto sobre un objeto."""
        self.matriz[sujeto][objeto].update(permisos)

    def revocar(self, sujeto: str, objeto: str, *permisos: str):
        """Revoca permisos de un sujeto sobre un objeto."""
        self.matriz[sujeto][objeto] -= set(permisos)

    def verificar(self, sujeto: str, objeto: str, permiso: str) -> bool:
        """Verifica si un sujeto tiene un permiso sobre un objeto."""
        return permiso in self.matriz[sujeto][objeto]

    def mostrar(self):
        """Muestra la matriz completa."""
        if not self.matriz:
            print("  (matriz vacia)")
            return

        # Recopilar todos los objetos
        objetos = set()
        for permisos_sujeto in self.matriz.values():
            objetos.update(permisos_sujeto.keys())
        objetos = sorted(objetos)

        # Imprimir encabezado
        ancho = max(len(o) for o in objetos) + 2
        print(f"  {'Sujeto':<15}", end="")
        for obj in objetos:
            print(f"{obj:<{ancho}}", end="")
        print()
        print("  " + "-" * (15 + ancho * len(objetos)))

        # Imprimir filas
        for sujeto in sorted(self.matriz.keys()):
            print(f"  {sujeto:<15}", end="")
            for obj in objetos:
                perms = self.matriz[sujeto].get(obj, set())
                perm_str = ",".join(sorted(perms)) if perms else "---"
                print(f"{perm_str:<{ancho}}", end="")
            print()


class ACL:
    """Representacion por ACL (organizada por objeto)."""

    def __init__(self):
        # acl[objeto] = [(sujeto, permisos), ...]
        self.acl: dict[str, list[tuple[str, set[str]]]] = defaultdict(list)

    @classmethod
    def desde_matriz(cls, matriz: MatrizAcceso) -> "ACL":
        """Construye ACL desde una matriz de acceso."""
        acl = cls()
        for sujeto, objetos in matriz.matriz.items():
            for objeto, permisos in objetos.items():
                if permisos:
                    acl.acl[objeto].append((sujeto, permisos.copy()))
        return acl

    def verificar(self, sujeto: str, objeto: str, permiso: str) -> bool:
        """Verifica acceso buscando en la ACL del objeto."""
        for s, perms in self.acl.get(objeto, []):
            if s == sujeto and permiso in perms:
                return True
        return False

    def quien_accede(self, objeto: str) -> list[tuple[str, set[str]]]:
        """Retorna todos los sujetos que acceden a un objeto."""
        return self.acl.get(objeto, [])

    def mostrar(self):
        print("  Representacion ACL (por objeto):")
        for objeto in sorted(self.acl.keys()):
            entradas = self.acl[objeto]
            entradas_str = ", ".join(
                f"({s}: {','.join(sorted(p))})" for s, p in entradas
            )
            print(f"    {objeto} -> [{entradas_str}]")


class CapabilityList:
    """Representacion por lista de capacidades (organizada por sujeto)."""

    def __init__(self):
        # caps[sujeto] = [(objeto, permisos), ...]
        self.caps: dict[str, list[tuple[str, set[str]]]] = defaultdict(list)

    @classmethod
    def desde_matriz(cls, matriz: MatrizAcceso) -> "CapabilityList":
        """Construye Capability List desde una matriz de acceso."""
        caplist = cls()
        for sujeto, objetos in matriz.matriz.items():
            for objeto, permisos in objetos.items():
                if permisos:
                    caplist.caps[sujeto].append((objeto, permisos.copy()))
        return caplist

    def verificar(self, sujeto: str, objeto: str, permiso: str) -> bool:
        """Verifica acceso buscando en las capacidades del sujeto."""
        for o, perms in self.caps.get(sujeto, []):
            if o == objeto and permiso in perms:
                return True
        return False

    def que_puede_hacer(self, sujeto: str) -> list[tuple[str, set[str]]]:
        """Retorna todo lo que un sujeto puede hacer."""
        return self.caps.get(sujeto, [])

    def mostrar(self):
        print("  Representacion Capability List (por sujeto):")
        for sujeto in sorted(self.caps.keys()):
            entradas = self.caps[sujeto]
            entradas_str = ", ".join(
                f"({o}: {','.join(sorted(p))})" for o, p in entradas
            )
            print(f"    {sujeto} -> [{entradas_str}]")


class TablaAutorizacion:
    """Representacion como tabla de triplas (sujeto, objeto, derechos)."""

    def __init__(self):
        self.triplas: list[tuple[str, str, set[str]]] = []

    @classmethod
    def desde_matriz(cls, matriz: MatrizAcceso) -> "TablaAutorizacion":
        """Construye tabla desde una matriz de acceso."""
        tabla = cls()
        for sujeto, objetos in matriz.matriz.items():
            for objeto, permisos in objetos.items():
                if permisos:
                    tabla.triplas.append((sujeto, objeto, permisos.copy()))
        return tabla

    def verificar(self, sujeto: str, objeto: str, permiso: str) -> bool:
        """Verifica acceso buscando en las triplas."""
        return any(
            s == sujeto and o == objeto and permiso in p
            for s, o, p in self.triplas
        )

    def mostrar(self):
        print("  Representacion Tabla de Autorizacion (triplas):")
        for sujeto, objeto, permisos in sorted(self.triplas):
            print(f"    ({sujeto}, {objeto}, {{{','.join(sorted(permisos))}}})")


def main():
    print("=" * 65)
    print("  IMPLEMENTACION DE MATRIZ DE ACCESO")
    print("=" * 65)

    # Crear la matriz de acceso
    m = MatrizAcceso()
    m.otorgar("root", "passwd.txt", "r", "w", "x")
    m.otorgar("root", "config.ini", "r", "w")
    m.otorgar("root", "impresora", "control")
    m.otorgar("luis", "passwd.txt", "r")
    m.otorgar("luis", "config.ini", "r", "w")
    m.otorgar("luis", "impresora", "imprimir")
    m.otorgar("maria", "passwd.txt", "r")
    m.otorgar("maria", "config.ini", "r")
    m.otorgar("web_server", "passwd.txt", "r")

    print("\n--- Matriz Completa ---")
    m.mostrar()

    # Convertir a las 3 representaciones
    acl = ACL.desde_matriz(m)
    caps = CapabilityList.desde_matriz(m)
    tabla = TablaAutorizacion.desde_matriz(m)

    print(f"\n--- Representacion 1: ACL ---")
    acl.mostrar()

    print(f"\n--- Representacion 2: Capability List ---")
    caps.mostrar()

    print(f"\n--- Representacion 3: Tabla de Autorizacion ---")
    tabla.mostrar()

    # Verificacion de acceso con las 3 representaciones
    print(f"\n{'=' * 65}")
    print("  VERIFICACION DE ACCESO")
    print(f"{'=' * 65}")

    consultas = [
        ("luis", "passwd.txt", "r"),
        ("luis", "passwd.txt", "w"),
        ("maria", "config.ini", "w"),
        ("web_server", "impresora", "imprimir"),
        ("root", "config.ini", "w"),
    ]

    for sujeto, objeto, permiso in consultas:
        r1 = acl.verificar(sujeto, objeto, permiso)
        r2 = caps.verificar(sujeto, objeto, permiso)
        r3 = tabla.verificar(sujeto, objeto, permiso)
        estado = "PERMITIDO" if r1 else "DENEGADO"
        consistente = "OK" if r1 == r2 == r3 else "ERROR"
        print(f"  {sujeto} -> {objeto} [{permiso}]: {estado} ({consistente})")

    # Consultas especificas por representacion
    print(f"\n--- Consulta ACL: Quien accede a passwd.txt? ---")
    for sujeto, perms in acl.quien_accede("passwd.txt"):
        print(f"    {sujeto}: {','.join(sorted(perms))}")

    print(f"\n--- Consulta Capability: Que puede hacer luis? ---")
    for objeto, perms in caps.que_puede_hacer("luis"):
        print(f"    {objeto}: {','.join(sorted(perms))}")

if __name__ == "__main__":
    main()
```

Guarda como `matrices_acceso.py` y ejecuta:

```bash
python3 matrices_acceso.py
```

### Ejercicio 2: ACLs reales en Linux

```bash
# Crear estructura que simule la matriz del ejemplo
mkdir -p /tmp/matriz_demo
cd /tmp/matriz_demo

# Crear archivos
echo "usuario:password_hash" > passwd.txt
echo "db_host=localhost" > config.ini

# Simular la matriz con permisos Unix + ACLs
chmod 644 passwd.txt   # root rw, otros r
chmod 640 config.ini   # root rw, grupo r

# Agregar ACLs especificas
# luis puede leer+escribir config.ini
setfacl -m u:$(whoami):rw config.ini

# Ver la ACL resultante
echo "--- ACL de config.ini ---"
getfacl config.ini

echo "--- ACL de passwd.txt ---"
getfacl passwd.txt
```

### Ejercicio 3: Linux capabilities en practica

```bash
# Ver capabilities del proceso actual
cat /proc/self/status | grep Cap

# Decodificar capabilities (requiere libcap)
# Instalar si no existe
sudo apt install libcap2-bin -y 2>/dev/null

# Ver capabilities de ejecutables comunes
echo "--- Capabilities de ping ---"
getcap /usr/bin/ping 2>/dev/null || echo "ping no tiene caps especiales"

echo "--- Capabilities de todos los ejecutables ---"
sudo getcap -r /usr/bin/ 2>/dev/null | head -10

# Ver capabilities del proceso actual decodificadas
grep Cap /proc/self/status | while read line; do
    name=$(echo "$line" | cut -d: -f1)
    value=$(echo "$line" | tr -s ' ' | cut -d: -f2 | tr -d ' ')
    decoded=$(capsh --decode="$value" 2>/dev/null)
    echo "$name: $decoded"
done
```

## 5.8 Resumen del Modulo

```
MATRIZ DE ACCESO:
  Modelo teorico: filas=sujetos, columnas=objetos, celdas=permisos
  Problema: demasiado grande para almacenar completa

IMPLEMENTACIONES:
  1. ACL (por objeto):
     - chmod/setfacl en Linux
     - Facil: "quien accede a X?"
     - Dificil: "que puede hacer Y?"

  2. Capability List (por sujeto):
     - Linux capabilities (setcap/getcap)
     - Facil: "que puede hacer Y?"
     - Dificil: "quien accede a X?"

  3. Tabla de Autorizacion (triplas):
     - Bases de datos de permisos
     - Flexible para ambas consultas
     - Requiere busqueda

  Linux combina las 3: permisos Unix (ACL simple) + ACLs extendidas
  + capabilities del kernel.
```

## 5.9 Preguntas de Repaso

1. Que es una matriz de acceso y por que no se almacena completa?
2. Compara ACL vs Capability List: ventajas y desventajas de cada una.
3. Como se implementa la ACL en los permisos Unix (rwx)?
4. Que son las Linux capabilities y que problema resuelven?
5. En que escenario usarias una tabla de autorizacion en lugar de ACL?
