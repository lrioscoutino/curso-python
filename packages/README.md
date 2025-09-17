# Tópicos Avanzados de Programación con Python
## Clase 2: Componentes y Librerías

---

## 2.1 Definición Conceptual de Componentes, Paquetes y Librerías

### ¿Qué son los Componentes?

Un **componente** en programación es una unidad de software reutilizable que encapsula funcionalidad específica y puede ser utilizada de manera independiente o como parte de un sistema más grande.

**Características principales:**
- **Reutilización:** Pueden ser utilizados en múltiples contextos
- **Encapsulación:** Ocultan su implementación interna
- **Interfaz definida:** Proporcionan métodos claros para interactuar con ellos
- **Independencia:** Funcionan de manera autónoma

### Paquetes vs Librerías vs Módulos

```python
# Módulo: Un archivo .py individual
# archivo: calculadora.py
def sumar(a, b):
    return a + b

def restar(a, b):
    return a - b
```

```python
# Paquete: Una carpeta que contiene múltiples módulos
# estructura de carpetas:
# matematicas/
#   ├── __init__.py
#   ├── aritmetica.py
#   ├── geometria.py
#   └── estadistica.py
```

**Diferencias clave:**

| Concepto | Definición | Ejemplo |
|----------|------------|---------|
| **Módulo** | Archivo individual .py | `math.py`, `datetime.py` |
| **Paquete** | Carpeta con módulos relacionados | `numpy`, `pandas` |
| **Librería** | Conjunto de paquetes y módulos | `matplotlib` (incluye pyplot, patches, etc.) |

### Ventajas de la Modularización

1. **Mantenibilidad:** Código más fácil de mantener y actualizar
2. **Reutilización:** Evita duplicación de código
3. **Colaboración:** Equipos pueden trabajar en componentes separados
4. **Testing:** Pruebas más específicas y efectivas
5. **Escalabilidad:** Sistemas más fáciles de extender

---

## 2.2 Uso de Librerías Proporcionadas por el Lenguaje

### Librería Estándar de Python

Python incluye una extensa librería estándar. Exploremos las más importantes:

#### 2.2.1 Módulos Fundamentales

```python
# os - Interacción con el sistema operativo
import os

# Obtener directorio actual
directorio_actual = os.getcwd()
print(f"Directorio actual: {directorio_actual}")

# Listar archivos
archivos = os.listdir('.')
print(f"Archivos: {archivos}")

# Crear directorio
os.makedirs('nuevo_directorio', exist_ok=True)
```

```python
# sys - Información del sistema y intérprete
import sys

print(f"Versión de Python: {sys.version}")
print(f"Plataforma: {sys.platform}")
print(f"Argumentos de línea de comandos: {sys.argv}")

# Agregar rutas al PATH de Python
sys.path.append('/ruta/personalizada')
```

#### 2.2.2 Manejo de Fechas y Tiempo

```python
from datetime import datetime, timedelta, date
import time

# Fecha y hora actual
ahora = datetime.now()
print(f"Ahora: {ahora}")

# Formateo de fechas
fecha_formateada = ahora.strftime("%d/%m/%Y %H:%M:%S")
print(f"Fecha formateada: {fecha_formateada}")

# Operaciones con fechas
mañana = ahora + timedelta(days=1)
hace_una_semana = ahora - timedelta(weeks=1)

# Medición de tiempo de ejecución
inicio = time.time()
# ... código a medir ...
fin = time.time()
tiempo_ejecucion = fin - inicio
```

#### 2.2.3 Expresiones Regulares

```python
import re

# Patrón para validar email
patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def validar_email(email):
    return re.match(patron_email, email) is not None

# Búsqueda y reemplazo
texto = "Mi teléfono es 555-1234 y mi móvil es 555-5678"
telefonos = re.findall(r'\d{3}-\d{4}', texto)
print(f"Teléfonos encontrados: {telefonos}")

# Reemplazo
texto_censurado = re.sub(r'\d{3}-\d{4}', 'XXX-XXXX', texto)
```

#### 2.2.4 Manejo de JSON

```python
import json

# Datos de ejemplo
datos = {
    "nombre": "Juan Pérez",
    "edad": 30,
    "activo": True,
    "habilidades": ["Python", "JavaScript", "SQL"]
}

# Convertir a JSON
json_string = json.dumps(datos, indent=2, ensure_ascii=False)
print(json_string)

# Leer desde JSON
datos_recuperados = json.loads(json_string)

# Guardar en archivo
with open('datos.json', 'w', encoding='utf-8') as archivo:
    json.dump(datos, archivo, indent=2, ensure_ascii=False)

# Leer desde archivo
with open('datos.json', 'r', encoding='utf-8') as archivo:
    datos_del_archivo = json.load(archivo)
```

