"""
1.2-1.3 — TDA Diccionario / Mapa

Caso de uso: contar cuántas veces aparece cada palabra en un texto.
Se necesita acceso casi instantáneo a "¿cuántas veces ha aparecido
esta palabra?" sin recorrer todo desde cero cada vez.
"""


def contar_palabras(texto: str) -> dict:
    frecuencia = {}
    for palabra in texto.lower().split():
        frecuencia[palabra] = frecuencia.get(palabra, 0) + 1   # O(1) promedio
    return frecuencia


def palabra_mas_frecuente(frecuencia: dict):
    return max(frecuencia, key=frecuencia.get)


if __name__ == "__main__":
    texto = "el perro corre el perro ladra y el gato duerme"
    frecuencia = contar_palabras(texto)

    print("Frecuencia:", frecuencia)
    print("Más frecuente:", palabra_mas_frecuente(frecuencia))

    print("\n--- Otro caso: caché de resultados (memoización) ---")

    cache_fibonacci = {}

    def fibonacci(n):
        if n in cache_fibonacci:
            return cache_fibonacci[n]
        if n <= 1:
            resultado = n
        else:
            resultado = fibonacci(n - 1) + fibonacci(n - 2)
        cache_fibonacci[n] = resultado
        return resultado

    for i in range(10):
        print(f"fib({i}) = {fibonacci(i)}")
