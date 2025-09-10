# 📘 Clase y Práctica: Manejo de Errores en Python con `try` y `except`

## 1. ¿Qué es una excepción?
Una **excepción** es un error que ocurre durante la ejecución de un programa y que, si no se maneja, detiene el flujo normal.  

Ejemplo:
```python
print(10 / 0)  # Error: ZeroDivisionError
```

---

## 2. ¿Qué hace `try` y `except`?
Sirve para **manejar excepciones** y evitar que el programa se interrumpa.  

Estructura básica:
```python
try:
    # Código que puede generar un error
    ...
except:
    # Código que se ejecuta si ocurre un error
    ...
```

Ejemplo:
```python
try:
    numero = int("abc")
except:
    print("Ocurrió un error al convertir el texto en número")
```

---

## 3. Manejo de excepciones específicas
Podemos capturar un **tipo específico de error**:
```python
try:
    resultado = 10 / 0
except ZeroDivisionError:
    print("No se puede dividir entre cero")
```

---

## 4. Uso de `else` y `finally`
- `else`: se ejecuta si **no hubo error**.  
- `finally`: se ejecuta **siempre**, ocurra o no error.  

Ejemplo:
```python
try:
    numero = int("123")
except ValueError:
    print("Error: no se pudo convertir")
else:
    print("Conversión exitosa:", numero)
finally:
    print("Fin del bloque try-except")
```

---

# 📝 Práctica: Uso de `try` y `except`

## 🎯 Objetivo
Que los estudiantes aprendan a **manejar errores comunes** en Python para que sus programas sean más robustos.

---

## 📘 Ejercicio 1: División segura
1. Crea un archivo `division_segura.py`.  
2. Pide dos números al usuario.  
3. Intenta dividirlos usando `try` y `except`.  
4. Maneja estos casos:
   - Error al ingresar texto en lugar de número → `ValueError`.  
   - División entre cero → `ZeroDivisionError`.  

Ejemplo esperado:
```
Ingresa el primer número: 10
Ingresa el segundo número: 0
Error: No se puede dividir entre cero
```

---

## 📘 Ejercicio 2: Lectura de archivos
1. Crea un archivo `lectura_archivo.py`.  
2. Pide al usuario un nombre de archivo.  
3. Intenta abrirlo y mostrar su contenido.  
4. Maneja el error `FileNotFoundError` si no existe.  

Ejemplo esperado:
```
Ingresa el nombre del archivo: datos.txt
Error: El archivo no existe
```

---

## 📘 Ejercicio 3: Calculadora con validación
1. Crea un archivo `calculadora.py`.  
2. Pide al usuario dos números y una operación (`+`, `-`, `*`, `/`).  
3. Maneja los siguientes errores:
   - Entrada inválida (`ValueError`).  
   - División entre cero (`ZeroDivisionError`).  
   - Operación no reconocida.  

Ejemplo esperado:
```
Ingresa el primer número: 8
Ingresa el segundo número: 2
Ingresa la operación (+, -, *, /): /
Resultado: 4.0
```

---