#### 2.2.5 Colecciones Especializadas

```python
from collections import defaultdict, Counter, namedtuple, deque

# defaultdict - diccionario con valores por defecto
grupos = defaultdict(list)
personas = [
    ("Juan", "Ingeniería"),
    ("María", "Medicina"),
    ("Carlos", "Ingeniería"),
    ("Ana", "Medicina")
]

for nombre, carrera in personas:
    grupos[carrera].append(nombre)

print(dict(grupos))  # {'Ingeniería': ['Juan', 'Carlos'], 'Medicina': ['María', 'Ana']}

# Counter - contador de elementos
palabras = "python es genial python es poderoso".split()
contador = Counter(palabras)
print(contador.most_common(2))  # [('python', 2), ('es', 2)]

# namedtuple - tupla con nombres
Persona = namedtuple('Persona', ['nombre', 'edad', 'ciudad'])
persona1 = Persona("Juan", 25, "Madrid")
print(f"{persona1.nombre} tiene {persona1.edad} años")

# deque - cola de doble extremo
cola = deque(['a', 'b', 'c'])
cola.appendleft('z')  # Agregar al inicio
cola.append('d')      # Agregar al final
print(cola)  # deque(['z', 'a', 'b', 'c', 'd'])
```

---

## 2.3 Creación de Componentes Definidos por el Usuario

### 2.3.1 Componentes No Visuales

#### Ejemplo 1: Sistema de Gestión de Usuarios

```python
# archivo: usuario_manager.py
from datetime import datetime
from typing import List, Optional
import json

class Usuario:
    """Componente que representa un usuario del sistema."""
    
    def __init__(self, id_usuario: int, nombre: str, email: str):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.fecha_creacion = datetime.now()
        self.activo = True
        self.ultimo_acceso = None
    
    def activar(self):
        """Activa el usuario."""
        self.activo = True
    
    def desactivar(self):
        """Desactiva el usuario."""
        self.activo = False
    
    def registrar_acceso(self):
        """Registra el último acceso del usuario."""
        self.ultimo_acceso = datetime.now()
    
    def to_dict(self) -> dict:
        """Convierte el usuario a diccionario para serialización."""
        return {
            'id_usuario': self.id_usuario,
            'nombre': self.nombre,
            'email': self.email,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'activo': self.activo,
            'ultimo_acceso': self.ultimo_acceso.isoformat() if self.ultimo_acceso else None
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un usuario desde un diccionario."""
        usuario = cls(data['id_usuario'], data['nombre'], data['email'])
        usuario.fecha_creacion = datetime.fromisoformat(data['fecha_creacion'])
        usuario.activo = data['activo']
        if data['ultimo_acceso']:
            usuario.ultimo_acceso = datetime.fromisoformat(data['ultimo_acceso'])
        return usuario
    
    def __str__(self):
        return f"Usuario({self.id_usuario}, {self.nombre}, {self.email})"

class GestorUsuarios:
    """Componente para gestionar múltiples usuarios."""
    
    def __init__(self):
        self.usuarios: dict[int, Usuario] = {}
        self.proximo_id = 1
    
    def crear_usuario(self, nombre: str, email: str) -> Usuario:
        """Crea un nuevo usuario."""
        if self.buscar_por_email(email):
            raise ValueError(f"Ya existe un usuario con el email {email}")
        
        usuario = Usuario(self.proximo_id, nombre, email)
        self.usuarios[self.proximo_id] = usuario
        self.proximo_id += 1
        return usuario
    
    def obtener_usuario(self, id_usuario: int) -> Optional[Usuario]:
        """Obtiene un usuario por su ID."""
        return self.usuarios.get(id_usuario)
    
    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        """Busca un usuario por su email."""
        for usuario in self.usuarios.values():
            if usuario.email == email:
                return usuario
        return None
    
    def listar_usuarios_activos(self) -> List[Usuario]:
        """Lista todos los usuarios activos."""
        return [u for u in self.usuarios.values() if u.activo]
    
    def eliminar_usuario(self, id_usuario: int) -> bool:
        """Elimina un usuario del sistema."""
        if id_usuario in self.usuarios:
            del self.usuarios[id_usuario]
            return True
        return False
    
    def guardar_en_archivo(self, nombre_archivo: str):
        """Guarda todos los usuarios en un archivo JSON."""
        datos = {
            'usuarios': [u.to_dict() for u in self.usuarios.values()],
            'proximo_id': self.proximo_id
        }
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, indent=2, ensure_ascii=False)
    
    def cargar_desde_archivo(self, nombre_archivo: str):
        """Carga usuarios desde un archivo JSON."""
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
                
            self.usuarios.clear()
            for usuario_data in datos['usuarios']:
                usuario = Usuario.from_dict(usuario_data)
                self.usuarios[usuario.id_usuario] = usuario
            
            self.proximo_id = datos['proximo_id']
        except FileNotFoundError:
            print(f"Archivo {nombre_archivo} no encontrado. Iniciando con lista vacía.")
```

