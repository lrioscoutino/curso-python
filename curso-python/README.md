# Ejercicios de Introducción a Python

## 1. Variables y Tipos de Datos

**Objetivo:** Demostrar la declaración de variables con diferentes tipos de datos

```python
nombre = "Juan Pérez"
edad = 25
altura = 1.75
es_estudiante = True

print("Variables:")
print(f"Nombre: {nombre}")
print(f"Edad: {edad}")
print(f"Altura: {altura}")
print(f"Es estudiante: {es_estudiante}")
print(f"Tipo de nombre: {type(nombre)}")
print(f"Tipo de edad: {type(edad)}")
print(f"Tipo de altura: {type(altura)}")
print(f"Tipo de es_estudiante: {type(es_estudiante)}")
```

## 2. Operadores Aritméticos

**Objetivo:** Practicar operaciones matemáticas básicas

```python
def calcular_operaciones(a, b):
    print("Operadores Aritméticos:")
    print(f"Suma: {a} + {b} = {a + b}")
    print(f"Resta: {a} - {b} = {a - b}")
    print(f"Multiplicación: {a} * {b} = {a * b}")
    print(f"División: {a} / {b} = {a / b}")
    print(f"División entera: {a} // {b} = {a // b}")
    print(f"Módulo (residuo): {a} % {b} = {a % b}")
    print(f"Potencia: {a} ** {b} = {a ** b}")

calcular_operaciones(10, 3)
```

## 3. Operadores Lógicos y Condicionales

**Objetivo:** Implementar estructuras condicionales y operadores lógicos

```python
def clasificar_numero(numero):
    print("Operadores Lógicos y Condicionales:")
    
    if numero > 0 and numero % 2 == 0:
        print(f"{numero} es un número positivo par")
    elif numero > 0 and numero % 2 != 0:
        print(f"{numero} es un número positivo impar")
    elif numero < 0:
        print(f"{numero} es un número negativo")
    else:
        print(f"{numero} es cero")
    
    # Operador ternario
    resultado = "Mayor de edad" if numero >= 18 else "Menor de edad"
    print(f"Condición de edad: {resultado}")

clasificar_numero(20)
clasificar_numero(-5)
clasificar_numero(0)
```

## 4. Funciones y Recursividad

**Objetivo:** Demostrar definición y uso de funciones

```python
def calcular_factorial(n):
    """Calcula el factorial de un número usando recursividad"""
    if n == 0 or n == 1:
        return 1
    else:
        return n * calcular_factorial(n-1)

print("Factorial de 5:", calcular_factorial(5))
```

## 5. Loops: For

**Objetivo:** Practicar iteración con bucles for

```python
# Iteración sobre lista
frutas = ["manzana", "banana", "cereza"]
for fruta in frutas:
    print(f"Me gusta comer {fruta}")

# Conteo con range()
print("\nConteo con for:")
for i in range(5):
    print(f"Número: {i}")
```

## 6. Loops: While

**Objetivo:** Implementar bucles while con control de condición

```python
contador = 0
while contador < 3:
    print(f"Contador: {contador}")
    contador += 1
```

## 7. Listas y Manipulación

**Objetivo:** Demostrar operaciones básicas con listas

```python
numeros = [1, 2, 3, 4, 5]
print("Lista original:", numeros)

# Agregar elemento
numeros.append(6)
print("Después de append:", numeros)

# Eliminar elemento
numeros.remove(3)
print("Después de remove:", numeros)

# Comprensión de lista
numeros_cuadrados = [x**2 for x in numeros]
print("Lista de cuadrados:", numeros_cuadrados)
```