"""
EJERCICIOS DE INTRODUCCIÓN A PYTHON

Objetivo: Practicar conceptos fundamentales de programación en Python
mediante ejemplos prácticos y explicativos.
"""

# 1. VARIABLES Y TIPOS DE DATOS
"""
Objetivo: Demostrar la declaración de variables con diferentes tipos de datos
Tipos a explorar:
- Cadenas (str)
- Enteros (int)
- Flotantes (float)
- Booleanos (bool)

Conceptos:
- Asignación de valores
- Impresión de variables
- Uso de la función type() para identificar tipos
"""
nombre = "Juan Pérez"
edad = 25
altura = 1.75
es_estudiante = True

print("1. Variables y Tipos de Datos:")
print(f"Nombre: {nombre}")
print(f"Edad: {edad}")
print(f"Altura: {altura}")
print(f"Es estudiante: {es_estudiante}")
print(f"Tipo de nombre: {type(nombre)}")
print(f"Tipo de edad: {type(edad)}")
print(f"Tipo de altura: {type(altura)}")
print(f"Tipo de es_estudiante: {type(es_estudiante)}\n")

# 2. OPERADORES ARITMÉTICOS
"""
Objetivo: Practicar operaciones matemáticas básicas
Operadores a demostrar:
- Suma (+)
- Resta (-)
- Multiplicación (*)
- División (/)
- División entera (//)
- Módulo (%)
- Potencia (**)
Conceptos:
- Definición de función con múltiples operaciones
- Impresión de resultados de operaciones
"""
def calcular_operaciones(a, b):
    print("2. Operadores Aritméticos:")
    print(f"Suma: {a} + {b} = {a + b}")
    print(f"Resta: {a} - {b} = {a - b}")
    print(f"Multiplicación: {a} * {b} = {a * b}")
    print(f"División: {a} / {b} = {a / b}")
    print(f"División entera: {a} // {b} = {a // b}")
    print(f"Módulo (residuo): {a} % {b} = {a % b}")
    print(f"Potencia: {a} ** {b} = {a ** b}\n")

calcular_operaciones(10, 3)

# 3. OPERADORES LÓGICOS Y CONDICIONALES
"""
Objetivo: Implementar estructuras condicionales y operadores lógicos
Conceptos a practicar:
- Uso de if, elif, else
- Operadores lógicos (and, or, not)
- Operador ternario
- Evaluación de condiciones múltiples
"""
def clasificar_numero(numero):
    print("3. Operadores Lógicos y Condicionales:")
    
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
    print(f"Condición de edad: {resultado}\n")

clasificar_numero(20)
clasificar_numero(-5)
clasificar_numero(0)

# 4. FUNCIONES
"""
Objetivo: Demostrar definición y uso de funciones
Conceptos a practicar:
- Definición de funciones
- Recursividad
- Retorno de valores
- Documentación de funciones
"""
def calcular_factorial(n):
    """Calcula el factorial de un número usando recursividad"""
    print("4. Funciones y Recursividad:")
    if n == 0 or n == 1:
        return 1
    else:
        return n * calcular_factorial(n-1)

print(f"Factorial de 5: {calcular_factorial(5)}\n")

# 5. LOOPS: FOR
"""
Objetivo: Practicar iteración con bucles for
Conceptos a demostrar:
- Iteración sobre listas
- Uso de range()
- Recorrido de elementos
"""
print("5. Loops - For:")
frutas = ["manzana", "banana", "cereza"]
for fruta in frutas:
    print(f"Me gusta comer {fruta}")

# Rango de números con for
print("\nConteo con for:")
for i in range(5):
    print(f"Número: {i}")

# 6. LOOPS: WHILE
"""
Objetivo: Implementar bucles while con control de condición
Conceptos a practicar:
- Bucle while
- Incremento de contador
- Condición de parada
"""
print("\n6. Loops - While:")
contador = 0
while contador < 3:
    print(f"Contador: {contador}")
    contador += 1

# 7. LISTAS Y MANIPULACIÓN
"""
Objetivo: Demostrar operaciones básicas con listas
Conceptos a practicar:
- Creación de listas
- Métodos de lista (append, remove)
- Comprensión de listas
- Transformación de elementos
"""
numeros = [1, 2, 3, 4, 5]
print("\n7. Listas:")
print("Lista original:", numeros)
numeros.append(6)
print("Después de append:", numeros)
numeros.remove(3)
print("Después de remove:", numeros)
numeros_cuadrados = [x**2 for x in numeros]
print("Lista de cuadrados:", numeros_cuadrados)