#### Ejemplo 2: Sistema de Cache

```python
# archivo: cache_manager.py
from typing import Any, Optional
from datetime import datetime, timedelta
import threading
from collections import OrderedDict

class CacheItem:
    """Elemento individual del cache."""
    
    def __init__(self, value: Any, ttl_seconds: Optional[int] = None):
        self.value = value
        self.created_at = datetime.now()
        self.expires_at = None
        if ttl_seconds:
            self.expires_at = self.created_at + timedelta(seconds=ttl_seconds)
    
    def is_expired(self) -> bool:
        """Verifica si el elemento ha expirado."""
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at

class CacheManager:
    """Gestor de cache thread-safe con TTL y límite de tamaño."""
    
    def __init__(self, max_size: int = 1000, default_ttl: Optional[int] = None):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache = OrderedDict()
        self._lock = threading.RLock()
        self._hits = 0
        self._misses = 0
    
    def get(self, key: str) -> Optional[Any]:
        """Obtiene un valor del cache."""
        with self._lock:
            if key not in self._cache:
                self._misses += 1
                return None
            
            item = self._cache[key]
            
            # Verificar expiración
            if item.is_expired():
                del self._cache[key]
                self._misses += 1
                return None
            
            # Mover al final (LRU)
            self._cache.move_to_end(key)
            self._hits += 1
            return item.value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Establece un valor en el cache."""
        with self._lock:
            # Usar TTL específico o por defecto
            ttl_to_use = ttl if ttl is not None else self.default_ttl
            
            # Crear nuevo item
            item = CacheItem(value, ttl_to_use)
            
            # Si la clave ya existe, actualizarla
            if key in self._cache:
                self._cache[key] = item
                self._cache.move_to_end(key)
                return
            
            # Si el cache está lleno, remover el más antiguo
            if len(self._cache) >= self.max_size:
                self._cache.popitem(last=False)  # Remover el primero (más antiguo)
            
            self._cache[key] = item
    
    def delete(self, key: str) -> bool:
        """Elimina una clave del cache."""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
    
    def clear(self) -> None:
        """Limpia todo el cache."""
        with self._lock:
            self._cache.clear()
    
    def size(self) -> int:
        """Retorna el tamaño actual del cache."""
        with self._lock:
            return len(self._cache)
    
    def get_stats(self) -> dict:
        """Obtiene estadísticas del cache."""
        with self._lock:
            total_requests = self._hits + self._misses
            hit_rate = (self._hits / total_requests * 100) if total_requests > 0 else 0
            
            return {
                'hits': self._hits,
                'misses': self._misses,
                'total_requests': total_requests,
                'hit_rate_percent': round(hit_rate, 2),
                'current_size': len(self._cache),
                'max_size': self.max_size
            }
    
    def cleanup_expired(self) -> int:
        """Limpia elementos expirados y retorna la cantidad eliminada."""
        with self._lock:
            expired_keys = []
            for key, item in self._cache.items():
                if item.is_expired():
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self._cache[key]
            
            return len(expired_keys)
```


---

## 2.4 Creación y Uso de Paquetes/Librerías Definidas por el Usuario

### 2.4.1 Estructura de un Paquete

Crear un paquete propio requiere una estructura específica de directorios:

```
mi_libreria/
├── __init__.py
├── setup.py
├── README.md
├── requirements.txt
├── mi_libreria/
│   ├── __init__.py
│   ├── utilidades/
│   │   ├── __init__.py
│   │   ├── matematicas.py
│   │   └── texto.py
│   ├── datos/
│   │   ├── __init__.py
│   │   ├── procesador.py
│   │   └── validador.py
│   └── visualizacion/
│       ├── __init__.py
│       ├── graficos.py
│       └── reportes.py
└── tests/
    ├── __init__.py
    ├── test_utilidades.py
    ├── test_datos.py
    └── test_visualizacion.py
```

