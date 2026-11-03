# Modulo 6: Proteccion Basada en el Lenguaje (Tema 6.5)

## 6.1 Teoria: Que es la Proteccion Basada en el Lenguaje?

Cuando la proteccion no solo depende del SO, sino que el propio
lenguaje de programacion la implementa como parte de su diseno.

```
Proteccion del SO (hardware/kernel):
  - Permisos de archivos, memoria virtual, rings del CPU
  - Opera a nivel bajo, general, para todos los programas
  - Si falla, el atacante tiene acceso al sistema

Proteccion del lenguaje (compilador/runtime):
  - El lenguaje IMPIDE al programador hacer cosas peligrosas
  - Opera a nivel del codigo fuente y tiempo de ejecucion
  - Agrega una capa ADICIONAL de proteccion

Analogia:
  SO = las leyes del pais (aplican a todos)
  Lenguaje = las reglas internas de una empresa
  Ambas se complementan: puedes cumplir la ley pero violar reglas internas
```

## 6.2 Mecanismos de Proteccion en Lenguajes

### Seguridad de Tipos (Type Safety)

```
El sistema de tipos PREVIENE operaciones invalidas en tiempo
de compilacion o ejecucion.

C (NO type-safe):
  int *ptr = (int *)0x12345;   // Apuntar a cualquier direccion
  *ptr = 42;                    // Escribir en memoria arbitraria
  -> PERMITIDO por el compilador, explota en ejecucion (o peor: funciona
     y corrompe datos silenciosamente)

Python (type-safe en runtime):
  x = "hola"
  y = x + 5   # TypeError: no puedes sumar string + int
  -> El RUNTIME detecta la operacion invalida y lanza excepcion

Rust (type-safe en compilacion):
  let x: &str = "hola";
  let y = x + 5;  // Error de compilacion: no compila
  -> El COMPILADOR detecta el error ANTES de ejecutar

Java (type-safe con verificacion):
  String x = "hola";
  int y = (int) x;  // Error de compilacion
  Object[] arr = new String[3];
  arr[0] = 42;  // ArrayStoreException en runtime
```

### Seguridad de Memoria (Memory Safety)

```
Previene que el programa acceda a memoria que no le pertenece.

PROBLEMAS comunes en lenguajes sin memory safety (C/C++):

1. Buffer Overflow:
   char buf[10];
   strcpy(buf, "este string es mucho mas largo que 10 caracteres");
   // Sobreescribe memoria adyacente -> posible ejecucion de codigo

2. Use-After-Free:
   int *ptr = malloc(sizeof(int));
   free(ptr);
   *ptr = 42;  // Accede a memoria ya liberada -> comportamiento indefinido

3. Dangling Pointer:
   int *ptr;
   {
       int x = 10;
       ptr = &x;
   }
   // x ya no existe, ptr apunta a basura

LENGUAJES con memory safety:
  - Python: Garbage collector, no hay punteros directos
  - Java: Garbage collector, verificacion de limites de arrays
  - Rust: Ownership system, borrow checker (sin GC!)
  - Go: Garbage collector, slices con bounds checking
```

### Sandboxing a Nivel de Lenguaje

```
El lenguaje/runtime restringe lo que el codigo puede hacer:

Java Security Manager (clasico, deprecado pero ilustrativo):
  - Applets web solo podian acceder a su propio sandbox
  - No acceso al sistema de archivos
  - No conexiones de red arbitrarias
  - No ejecucion de procesos del SO

Python RestrictedPython:
  - Subconjunto de Python que limita operaciones peligrosas
  - No acceso a __import__, exec, eval
  - Usado en Zope/Plone para codigo no confiable

WebAssembly (WASM):
  - Codigo compilado ejecuta en sandbox del navegador
  - No acceso directo a memoria del host
  - API limitada a lo que el host expone
```

## 6.3 Comparacion de Lenguajes por Nivel de Proteccion

```
┌──────────┬───────────┬───────────┬───────────┬────────────────────┐
│ Lenguaje │ Type Safe │ Mem Safe  │ Bounds    │ Mecanismo          │
│          │           │           │ Check     │                    │
├──────────┼───────────┼───────────┼───────────┼────────────────────┤
│ C        │ Debil     │ NO        │ NO        │ Confianza total    │
│          │           │           │           │ en el programador  │
├──────────┼───────────┼───────────┼───────────┼────────────────────┤
│ C++      │ Medio     │ NO*       │ NO*       │ Smart pointers     │
│          │           │           │           │ opcionales         │
├──────────┼───────────┼───────────┼───────────┼────────────────────┤
│ Java     │ SI        │ SI        │ SI        │ JVM + GC           │
├──────────┼───────────┼───────────┼───────────┼────────────────────┤
│ Python   │ SI (dyn)  │ SI        │ SI        │ Interprete + GC    │
├──────────┼───────────┼───────────┼───────────┼────────────────────┤
│ Rust     │ SI        │ SI        │ SI        │ Ownership + Borrow │
│          │           │           │           │ checker (compile)  │
├──────────┼───────────┼───────────┼───────────┼────────────────────┤
│ Go       │ SI        │ SI        │ SI        │ GC + bounds check  │
└──────────┴───────────┴───────────┴───────────┴────────────────────┘

* C++ ofrece mecanismos opcionales (smart pointers, std::vector)
  pero no los obliga. El programador puede ignorarlos.
```

