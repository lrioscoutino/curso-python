# Curso de Python y Django: De Principiante a Intermedio

## Módulo 1: Introducción a Python

### 1.1 Configuración del entorno

La configuración adecuada del entorno de desarrollo es crucial para comenzar a programar en Python.

- Instalación de Python:
  Python se puede descargar desde python.org. Es importante verificar la instalación para asegurarse de que Python está correctamente configurado en el sistema.

  ```bash
  python --version
  ```

- Uso de entornos virtuales:
  Los entornos virtuales son espacios aislados donde puedes instalar paquetes específicos para cada proyecto sin afectar a tu sistema global.

  ```bash
  python -m venv mi_entorno
  source mi_entorno/bin/activate  # En Windows: mi_entorno\Scripts\activate
  ```

  Esto crea un nuevo entorno virtual llamado "mi_entorno" y lo activa, permitiéndote instalar paquetes específicos para tu proyecto.

### 1.2 Fundamentos de Python

Python es un lenguaje de alto nivel con una sintaxis clara y legible.

- Variables y tipos de datos:
  En Python, no necesitas declarar el tipo de una variable. El tipo se infiere automáticamente.

  ```python
  # Enteros
  edad = 25
  
  # Flotantes
  altura = 1.75
  
  # Cadenas
  nombre = "Ana"
  
  # Booleanos
  es_estudiante = True
  ```

  Aquí, `edad` es un entero, `altura` es un flotante, `nombre` es una cadena y `es_estudiante` es un booleano.

- Operadores:
  Python soporta varios tipos de operadores para realizar operaciones.

  ```python
  # Aritméticos
  suma = 5 + 3        # Suma
  resta = 10 - 4      # Resta
  multiplicacion = 2 * 3  # Multiplicación
  division = 15 / 3   # División

  # Comparación
  es_igual = (5 == 5)  # Igualdad
  es_mayor = (10 > 5)  # Mayor que
  ```

  Los operadores aritméticos realizan cálculos, mientras que los operadores de comparación devuelven valores booleanos.

- Estructuras de control:
  Las estructuras de control permiten tomar decisiones en el código.

  ```python
  edad = 18
  if edad >= 18:
      print("Eres mayor de edad")
  elif edad >= 13:
      print("Eres un adolescente")
  else:
      print("Eres un niño")
  ```

  Este código verifica la edad y imprime un mensaje diferente dependiendo del valor.

- Bucles:
  Los bucles permiten repetir acciones múltiples veces.

  ```python
  # For loop
  for i in range(5):
      print(i)
  
  # While loop
  contador = 0
  while contador < 5:
      print(contador)
      contador += 1
  ```

  El bucle `for` itera sobre una secuencia (en este caso, los números del 0 al 4). El bucle `while` continúa mientras su condición sea verdadera.

### 1.3 Estructuras de datos

Python ofrece varias estructuras de datos incorporadas para almacenar colecciones de elementos.

- Listas:
  Las listas son colecciones ordenadas y mutables.

  ```python
  frutas = ["manzana", "banana", "cereza"]
  print(frutas[0])  # manzana
  frutas.append("naranja")
  ```

  Puedes acceder a elementos por índice y modificar la lista (por ejemplo, añadiendo elementos con `append`).

- Tuplas:
  Las tuplas son colecciones ordenadas e inmutables.

  ```python
  coordenadas = (10, 20)
  x, y = coordenadas
  ```

  Las tuplas son útiles para datos que no deben cambiar, como coordenadas.

- Diccionarios:
  Los diccionarios almacenan pares clave-valor.

  ```python
  persona = {
      "nombre": "Juan",
      "edad": 30,
      "ciudad": "Madrid"
  }
  print(persona["nombre"])  # Juan
  ```

  Puedes acceder a los valores utilizando sus claves.

- Conjuntos:
  Los conjuntos son colecciones no ordenadas de elementos únicos.

  ```python
  numeros = {1, 2, 3, 4, 5}
  numeros.add(6)
  print(2 in numeros)  # True
  ```

  Los conjuntos son útiles para eliminar duplicados y realizar operaciones de conjunto.

### 1.4 Funciones

Las funciones permiten organizar y reutilizar código.

- Definición y llamada de funciones:
  ```python
  def saludar(nombre):
      return f"Hola, {nombre}!"

  mensaje = saludar("María")
  print(mensaje)  # Hola, María!
  ```

  Esta función toma un parámetro `nombre` y devuelve un saludo personalizado.

- Argumentos y parámetros:
  ```python
  def suma(a, b=0):
      return a + b

  print(suma(5, 3))  # 8
  print(suma(5))     # 5
  ```

  Aquí, `b` tiene un valor por defecto de 0, lo que permite llamar a la función con uno o dos argumentos.

- Retorno de valores:
  ```python
  def dividir(a, b):
      if b == 0:
          return "Error: División por cero"
      return a / b

  resultado = dividir(10, 2)
  print(resultado)  # 5.0
  ```

  Esta función maneja el caso especial de división por cero y devuelve el resultado de la división en otros casos.

### 1.5 Programación orientada a objetos

La programación orientada a objetos (POO) es un paradigma que organiza el código en objetos que contienen datos y código.

