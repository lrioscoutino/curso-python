# 15 Ejercicios de Python de Nivel Intermedio

## 1. Anagrama
**Pregunta:** Escribe una función que determine si dos palabras son anagramas.

**Respuesta:**
```python
def es_anagrama(palabra1, palabra2):
    if len(palabra1) != len(palabra2):
        return False
    return sorted(palabra1.lower()) == sorted(palabra2.lower())

print(es_anagrama("escuela", "cuclees"))  # True
print(es_anagrama("python", "java"))  # False
```

## 2. Invertir una cadena
**Pregunta:** Crea una función que invierta el orden de los caracteres en una cadena.

**Respuesta:**
```python
def invertir_cadena(cadena):
    return cadena[::-1]

print(invertir_cadena("Python"))  # nohtyP
print(invertir_cadena("Hola mundo"))  # odnum aloH
```

## 3. Fibonacci
**Pregunta:** Implementa la secuencia de Fibonacci hasta el n-ésimo término.

**Respuesta:**
```python
def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(0))  # 0
print(fibonacci(1))  # 1
print(fibonacci(6))  # 8
```

## 4. Eliminar duplicados
**Pregunta:** Crea una función que elimine los elementos duplicados de una lista.

**Respuesta:**
```python
def eliminar_duplicados(lista):
    return list(set(lista))

print(eliminar_duplicados([1, 2, 3, 2, 4, 1, 5]))  # [1, 2, 3, 4, 5]
print(eliminar_duplicados(["apple", "banana", "cherry", "banana"]))  # ['apple', 'banana', 'cherry']
```

## 5. Palindromo
**Pregunta:** Crea una función que determine si una cadena es un palíndromo.

**Respuesta:**
```python
def es_palindromo(cadena):
    cadena = cadena.lower().replace(" ", "")
    return cadena == cadena[::-1]

print(es_palindromo("Anita lava la tina"))  # True
print(es_palindromo("Python"))  # False
```

## 6. Contar palabras
**Pregunta:** Escribe una función que cuente la frecuencia de cada palabra en una cadena de texto.

**Respuesta:**
```python
def contar_palabras(texto):
    palabras = texto.lower().split()
    conteo = {}
    for palabra in palabras:
        if palabra in conteo:
            conteo[palabra] += 1
        else:
            conteo[palabra] = 1
    return conteo

texto = "El perro persiguió al gato. El gato huyó del perro."
print(contar_palabras(texto))
# {'el': 2, 'perro': 2, 'persiguió': 1, 'al': 1, 'gato': 2, 'huyó': 1, 'del': 1}
```

## 7. Encontrar el mayor elemento
**Pregunta:** Crea una función que encuentre el elemento más grande en una lista de números.

**Respuesta:**
```python
def encontrar_mayor(lista):
    return max(lista)

print(encontrar_mayor([5, 2, 8, 1, 9]))  # 9
print(encontrar_mayor([-3, 0, 4, -1, 7]))  # 7
```

## 8. Invertir una lista
**Pregunta:** Escribe una función que invierta el orden de los elementos en una lista.

**Respuesta:**
```python
def invertir_lista(lista):
    return lista[::-1]

print(invertir_lista([1, 2, 3, 4, 5]))  # [5, 4, 3, 2, 1]
print(invertir_lista(["apple", "banana", "cherry"]))  # ['cherry', 'banana', 'apple']
```

## 9. Filtrar números pares
**Pregunta:** Crea una función que devuelva una nueva lista con solo los números pares de una lista dada.

**Respuesta:**
```python
def filtrar_pares(lista):
    return [num for num in lista if num % 2 == 0]

print(filtrar_pares([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))  # [2, 4, 6, 8, 10]
print(filtrar_pares([-2, 0, 1, 3, 5, 8]))  # [-2, 0, 8]
```

## 10. Encontrar el segundo mayor
**Pregunta:** Implementa una función que encuentre el segundo mayor elemento en una lista.

**Respuesta:**
```python
def encontrar_segundo_mayor(lista):
    if len(lista) < 2:
        return None
    lista.sort(reverse=True)
    return lista[1]

print(encontrar_segundo_mayor([5, 2, 8, 1, 9]))  # 8
print(encontrar_segundo_mayor([10, 5, 8, 12, 7]))  # 10
```

## 11. Contar vocales
**Pregunta:** Crea una función que cuente el número de vocales en una cadena de texto.

**Respuesta:**
```python
def contar_vocales(texto):
    vocales = "aeiou"
    cuenta = 0
    for letra in texto.lower():
        if letra in vocales:
            cuenta += 1
    return cuenta

print(contar_vocales("Hola, ¿cómo estás?"))  # 3
print(contar_vocales("Python es un lenguaje de programación excelente."))  # 12
```

## 12. Ordenar una lista de tuplas
**Pregunta:** Escribe una función que ordene una lista de tuplas por el segundo elemento de cada tupla.

**Respuesta:**
```python
def ordenar_tuplas(lista_tuplas):
    return sorted(lista_tuplas, key=lambda x: x[1])

print(ordenar_tuplas([(3, 2), (1, 3), (4, 1), (2, 4)]))
# [(4, 1), (3, 2), (1, 3), (2, 4)]
print(ordenar_tuplas([("apple", 4), ("banana", 2), ("cherry", 1)]))
# [('cherry', 1), ('banana', 2), ('apple', 4)]
```

## 13. Contar caracteres únicos
**Pregunta:** Crea una función que cuente el número de caracteres únicos en una cadena.

**Respuesta:**
```python
def contar_unicos(cadena):
    return len(set(cadena))

print(contar_unicos("hello"))  # 3
print(contar_unicos("Python"))  # 6
print(contar_unicos("aabbcc"))  # 3
```

## 14. Encontrar palabras más largas
**Pregunta:** Escribe una función que devuelva las N palabras más largas en una cadena de texto.

**Respuesta:**
```python
def palabras_mas_largas(texto, n):
    palabras = texto.split()
    palabras.sort(key=len, reverse=True)
    return palabras[:n]

print(palabras_mas_largas("El perro persiguió al gato", 2))
# ['persiguió', 'gato']
print(palabras_mas_largas("Python es un lenguaje de programación", 3))
# ['programación', 'lenguaje', 'Python']
```

## 15. Encontrar números primos
**Pregunta:** Implementa una función que genere los primeros N números primos.

**Respuesta:**
```python
def es_primo(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def primos_hasta(n):
    primos = []
    i = 2
    while len(primos) < n:
        if es_primo(i):
            primos.append(i)
        i += 1
    return primos

print(primos_hasta(5))  # [2, 3, 5, 7, 11]
print(primos_hasta(10))  # [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
```