## 6.4 El Modelo de Ownership de Rust (Ejemplo Avanzado)

```
Rust resuelve memory safety SIN garbage collector usando 3 reglas:

1. Cada valor tiene exactamente UN owner
2. Solo puede haber UN owner a la vez
3. Cuando el owner sale de scope, el valor se libera

Ejemplo:
  fn main() {
      let s1 = String::from("hola");  // s1 es owner
      let s2 = s1;                     // ownership se mueve a s2
      // println!("{}", s1);           // ERROR: s1 ya no es owner
      println!("{}", s2);              // OK: s2 es el owner
  }

  // Cuando s2 sale de scope, la memoria se libera automaticamente

Borrow checker (prestamos):
  fn main() {
      let s = String::from("hola");
      let len = calcular_largo(&s);  // &s = prestamo inmutable
      println!("Largo de '{}' es {}", s, len);  // s sigue disponible
  }

  fn calcular_largo(s: &String) -> usize {  // recibe referencia prestada
      s.len()
  }

Regla de prestamos:
  - Puedes tener MUCHAS referencias inmutables (&T)
  - O UNA sola referencia mutable (&mut T)
  - NUNCA ambas al mismo tiempo
  -> Previene data races en tiempo de compilacion!
```

## 6.5 Practica: Demostrando Proteccion del Lenguaje

### Ejercicio 1: Python - Type Safety y Memory Safety

