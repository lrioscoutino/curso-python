"""
Tarea 1 — Clasificación de estructuras de datos (1.1)

Completa la función `clasificar()` para cada una de las 5 estructuras
listadas en `ESTRUCTURAS`. Debes devolver un diccionario con las 4
claves: "organizacion", "memoria", "homogeneidad", "nivel".

Valores válidos:
  organizacion:  "lineal" | "no_lineal"
  memoria:       "estatica" | "dinamica"
  homogeneidad:  "homogenea" | "heterogenea"
  nivel:         "fisica" | "logica"

Corre este archivo para ver si tus respuestas son correctas:
    python3 tarea_01_clasificacion.py
"""

ESTRUCTURAS = {
    "arreglo_calificaciones": "un array de tamaño fijo con 30 floats",
    "lista_enlazada_estudiantes": "nodos con referencia al siguiente, mismo tipo Estudiante",
    "arbol_genealogico": "nodos con distinto tipo de dato por campo, crece dinámicamente",
    "pila_de_llamadas": "estructura lineal que crece y decrece con cada llamada a función",
    "diccionario_configuracion": "clave-valor con acceso directo, tamaño variable",
}


def clasificar(nombre_estructura: str) -> dict:
    """TODO: completa la clasificación para cada estructura de ESTRUCTURAS."""
    # TODO: reemplaza este cuerpo. Ejemplo de retorno esperado:
    # return {"organizacion": "lineal", "memoria": "estatica",
    #         "homogeneidad": "homogenea", "nivel": "fisica"}
    raise NotImplementedError(f"Clasifica: {nombre_estructura}")


# --- No modifiques nada debajo de esta línea ---

_SOLUCION_ESPERADA = {
    "arreglo_calificaciones": {
        "organizacion": "lineal", "memoria": "estatica",
        "homogeneidad": "homogenea", "nivel": "fisica",
    },
    "lista_enlazada_estudiantes": {
        "organizacion": "lineal", "memoria": "dinamica",
        "homogeneidad": "homogenea", "nivel": "logica",
    },
    "arbol_genealogico": {
        "organizacion": "no_lineal", "memoria": "dinamica",
        "homogeneidad": "heterogenea", "nivel": "logica",
    },
    "pila_de_llamadas": {
        "organizacion": "lineal", "memoria": "dinamica",
        "homogeneidad": "homogenea", "nivel": "logica",
    },
    "diccionario_configuracion": {
        "organizacion": "no_lineal", "memoria": "dinamica",
        "homogeneidad": "heterogenea", "nivel": "logica",
    },
}


if __name__ == "__main__":
    aciertos = 0
    for nombre in ESTRUCTURAS:
        try:
            respuesta = clasificar(nombre)
        except NotImplementedError as e:
            print(f"[PENDIENTE] {e}")
            continue

        esperado = _SOLUCION_ESPERADA[nombre]
        if respuesta == esperado:
            print(f"[OK] {nombre}")
            aciertos += 1
        else:
            print(f"[FALLO] {nombre}: obtuviste {respuesta}, se esperaba {esperado}")

    print(f"\n{aciertos}/{len(ESTRUCTURAS)} correctas")
