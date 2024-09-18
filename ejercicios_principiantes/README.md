# 15 Ejercicios de Python para Principiantes

## 1. Hola Mundo
**Pregunta:** Escribe un programa que imprima "Hola Mundo" en la pantalla.

**Respuesta:**
```python
print("Hola Mundo")
```

## 2. Suma de dos números
**Pregunta:** Escribe un programa que sume dos números ingresados por el usuario.

**Respuesta:**
```python
num1 = float(input("Ingresa el primer número: "))
num2 = float(input("Ingresa el segundo número: "))
suma = num1 + num2
print(f"La suma de {num1} y {num2} es: {suma}")
```

## 3. Área de un círculo
**Pregunta:** Calcula el área de un círculo con el radio proporcionado por el usuario.

**Respuesta:**
```python
import math

radio = float(input("Ingresa el radio del círculo: "))
area = math.pi * radio ** 2
print(f"El área del círculo con radio {radio} es: {area:.2f}")
```

## 4. Número par o impar
**Pregunta:** Determina si un número ingresado por el usuario es par o impar.

**Respuesta:**
```python
numero = int(input("Ingresa un número: "))
if numero % 2 == 0:
    print(f"{numero} es par")
else:
    print(f"{numero} es impar")
```

## 5. Calculadora simple
**Pregunta:** Crea una calculadora que realice operaciones básicas (suma, resta, multiplicación, división) según la elección del usuario.

**Respuesta:**
```python
def calculadora(a, b, operacion):
    if operacion == '+':
        return a + b
    elif operacion == '-':
        return a - b
    elif operacion == '*':
        return a * b
    elif operacion == '/':
        return a / b if b != 0 else "Error: División por cero"

num1 = float(input("Ingresa el primer número: "))
num2 = float(input("Ingresa el segundo número: "))
op = input("Ingresa la operación (+, -, *, /): ")

resultado = calculadora(num1, num2, op)
print(f"El resultado es: {resultado}")
```

## 6. Factorial de un número
**Pregunta:** Calcula el factorial de un número ingresado por el usuario.

**Respuesta:**
```python
def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

num = int(input("Ingresa un número para calcular su factorial: "))
print(f"El factorial de {num} es: {factorial(num)}")
```

## 7. Tabla de multiplicar
**Pregunta:** Imprime la tabla de multiplicar de un número ingresado por el usuario.

**Respuesta:**
```python
num = int(input("Ingresa un número para ver su tabla de multiplicar: "))
for i in range(1, 11):
    print(f"{num} x {i} = {num * i}")
```

## 8. Promedio de una lista
**Pregunta:** Calcula el promedio de una lista de números ingresados por el usuario.

**Respuesta:**
```python
numeros = input("Ingresa una lista de números separados por espacios: ").split()
numeros = [float(num) for num in numeros]
promedio = sum(numeros) / len(numeros)
print(f"El promedio de los números ingresados es: {promedio:.2f}")
```

## 9. Palíndromo
**Pregunta:** Verifica si una palabra ingresada por el usuario es un palíndromo.

**Respuesta:**
```python
palabra = input("Ingresa una palabra: ").lower()
if palabra == palabra[::-1]:
    print(f"{palabra} es un palíndromo")
else:
    print(f"{palabra} no es un palíndromo")
```

## 10. Contador de vocales
**Pregunta:** Cuenta el número de vocales en una cadena ingresada por el usuario.

**Respuesta:**
```python
def contar_vocales(cadena):
    vocales = "aeiouAEIOU"
    return sum(1 for letra in cadena if letra in vocales)

texto = input("Ingresa una cadena de texto: ")
num_vocales = contar_vocales(texto)
print(f"El número de vocales en el texto es: {num_vocales}")
```

## 11. Conversor de temperatura
**Pregunta:** Convierte una temperatura de Celsius a Fahrenheit o viceversa, según la elección del usuario.

**Respuesta:**
```python
def celsius_a_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def fahrenheit_a_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9

opcion = input("Elige la conversión (C a F / F a C): ").upper()
temp = float(input("Ingresa la temperatura: "))

if opcion == "C A F":
    resultado = celsius_a_fahrenheit(temp)
    print(f"{temp}°C es igual a {resultado:.2f}°F")
elif opcion == "F A C":
    resultado = fahrenheit_a_celsius(temp)
    print(f"{temp}°F es igual a {resultado:.2f}°C")
else:
    print("Opción no válida")
```

## 12. Adivina el número
**Pregunta:** Crea un juego donde el usuario debe adivinar un número aleatorio entre 1 y 100.

**Respuesta:**
```python
import random

numero_secreto = random.randint(1, 100)
intentos = 0

while True:
    intento = int(input("Adivina el número (entre 1 y 100): "))
    intentos += 1
    
    if intento < numero_secreto:
        print("Demasiado bajo, intenta de nuevo.")
    elif intento > numero_secreto:
        print("Demasiado alto, intenta de nuevo.")
    else:
        print(f"¡Correcto! Adivinaste en {intentos} intentos.")
        break
```

## 13. Generador de contraseñas
**Pregunta:** Crea un generador de contraseñas aleatorias con una longitud especificada por el usuario.

**Respuesta:**
```python
import random
import string

def generar_contrasena(longitud):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contrasena = ''.join(random.choice(caracteres) for _ in range(longitud))
    return contrasena

longitud = int(input("Ingresa la longitud deseada para la contraseña: "))
nueva_contrasena = generar_contrasena(longitud)
print(f"Tu nueva contraseña es: {nueva_contrasena}")
```

## 14. Calculadora de IMC
**Pregunta:** Calcula el Índice de Masa Corporal (IMC) a partir del peso y la altura ingresados por el usuario.

**Respuesta:**
```python
def calcular_imc(peso, altura):
    return peso / (altura ** 2)

peso = float(input("Ingresa tu peso en kg: "))
altura = float(input("Ingresa tu altura en metros: "))

imc = calcular_imc(peso, altura)
print(f"Tu IMC es: {imc:.2f}")

if imc < 18.5:
    print("Bajo peso")
elif 18.5 <= imc < 25:
    print("Peso normal")
elif 25 <= imc < 30:
    print("Sobrepeso")
else:
    print("Obesidad")
```

## 15. Piedra, Papel o Tijera
**Pregunta:** Implementa el juego de Piedra, Papel o Tijera contra la computadora.

**Respuesta:**
```python
import random

def jugar():
    opciones = ["piedra", "papel", "tijera"]
    computadora = random.choice(opciones)
    jugador = input("Elige piedra, papel o tijera: ").lower()
    
    if jugador not in opciones:
        return "Opción no válida. Por favor, elige piedra, papel o tijera."
    
    if jugador == computadora:
        return f"Empate. Ambos eligieron {jugador}."
    
    if (jugador == "piedra" and computadora == "tijera") or \
       (jugador == "papel" and computadora == "piedra") or \
       (jugador == "tijera" and computadora == "papel"):
        return f"¡Ganaste! {jugador} vence a {computadora}."
    else:
        return f"Perdiste. {computadora} vence a {jugador}."

print(jugar())
```