### 2.4.2 Implementación del Paquete

#### archivo: mi_libreria/__init__.py

```python
"""
Mi Librería Personal - Herramientas de Desarrollo
================================================

Una librería completa con utilidades para desarrollo en Python.

Módulos disponibles:
- utilidades: Funciones matemáticas y de texto
- datos: Procesamiento y validación de datos
- visualizacion: Gráficos y reportes
"""

__version__ = "1.0.0"
__author__ = "Tu Nombre"
__email__ = "tu.email@universidad.edu"

# Importaciones principales para acceso directo
from .utilidades.matematicas import (
    factorial, fibonacci, es_primo, calcular_estadisticas
)
from .utilidades.texto import (
    limpiar_texto, extraer_numeros, capitalizar_palabras
)
from .datos.procesador import ProcesadorDatos
from .datos.validador import ValidadorDatos
from .visualizacion.graficos import GraficadorAvanzado

# Lista de componentes públicos
__all__ = [
    'factorial', 'fibonacci', 'es_primo', 'calcular_estadisticas',
    'limpiar_texto', 'extraer_numeros', 'capitalizar_palabras',
    'ProcesadorDatos', 'ValidadorDatos', 'GraficadorAvanzado'
]

def info():
    """Muestra información sobre la librería."""
    print(f"""
    Mi Librería Personal v{__version__}
    {'='*40}
    Autor: {__author__}
    Email: {__email__}
    
    Módulos disponibles:
    - utilidades.matematicas: Funciones matemáticas
    - utilidades.texto: Procesamiento de texto
    - datos.procesador: Procesamiento de datos
    - datos.validador: Validación de datos
    - visualizacion.graficos: Gráficos avanzados
    
    Uso: import mi_libreria
    """)
```

#### archivo: mi_libreria/utilidades/matematicas.py

```python
"""Módulo de utilidades matemáticas."""

import math
from typing import List, Dict, Union
from functools import lru_cache

@lru_cache(maxsize=128)
def factorial(n: int) -> int:
    """
    Calcula el factorial de un número.
    
    Args:
        n: Número entero no negativo
        
    Returns:
        Factorial de n
        
    Raises:
        ValueError: Si n es negativo
    """
    if n < 0:
        raise ValueError("El factorial no está definido para números negativos")
    if n <= 1:
        return 1
    return n * factorial(n - 1)

@lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    """
    Calcula el n-ésimo número de Fibonacci.
    
    Args:
        n: Posición en la secuencia (0-indexada)
        
    Returns:
        El n-ésimo número de Fibonacci
    """
    if n < 0:
        raise ValueError("n debe ser no negativo")
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def es_primo(n: int) -> bool:
    """
    Verifica si un número es primo.
    
    Args:
        n: Número a verificar
        
    Returns:
        True si es primo, False en caso contrario
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    # Verificar divisores impares hasta sqrt(n)
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def calcular_estadisticas(datos: List[Union[int, float]]) -> Dict[str, float]:
    """
    Calcula estadísticas descriptivas de una lista de números.
    
    Args:
        datos: Lista de números
        
    Returns:
        Diccionario con estadísticas (media, mediana, moda, desviación estándar)
    """
    if not datos:
        raise ValueError("La lista no puede estar vacía")
    
    datos_ordenados = sorted(datos)
    n = len(datos)
    
    # Media
    media = sum(datos) / n
    
    # Mediana
    if n % 2 == 0:
        mediana = (datos_ordenados[n//2 - 1] + datos_ordenados[n//2]) / 2
    else:
        mediana = datos_ordenados[n//2]
    
    # Moda (valor más frecuente)
    from collections import Counter
    contador = Counter(datos)
    moda = contador.most_common(1)[0][0]
    
    # Desviación estándar
    varianza = sum((x - media) ** 2 for x in datos) / n
    desviacion_estandar = math.sqrt(varianza)
    
    return {
        'media': round(media, 4),
        'mediana': mediana,
        'moda': moda,
        'desviacion_estandar': round(desviacion_estandar, 4),
        'varianza': round(varianza, 4),
        'minimo': min(datos),
        'maximo': max(datos),
        'rango': max(datos) - min(datos)
    }

def generar_primos(limite: int) -> List[int]:
    """
    Genera todos los números primos hasta un límite usando la Criba de Eratóstenes.
    
    Args:
        limite: Número límite (inclusive)
        
    Returns:
        Lista de números primos
    """
    if limite < 2:
        return []
    
    # Criba de Eratóstenes
    es_primo_array = [True] * (limite + 1)
    es_primo_array[0] = es_primo_array[1] = False
    
    for i in range(2, int(math.sqrt(limite)) + 1):
        if es_primo_array[i]:
            for j in range(i*i, limite + 1, i):
                es_primo_array[j] = False
    
    return [i for i in range(2, limite + 1) if es_primo_array[i]]
```

