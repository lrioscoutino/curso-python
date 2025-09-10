# 📘 Clase y Práctica: Decoradores en Python

## 1. ¿Qué es un decorador?
Un **decorador** en Python es una función que recibe otra función como argumento, le añade funcionalidad extra y devuelve una nueva función.  
- Es una forma de aplicar el principio **“open/closed”**: extender funcionalidad sin modificar el código original.  
- Se implementa con `@` encima de la función.  

---

## 2. Ejemplo básico
```python
def mi_decorador(func):
    def envoltura():
        print("Antes de ejecutar la función")
        func()
        print("Después de ejecutar la función")
    return envoltura

@mi_decorador
def saludar():
    print("Hola mundo")

saludar()
```

📌 Salida:
```
Antes de ejecutar la función
Hola mundo
Después de ejecutar la función
```

---

## 3. Decoradores con parámetros en la función
```python
def mi_decorador(func):
    def envoltura(*args, **kwargs):
        print("Ejecutando función con decorador")
        return func(*args, **kwargs)
    return envoltura

@mi_decorador
def sumar(a, b):
    return a + b

print(sumar(3, 5))
```

📌 Salida:
```
Ejecutando función con decorador
8
```

---

## 4. Decoradores anidados (múltiples)
```python
def mayusculas(func):
    def envoltura(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return envoltura

def signos(func):
    def envoltura(*args, **kwargs):
        return "¡" + func(*args, **kwargs) + "!"
    return envoltura

@mayusculas
@signos
def mensaje():
    return "hola"

print(mensaje())  # ¡HOLA!
```

---

## 5. Decoradores útiles en la práctica
- **Autenticación** en APIs o aplicaciones web.  
- **Medir tiempos de ejecución**.  
- **Validar parámetros**.  
- **Logs y debugging**.  

Ejemplo: Medir tiempo de ejecución
```python
import time

def medir_tiempo(func):
    def envoltura(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()
        print(f"Tiempo de ejecución: {fin - inicio:.4f} segundos")
        return resultado
    return envoltura

@medir_tiempo
def procesar():
    time.sleep(2)
    print("Proceso terminado")

procesar()
```

---

# 📝 Práctica: Decoradores en Python

## 🎯 Objetivo
Aprender a crear y usar **decoradores personalizados** para mejorar funciones existentes.  

---

## 📘 Ejercicio 1: Registro de funciones
1. Crea un archivo `decorador_log.py`.  
2. Implementa un decorador que imprima el nombre de la función cada vez que se ejecuta.  
3. Aplica el decorador a 2 funciones distintas.  

---

## 📘 Ejercicio 2: Validación de argumentos
1. Crea un archivo `decorador_validacion.py`.  
2. Haz un decorador que valide que los argumentos sean números antes de ejecutar una función de suma.  
3. Si se pasa algo que no es número, muestra un error.  

Ejemplo esperado:
```
>>> sumar("a", 3)
Error: Los parámetros deben ser números
```

---

## 📘 Ejercicio 3: Medición de tiempo
1. Crea un archivo `decorador_tiempo.py`.  
2. Implementa un decorador que mida el tiempo de ejecución de una función.  
3. Aplícalo a una función que simule un proceso lento (`time.sleep`).  

---