```python
#!/usr/bin/env python3
"""
Demuestra como Python implementa proteccion a nivel de lenguaje.
"""

def demo_type_safety():
    """Python previene operaciones de tipos incompatibles."""
    print("=== TYPE SAFETY EN PYTHON ===\n")

    # Python detecta errores de tipo en RUNTIME
    operaciones = [
        ("'hola' + ' mundo'", "str + str"),
        ("5 + 3", "int + int"),
        ("'hola' + 5", "str + int (error)"),
        ("[1,2] + 'abc'", "list + str (error)"),
        ("{'a': 1}[0]", "dict key error"),
    ]

    for expr, desc in operaciones:
        try:
            resultado = eval(expr)
            print(f"  [OK] {desc}: {expr} = {resultado}")
        except TypeError as e:
            print(f"  [BLOQUEADO] {desc}: {expr}")
            print(f"              TypeError: {e}")
        except KeyError as e:
            print(f"  [BLOQUEADO] {desc}: {expr}")
            print(f"              KeyError: {e}")


def demo_memory_safety():
    """Python previene acceso fuera de limites."""
    print("\n=== MEMORY SAFETY EN PYTHON ===\n")

    lista = [10, 20, 30, 40, 50]
    print(f"  Lista: {lista} (largo: {len(lista)})")

    # Bounds checking automatico
    indices = [0, 2, 4, 5, -1, 100]
    for i in indices:
        try:
            valor = lista[i]
            print(f"  [OK] lista[{i}] = {valor}")
        except IndexError as e:
            print(f"  [BLOQUEADO] lista[{i}]: IndexError: {e}")

    # No hay punteros directos - no puedes acceder a memoria arbitraria
    print("\n  Python no permite acceso directo a memoria:")
    print("  - No hay punteros (como en C)")
    print("  - No puedes hacer: ptr = 0x12345; *ptr = 42")
    print("  - El garbage collector maneja la memoria por ti")


def demo_encapsulamiento():
    """Proteccion a nivel de clases."""
    print("\n=== ENCAPSULAMIENTO (PROTECCION DE DATOS) ===\n")

    class CuentaBancaria:
        """Ejemplo de proteccion de datos con propiedades."""

        def __init__(self, titular: str, saldo_inicial: float):
            self._titular = titular        # Convencion: privado
            self.__saldo = saldo_inicial   # Name mangling: mas privado

        @property
        def saldo(self) -> float:
            """Solo lectura del saldo."""
            return self.__saldo

        def depositar(self, monto: float):
            if monto <= 0:
                raise ValueError("Monto debe ser positivo")
            self.__saldo += monto
            print(f"    Deposito: +${monto:.2f} -> Saldo: ${self.__saldo:.2f}")

        def retirar(self, monto: float):
            if monto <= 0:
                raise ValueError("Monto debe ser positivo")
            if monto > self.__saldo:
                raise ValueError("Fondos insuficientes")
            self.__saldo -= monto
            print(f"    Retiro:   -${monto:.2f} -> Saldo: ${self.__saldo:.2f}")

    cuenta = CuentaBancaria("Luis", 1000.0)

    # Operaciones validas
    print(f"  Saldo inicial: ${cuenta.saldo:.2f}")
    cuenta.depositar(500)
    cuenta.retirar(200)

    # Intentos de violar la proteccion
    print("\n  Intentos de acceso no autorizado:")

    try:
        cuenta.saldo = 999999  # Property sin setter
        print("  [FALLO] Modificacion directa de saldo permitida!")
    except AttributeError as e:
        print(f"  [BLOQUEADO] cuenta.saldo = 999999: {e}")

    try:
        cuenta.retirar(-100)  # Validacion de negocio
    except ValueError as e:
        print(f"  [BLOQUEADO] retirar(-100): {e}")

    try:
        cuenta.retirar(99999)  # Fondos insuficientes
    except ValueError as e:
        print(f"  [BLOQUEADO] retirar(99999): {e}")

    # NOTA: Python NO previene el name mangling hack
    print(f"\n  ADVERTENCIA: Python no es 100% seguro en encapsulamiento:")
    print(f"  cuenta._CuentaBancaria__saldo = {cuenta._CuentaBancaria__saldo}")
    print(f"  -> El name mangling se puede rodear. Es convencion, no enforcement.")


def demo_sandbox_eval():
    """Demuestra riesgos de eval() y como mitigarlos."""
    print("\n=== RIESGO: eval() Y exec() ===\n")

    # eval() ejecuta codigo arbitrario - PELIGROSO
    print("  eval() puede ejecutar CUALQUIER expresion Python:")
    print("  eval('__import__(\"os\").system(\"whoami\")') <- ejecutaria comando del SO!")
    print()

    # Mitigacion: restringir el contexto de eval
    print("  Mitigacion: restringir builtins disponibles")

    contexto_seguro = {"__builtins__": {}}  # Sin builtins

    expresiones = [
        "2 + 2",
        "3 * 7",
        "__import__('os').system('whoami')",
    ]

    for expr in expresiones:
        try:
            resultado = eval(expr, contexto_seguro)
            print(f"  [OK] eval('{expr}') = {resultado}")
        except NameError as e:
            print(f"  [BLOQUEADO] eval('{expr}'): {e}")
        except Exception as e:
            print(f"  [BLOQUEADO] eval('{expr}'): {type(e).__name__}: {e}")

    print("\n  MEJOR PRACTICA: Nunca usar eval() con input del usuario.")
    print("  Usar ast.literal_eval() para evaluar literales seguros.")


def demo_comparison_c_vs_python():
    """Muestra como C permitiria cosas que Python bloquea."""
    print("\n=== COMPARACION: QUE PERMITE C vs QUE BLOQUEA PYTHON ===\n")

    comparaciones = [
        ("Buffer Overflow",
         "char buf[5]; strcpy(buf, 'AAAAAAAAAA');",
         "Python: las listas/strings crecen dinamicamente, no hay overflow"),
        ("Null Pointer Deref",
         "int *p = NULL; *p = 42;",
         "Python: no hay punteros nulos. None causa AttributeError"),
        ("Use After Free",
         "free(ptr); *ptr = 10;",
         "Python: garbage collector libera memoria. No hay free() manual"),
        ("Integer Overflow",
         "int x = 2147483647; x++;  // Wraps to -2147483648",
         "Python: enteros de precision arbitraria. 2**1000 funciona"),
        ("Type Confusion",
         "void *p = &x; float *f = (float *)p;",
         "Python: no hay casts de punteros. TypeError si tipos incompatibles"),
    ]

    for nombre, c_code, python_note in comparaciones:
        print(f"  {nombre}:")
        print(f"    C:      {c_code}")
        print(f"    Python: {python_note}")
        print()


if __name__ == "__main__":
    demo_type_safety()
    demo_memory_safety()
    demo_encapsulamiento()
    demo_sandbox_eval()
    demo_comparison_c_vs_python()
```

Guarda como `proteccion_lenguaje.py` y ejecuta:

```bash
python3 proteccion_lenguaje.py
```

### Ejercicio 2: Demostrando Buffer Overflow en C (educativo)