#### archivo: mi_libreria/utilidades/texto.py

```python
"""Módulo de utilidades para procesamiento de texto."""

import re
import string
from typing import List, Dict
from collections import Counter

def limpiar_texto(texto: str, mantener_numeros: bool = True, 
                 mantener_espacios: bool = True) -> str:
    """
    Limpia un texto removiendo caracteres especiales.
    
    Args:
        texto: Texto a limpiar
        mantener_numeros: Si mantener números
        mantener_espacios: Si mantener espacios
        
    Returns:
        Texto limpio
    """
    if not texto:
        return ""
    
    # Convertir a minúsculas
    texto = texto.lower()
    
    # Definir caracteres permitidos
    caracteres_permitidos = string.ascii_lowercase
    if mantener_numeros:
        caracteres_permitidos += string.digits
    if mantener_espacios:
        caracteres_permitidos += ' '
    
    # Filtrar caracteres
    texto_limpio = ''.join(c for c in texto if c in caracteres_permitidos)
    
    # Limpiar espacios múltiples
    if mantener_espacios:
        texto_limpio = re.sub(r'\s+', ' ', texto_limpio).strip()
    
    return texto_limpio

def extraer_numeros(texto: str) -> List[float]:
    """
    Extrae todos los números de un texto.
    
    Args:
        texto: Texto del cual extraer números
        
    Returns:
        Lista de números encontrados
    """
    patron = r'-?\d+\.?\d*'
    numeros_str = re.findall(patron, texto)
    return [float(num) for num in numeros_str if num]

def capitalizar_palabras(texto: str, excepciones: List[str] = None) -> str:
    """
    Capitaliza las palabras de un texto, excepto las especificadas.
    
    Args:
        texto: Texto a capitalizar
        excepciones: Lista de palabras que no se deben capitalizar
        
    Returns:
        Texto con palabras capitalizadas
    """
    if not texto:
        return ""
    
    if excepciones is None:
        excepciones = ['y', 'o', 'de', 'del', 'la', 'el', 'los', 'las', 'en', 'con']
    
    palabras = texto.split()
    palabras_capitalizadas = []
    
    for i, palabra in enumerate(palabras):
        # Primera palabra siempre se capitaliza
        if i == 0 or palabra.lower() not in excepciones:
            palabras_capitalizadas.append(palabra.capitalize())
        else:
            palabras_capitalizadas.append(palabra.lower())
    
    return ' '.join(palabras_capitalizadas)

def contar_palabras(texto: str) -> Dict[str, int]:
    """
    Cuenta la frecuencia de palabras en un texto.
    
    Args:
        texto: Texto a analizar
        
    Returns:
        Diccionario con el conteo de palabras
    """
    texto_limpio = limpiar_texto(texto, mantener_numeros=False)
    palabras = texto_limpio.split()
    return dict(Counter(palabras))

def generar_resumen(texto: str, num_oraciones: int = 3) -> str:
    """
    Genera un resumen simple del texto basado en frecuencia de palabras.
    
    Args:
        texto: Texto a resumir
        num_oraciones: Número de oraciones en el resumen
        
    Returns:
        Resumen del texto
    """
    if not texto:
        return ""
    
    # Dividir en oraciones
    oraciones = re.split(r'[.!?]+', texto)
    oraciones = [o.strip() for o in oraciones if o.strip()]
    
    if len(oraciones) <= num_oraciones:
        return texto
    
    # Contar palabras importantes (más de 3 caracteres)
    todas_palabras = []
    for oracion in oraciones:
        palabras = limpiar_texto(oracion, mantener_numeros=False).split()
        todas_palabras.extend([p for p in palabras if len(p) > 3])
    
    frecuencias = Counter(todas_palabras)
    
    # Puntuar oraciones basado en palabras importantes
    puntuaciones = []
    for oracion in oraciones:
        palabras = limpiar_texto(oracion, mantener_numeros=False).split()
        puntuacion = sum(frecuencias.get(p, 0) for p in palabras if len(p) > 3)
        puntuaciones.append((puntuacion, oracion))
    
    # Seleccionar las mejores oraciones
    puntuaciones.sort(reverse=True)
    mejores_oraciones = [oracion for _, oracion in puntuaciones[:num_oraciones]]
    
    return '. '.join(mejores_oraciones) + '.'
```