- Clases y objetos:
  ```python
  class Perro:
      def __init__(self, nombre, edad):
          self.nombre = nombre
          self.edad = edad
      
      def ladrar(self):
          return f"{self.nombre} dice: ¡Guau!"

  mi_perro = Perro("Fido", 3)
  print(mi_perro.ladrar())  # Fido dice: ¡Guau!
  ```

  Esta clase `Perro` define un objeto con atributos (nombre, edad) y un método (ladrar).

- Herencia:
  ```python
  class Animal:
      def __init__(self, nombre):
          self.nombre = nombre
      
      def hablar(self):
          pass

  class Gato(Animal):
      def hablar(self):
          return f"{self.nombre} dice: ¡Miau!"

  mi_gato = Gato("Whiskers")
  print(mi_gato.hablar())  # Whiskers dice: ¡Miau!
  ```

  Aquí, `Gato` hereda de `Animal` y sobrescribe el método `hablar`.

## Módulo 2: Python Intermedio

### 2.1 Manejo de excepciones

El manejo de excepciones permite manejar errores de manera elegante.

- Try, except, else, finally:
  ```python
  try:
      numero = int(input("Introduce un número: "))
      resultado = 10 / numero
  except ValueError:
      print("Error: Debes introducir un número válido")
  except ZeroDivisionError:
      print("Error: No se puede dividir por cero")
  else:
      print(f"El resultado es: {resultado}")
  finally:
      print("Operación finalizada")
  ```

  Este código maneja posibles errores al convertir la entrada del usuario a un entero y al realizar una división.

- Creación de excepciones personalizadas:
  ```python
  class EdadInvalidaError(Exception):
      pass

  def verificar_edad(edad):
      if edad < 0 or edad > 120:
          raise EdadInvalidaError("La edad debe estar entre 0 y 120")
      return "Edad válida"

  try:
      print(verificar_edad(150))
  except EdadInvalidaError as e:
      print(f"Error: {e}")
  ```

  Aquí se define una excepción personalizada para manejar edades fuera de un rango válido.

### 2.2 Módulos y paquetes

Los módulos y paquetes permiten organizar y reutilizar código en múltiples archivos y proyectos.

- Importación de módulos:
  ```python
  import math
  print(math.pi)  # 3.141592653589793

  from datetime import datetime
  ahora = datetime.now()
  print(ahora)
  ```

  Estos ejemplos muestran cómo importar módulos completos o funciones específicas.

- Creación de módulos propios:
  ```python
  # En archivo utils.py
  def saludar(nombre):
      return f"Hola, {nombre}!"

  # En otro archivo
  from utils import saludar
  print(saludar("Ana"))  # Hola, Ana!
  ```

  Esto demuestra cómo crear y usar tus propios módulos.

### 2.3 Trabajo con archivos

Python ofrece funciones para leer y escribir archivos fácilmente.

- Lectura y escritura de archivos:
  ```python
  # Escritura
  with open("ejemplo.txt", "w") as archivo:
      archivo.write("Hola, mundo!")

  # Lectura
  with open("ejemplo.txt", "r") as archivo:
      contenido = archivo.read()
      print(contenido)  # Hola, mundo!
  ```

  El uso de `with` asegura que el archivo se cierre correctamente después de su uso.

- Manejo de rutas con os y pathlib:
  ```python
  import os
  from pathlib import Path

  # Usando os
  ruta_actual = os.getcwd()
  print(ruta_actual)

  # Usando pathlib
  ruta = Path("carpeta/subcarpeta/archivo.txt")
  print(ruta.parent)
  print(ruta.name)
  ```

  `os` y `pathlib` proporcionan funciones para trabajar con rutas de archivo de manera compatible con diferentes sistemas operativos.

### 2.4 Programación funcional

La programación funcional se centra en el uso de funciones para resolver problemas.

- Funciones lambda:
  ```python
  cuadrado = lambda x: x ** 2
  print(cuadrado(5))  # 25
  ```

  Las funciones lambda son funciones anónimas de una sola expresión.

- Map, filter, reduce:
  ```python
  numeros = [1, 2, 3, 4, 5]
  
  # Map
  cuadrados = list(map(lambda x: x ** 2, numeros))
  print(cuadrados)  # [1, 4, 9, 16, 25]

  # Filter
  pares = list(filter(lambda x: x % 2 == 0, numeros))
  print(pares)  # [2, 4]

  # Reduce
  from functools import reduce
  suma = reduce(lambda x, y: x + y, numeros)
  print(suma)  # 15
  ```

  `map` aplica una función a cada elemento de una secuencia, `filter` selecciona elementos basados en una condición, y `reduce` aplica una función de forma acumulativa.

### 2.5 Generadores e iteradores

Los generadores e iteradores permiten trabajar con secuencias de datos de manera eficiente.

- Creación de generadores:
  ```python
  def contador(max):
      n = 0
      while n < max:
          yield n
          n += 1

  for num in contador(5):
      print(num)  # Imprime 0, 1, 2, 3, 4
  ```

  Los generadores producen valores bajo demanda, lo que es útil para secuencias grandes o infinitas.

- Uso de iteradores:
  ```python
  mi_lista = [1, 2, 3, 4, 5]
  iterador = iter(mi_lista)
  
  print(next(iterador))  # 1
  print(next(iterador))  # 2
  ```

  Los iteradores permiten recorrer una secuencia elemento por elemento.

[El resto del curso continúa como en la versión anterior...]