```c
/* buffer_overflow_demo.c
 * SOLO PARA FINES EDUCATIVOS
 * Demuestra por que C no tiene proteccion a nivel de lenguaje.
 * Compilar: gcc -fno-stack-protector -o overflow buffer_overflow_demo.c
 */
#include <stdio.h>
#include <string.h>

void funcion_vulnerable() {
    char buffer[8];  /* Solo caben 8 caracteres */

    printf("Buffer de 8 bytes en direccion: %p\n", (void *)buffer);
    printf("Ingresa texto (mas de 8 chars para overflow): ");

    /* gets() NO verifica limites - NUNCA usar en codigo real */
    /* gets(buffer);  <- peligroso, descomentar solo para demo */

    /* Version segura con fgets */
    fgets(buffer, sizeof(buffer), stdin);

    printf("Contenido: %s\n", buffer);
}

void funcion_secreta() {
    printf("\n!!! FUNCION SECRETA EJECUTADA !!!\n");
    printf("En un ataque real, esto seria codigo malicioso.\n");
}

int main() {
    printf("=== Demo Buffer Overflow (educativo) ===\n");
    printf("Direccion de funcion_secreta: %p\n\n", (void *)funcion_secreta);

    printf("Con fgets (seguro): limita lectura a sizeof(buffer)\n");
    funcion_vulnerable();

    printf("\nNOTA: En C, la proteccion depende del PROGRAMADOR.\n");
    printf("Python/Java/Rust hacen esto automaticamente.\n");

    return 0;
}
```

Compilar y ejecutar:

```bash
# Compilar
gcc -o /tmp/overflow_demo /tmp/buffer_overflow_demo.c 2>/dev/null

# Ejecutar
echo "hola" | /tmp/overflow_demo
```

### Ejercicio 3: ctypes - Cuando Python pierde su proteccion

```python
#!/usr/bin/env python3
"""
Demuestra que Python pierde su proteccion de memoria
cuando usas ctypes (interfaz directa con C).
"""
import ctypes
import sys

def demo_ctypes_riesgo():
    print("=== CTYPES: PYTHON PIERDE MEMORY SAFETY ===\n")

    # Python normal: protegido
    x = 42
    print(f"  Variable normal: x = {x}")
    print(f"  id(x) = {id(x)} (direccion en CPython)")
    print(f"  sys.getrefcount(x) = {sys.getrefcount(x)}")

    # Con ctypes: acceso directo a memoria (PELIGROSO)
    print("\n  Con ctypes puedes acceder a memoria directamente:")
    print("  ctypes.cast(id(x), ctypes.POINTER(ctypes.c_long))")
    print("  -> Esto ROMPE la seguridad de memoria de Python")
    print("  -> Solo usar para interop con librerias C")

    # Demostrar lectura (seguro de demostrar)
    # Los enteros pequenos en CPython estan pre-cacheados
    ptr = ctypes.cast(id(x), ctypes.POINTER(ctypes.c_long))
    print(f"\n  Leyendo via puntero: ptr[0] = {ptr[0]}")
    print(f"  (Esto lee el refcount interno del objeto)")

    print("\n  LECCION: Los mecanismos de proteccion del lenguaje")
    print("  se pueden bypassear con FFI (Foreign Function Interface).")
    print("  Por eso, librerias que usan ctypes/cffi deben auditarse.")


if __name__ == "__main__":
    demo_ctypes_riesgo()
```

## 6.6 Resumen del Modulo

```
PROTECCION BASADA EN EL LENGUAJE:
  Capa adicional de seguridad implementada por el lenguaje/runtime.
  Complementa (no reemplaza) la proteccion del SO.

MECANISMOS CLAVE:
  Type Safety:     Previene operaciones de tipos incompatibles
  Memory Safety:   Previene acceso a memoria invalida
  Bounds Checking: Previene acceso fuera de limites de arrays
  Encapsulamiento: Restringe acceso a datos internos
  Sandboxing:      Limita capacidades del codigo no confiable

COMPARACION:
  C/C++:     Minima proteccion, maximo rendimiento, maximo riesgo
  Python:    Proteccion en runtime (type safe, memory safe, GC)
  Java:      Proteccion en JVM (type safe, memory safe, sandbox)
  Rust:      Proteccion en compilacion (ownership, borrow checker)

LIMITACIONES:
  - Se puede bypassear con FFI (ctypes, JNI, unsafe en Rust)
  - eval()/exec() rompen las garantias del lenguaje
  - La proteccion del lenguaje NO reemplaza permisos del SO
```

## 6.7 Preguntas de Repaso

1. Que diferencia hay entre proteccion del SO y proteccion del lenguaje?
2. Que es type safety? Da un ejemplo en Python vs C.
3. Por que Rust no necesita garbage collector para ser memory safe?
4. Que riesgos tiene usar eval() en Python? Como se mitiga?
5. En que situaciones la proteccion del lenguaje puede ser bypassed?