#### archivo: mi_libreria/datos/procesador.py

```python
"""Módulo para procesamiento de datos."""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Union
import json

class ProcesadorDatos:
    """Clase para procesamiento avanzado de datos."""
    
    def __init__(self):
        self.historial_operaciones = []
    
    def cargar_csv(self, archivo: str, **kwargs) -> pd.DataFrame:
        """
        Carga datos desde un archivo CSV.
        
        Args:
            archivo: Ruta del archivo CSV
            **kwargs: Argumentos adicionales para pandas.read_csv
            
        Returns:
            DataFrame con los datos
        """
        try:
            df = pd.read_csv(archivo, **kwargs)
            self.historial_operaciones.append(f"Cargado CSV: {archivo}")
            return df
        except Exception as e:
            raise ValueError(f"Error al cargar CSV: {str(e)}")
    
    def limpiar_datos(self, df: pd.DataFrame, 
                     eliminar_duplicados: bool = True,
                     llenar_nulos: Union[str, Dict] = 'mean') -> pd.DataFrame:
        """
        Limpia un DataFrame eliminando duplicados y tratando valores nulos.
        
        Args:
            df: DataFrame a limpiar
            eliminar_duplicados: Si eliminar filas duplicadas
            llenar_nulos: Estrategia para llenar nulos ('mean', 'median', 'mode', 0, dict)
            
        Returns:
            DataFrame limpio
        """
        df_limpio = df.copy()
        
        # Eliminar duplicados
        if eliminar_duplicados:
            antes = len(df_limpio)
            df_limpio = df_limpio.drop_duplicates()
            despues = len(df_limpio)
            self.historial_operaciones.append(f"Eliminados {antes - despues} duplicados")
        
        # Tratar valores nulos
        if llenar_nulos is not None:
            if isinstance(llenar_nulos, str):
                if llenar_nulos == 'mean':
                    # Llenar con la media (solo columnas numéricas)
                    numericas = df_limpio.select_dtypes(include=[np.number]).columns
                    df_limpio[numericas] = df_limpio[numericas].fillna(df_limpio[numericas].mean())
                elif llenar_nulos == 'median':
                    numericas = df_limpio.select_dtypes(include=[np.number]).columns
                    df_limpio[numericas] = df_limpio[numericas].fillna(df_limpio[numericas].median())
                elif llenar_nulos == 'mode':
                    for col in df_limpio.columns:
                        if df_limpio[col].isnull().any():
                            moda = df_limpio[col].mode()
                            if not moda.empty:
                                df_limpio[col].fillna(moda[0], inplace=True)
            elif isinstance(llenar_nulos, dict):
                df_limpio = df_limpio.fillna(llenar_nulos)
            else:
                df_limpio = df_limpio.fillna(llenar_nulos)
            
            self.historial_operaciones.append(f"Valores nulos tratados con: {llenar_nulos}")
        
        return df_limpio
    
    def detectar_outliers(self, df: pd.DataFrame, columna: str, 
                         metodo: str = 'iqr') -> List[int]:
        """
        Detecta outliers en una columna específica.
        
        Args:
            df: DataFrame
            columna: Nombre de la columna
            metodo: Método de detección ('iqr', 'zscore')
            
        Returns:
            Lista de índices de outliers
        """
        if columna not in df.columns:
            raise ValueError(f"Columna '{columna}' no encontrada")
        
        datos = df[columna].dropna()
        outliers = []
        
        if metodo == 'iqr':
            Q1 = datos.quantile(0.25)
            Q3 = datos.quantile(0.75)
            IQR = Q3 - Q1
            limite_inferior = Q1 - 1.5 * IQR
            limite_superior = Q3 + 1.5 * IQR
            outliers = df[(df[columna] < limite_inferior) | 
                         (df[columna] > limite_superior)].index.tolist()
        
        elif metodo == 'zscore':
            from scipy import stats
            z_scores = np.abs(stats.zscore(datos))
            threshold = 3
            outliers = df[np.abs(stats.zscore(df[columna].fillna(datos.mean()))) > threshold].index.tolist()
        
        self.historial_operaciones.append(f"Detectados {len(outliers)} outliers en '{columna}' usando {metodo}")
        return outliers
    
    def agrupar_datos(self, df: pd.DataFrame, por: Union[str, List[str]], 
                     agregaciones: Dict[str, Union[str, List[str]]]) -> pd.DataFrame:
        """
        Agrupa datos y aplica funciones de agregación.
        
        Args:
            df: DataFrame
            por: Columna(s) para agrupar
            agregaciones: Diccionario de columna -> función(es) de agregación
            
        Returns:
            DataFrame agrupado
        """
        try:
            resultado = df.groupby(por).agg(agregaciones)
            self.historial_operaciones.append(f"Agrupado por {por} con agregaciones {agregaciones}")
            return resultado
        except Exception as e:
            raise ValueError(f"Error en agrupación: {str(e)}")
    
    def normalizar_datos(self, df: pd.DataFrame, columnas: Optional[List[str]] = None,
                        metodo: str = 'minmax') -> pd.DataFrame:
        """
        Normaliza datos numéricos.
        
        Args:
            df: DataFrame
            columnas: Columnas a normalizar (None para todas las numéricas)
            metodo: Método de normalización ('minmax', 'zscore')
            
        Returns:
            DataFrame normalizado
        """
        df_norm = df.copy()
        
        if columnas is None:
            columnas = df_norm.select_dtypes(include=[np.number]).columns.tolist()
        
        from sklearn.preprocessing import MinMaxScaler, StandardScaler
        
        if metodo == 'minmax':
            scaler = MinMaxScaler()
        elif metodo == 'zscore':
            scaler = StandardScaler()
        else:
            raise ValueError("Método debe ser 'minmax' o 'zscore'")
        
        df_norm[columnas] = scaler.fit_transform(df_norm[columnas])
        self.historial_operaciones.append(f"Normalizado columnas {columnas} con {metodo}")
        
        return df_norm
    
    def obtener_resumen(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Obtiene un resumen completo del DataFrame.
        
        Args:
            df: DataFrame a resumir
            
        Returns:
            Diccionario con información del resumen
        """
        resumen = {
            'forma': df.shape,
            'columnas': df.columns.tolist(),
            'tipos_datos': df.dtypes.to_dict(),
            'valores_nulos': df.isnull().sum().to_dict(),
            'memoria_mb': round(df.memory_usage(deep=True).sum() / 1024**2, 2),
            'estadisticas_numericas': df.describe().to_dict() if not df.select_dtypes(include=[np.number]).empty else {},
            'valores_unicos': {col: df[col].nunique() for col in df.columns}
        }
        
        return resumen
    
    def exportar_datos(self, df: pd.DataFrame, archivo: str, formato: str = 'csv'):
        """
        Exporta DataFrame a diferentes formatos.
        
        Args:
            df: DataFrame a exportar
            archivo: Nombre del archivo
            formato: Formato de exportación ('csv', 'excel', 'json')
        """
        try:
            if formato == 'csv':
                df.to_csv(archivo, index=False)
            elif formato == 'excel':
                df.to_excel(archivo, index=False)
            elif formato == 'json':
                df.to_json(archivo, orient='records', indent=2)
            else:
                raise ValueError("Formato debe ser 'csv', 'excel' o 'json'")
            
            self.historial_operaciones.append(f"Exportado a {archivo} en formato {formato}")
        except Exception as e:
            raise ValueError(f"Error al exportar: {str(e)}")
    
    def obtener_historial(self) -> List[str]:
        """Retorna el historial de operaciones realizadas."""
        return self.historial_operaciones.copy()
    
    def limpiar_historial(self):
        """Limpia el historial de operaciones."""
        self.historial_operaciones.clear()
```

