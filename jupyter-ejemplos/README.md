# Jupyter — ejemplos con pandas y matplotlib

Notebooks que usan pandas y matplotlib para medir y graficar comportamientos reales, en vez de solo describirlos en teoría.

## Instalación

```bash
# con uv (recomendado)
uv venv
uv pip install -r requirements.txt

# o con pip
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Correr Jupyter:

```bash
jupyter notebook
# o, si prefieres JupyterLab:
jupyter lab
```

## Notebooks

- [`complejidad_algoritmos/complejidad_algoritmos.ipynb`](complejidad_algoritmos/complejidad_algoritmos.ipynb) — mide en vivo el tiempo de ejecución de algoritmos de las 6 complejidades más comunes (O(1), O(log n), O(n), O(n log n), O(n²), O(2ⁿ)), guarda los resultados en `DataFrame`s de pandas, y grafica cada uno con matplotlib para confirmar visualmente que la curva coincide con la teoría (Estructura de Datos, 1.5 Análisis de algoritmos).

Todas las celdas de este notebook fueron **ejecutadas y verificadas** antes de publicarse (`jupyter nbconvert --execute`, 25/25 celdas sin error) — los patrones de tiempo medidos coinciden con lo esperado: O(1)/O(log n) se mantienen prácticamente planos incluso con n=10,000,000, mientras que O(n²) y O(2ⁿ) crecen dramáticamente incluso con n mucho más pequeño.
