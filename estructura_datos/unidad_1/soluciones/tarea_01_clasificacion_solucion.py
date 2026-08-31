"""Solución de referencia — Tarea 1: Clasificación de estructuras de datos."""

ESTRUCTURAS = {
    "arreglo_calificaciones": "un array de tamaño fijo con 30 floats",
    "lista_enlazada_estudiantes": "nodos con referencia al siguiente, mismo tipo Estudiante",
    "arbol_genealogico": "nodos con distinto tipo de dato por campo, crece dinámicamente",
    "pila_de_llamadas": "estructura lineal que crece y decrece con cada llamada a función",
    "diccionario_configuracion": "clave-valor con acceso directo, tamaño variable",
}


def clasificar(nombre_estructura: str) -> dict:
    tabla = {
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
    return tabla[nombre_estructura]


if __name__ == "__main__":
    for nombre in ESTRUCTURAS:
        print(nombre, "->", clasificar(nombre))