#### archivo: setup.py

```python
"""Configuración para instalación del paquete."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="mi-libreria-personal",
    version="1.0.0",
    author="Tu Nombre",
    author_email="tu.email@universidad.edu",
    description="Una librería completa con utilidades para desarrollo en Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tu-usuario/mi-libreria",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=0.5",
        ],
    },
    entry_points={
        "console_scripts": [
            "mi-libreria=mi_libreria.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
```


## Recursos Adicionales

### Librerías Recomendadas para Estudio

1. **Ciencia de Datos:**
   - pandas: Manipulación de datos
   - numpy: Computación numérica
   - matplotlib/seaborn: Visualización
   - scikit-learn: Machine Learning

2. **Desarrollo Web:**
   - Flask/Django: Frameworks web
   - requests: Cliente HTTP
   - Beautiful Soup: Web scraping

3. **Utilidades:**
   - click: Interfaces de línea de comandos
   - pytest: Testing
   - logging: Sistema de logs

### Mejores Prácticas

1. **Nomenclatura:**
   - Usar nombres descriptivos y consistentes
   - Seguir PEP 8 para convenciones de estilo
   - Documentar funciones con docstrings

2. **Estructura:**
   - Separar responsabilidades en módulos diferentes
   - Crear interfaces claras entre componentes
   - Minimizar dependencias

3. **Testing:**
   - Escribir pruebas unitarias para cada componente
   - Usar mocks para dependencias externas
   - Mantener cobertura de pruebas alta

4. **Documentación:**
   - README claro con ejemplos de uso
   - Documentación de API con Sphinx
   - Changelog para versiones

---

## Tareas para Casa

### Tarea 1: Análisis de Librería (Individual)
Selecciona una librería popular de Python (requests, pandas, matplotlib, etc.) y realiza:
1. Análisis de su estructura de paquetes
2. Identificación de componentes principales
3. Estudio de patrones de diseño utilizados
4. Documento de 3-4 páginas con findings

Preparar una presentación de 15 minutos sobre su librería:
1. Demostración de funcionalidades
2. Decisiones de diseño
3. Retos enfrentados
4. Demo en vivo

---

## Ejercicios de Laboratorio

### Lab 1: Exploración de Librerías Estándar (30 min)

```python
# Ejercicio 1: Usar os y sys para información del sistema
import os
import sys

def info_sistema():
    """Recopila información del sistema."""
    # TODO: Implementar función que retorne diccionario con:
    # - Sistema operativo
    # - Versión de Python
    # - Directorio actual
    # - Variables de entorno importantes
    pass

# Ejercicio 2: Procesamiento de fechas
from datetime import datetime, timedelta

def calcular_edad_dias(fecha_nacimiento: str):
    """Calcula edad en días desde fecha de nacimiento."""
    # TODO: Implementar cálculo de edad en días
    # Formato fecha: "YYYY-MM-DD"
    pass

def proximo_cumpleanos(fecha_nacimiento: str):
    """Calcula días hasta el próximo cumpleaños."""
    # TODO: Implementar cálculo
    pass
```

### Lab 2: Componente de Configuración (45 min)

```python
# config_manager.py
import json
import os
from typing import Any, Dict, Optional

class ConfigManager:
    """Gestor de configuración para aplicaciones."""
    
    def __init__(self, archivo_config: str = "config.json"):
        # TODO: Implementar inicialización
        pass
    
    def get(self, clave: str, default: Any = None) -> Any:
        """Obtiene valor de configuración."""
        # TODO: Implementar con soporte para claves anidadas (ej: "db.host")
        pass
    
    def set(self, clave: str, valor: Any) -> None:
        """Establece valor de configuración."""
        # TODO: Implementar
        pass
    
    def save(self) -> None:
        """Guarda configuración en archivo."""
        # TODO: Implementar
        pass
    
    def load_from_env(self, mapeo: Dict[str, str]) -> None:
        """Carga configuración desde variables de entorno."""
        # TODO: Implementar
        # mapeo: {"DATABASE_URL": "db.url"}
        pass
```

### Lab 3: Visualizador de Datos Simple (60 min)

```python
# visualizador_simple.py
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Tuple

class VisualizadorDatos:
    """Componente para visualización simple de datos."""
    
    def __init__(self, estilo: str = "seaborn"):
        # TODO: Configurar matplotlib
        pass
    
    def grafico_barras(self, datos: Dict[str, float], titulo: str = ""):
        """Crea gráfico de barras."""
        # TODO: Implementar con personalización de colores
        pass
    
    def grafico_lineas(self, x: List, y: List, titulo: str = ""):
        """Crea gráfico de líneas."""
        # TODO: Implementar
        pass
    
    def histograma(self, datos: List[float], bins: int = 20):
        """Crea histograma."""
        # TODO: Implementar
        pass
    
    def guardar_figura(self, nombre: str):
        """Guarda la figura actual."""
        # TODO: Implementar
        pass

# Datos de prueba
ventas_mensuales = {
    "Enero": 15000, "Febrero": 18000, "Marzo": 22000,
    "Abril": 19000, "Mayo": 25000, "Junio": 28000
}

temperaturas = [23, 25, 27, 24, 22, 26, 28, 30, 29, 27, 25, 24]
```

---
