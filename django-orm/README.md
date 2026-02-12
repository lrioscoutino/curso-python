# Manual Teorico-Practico: Django ORM

## Tabla de Contenidos

1. [Fundamentos Teoricos del ORM](#1-fundamentos-teoricos-del-orm)
2. [Instalacion del Entorno con uv](#2-instalacion-del-entorno-con-uv)
3. [Creacion del Proyecto Django](#3-creacion-del-proyecto-django)
4. [Creacion de la App y el Modelo Estudiantes](#4-creacion-de-la-app-y-el-modelo-estudiantes)
5. [Migraciones: De Python a SQL](#5-migraciones-de-python-a-sql)
6. [Operaciones CRUD con el ORM](#6-operaciones-crud-con-el-orm)
7. [Consultas Avanzadas](#7-consultas-avanzadas)
8. [Relaciones entre Modelos](#8-relaciones-entre-modelos)
9. [Ejercicios Practicos](#9-ejercicios-practicos)

---

## 1. Fundamentos Teoricos del ORM

### Que es un ORM?

**ORM** (Object-Relational Mapping) es una tecnica de programacion que permite interactuar con una base de datos relacional usando objetos de un lenguaje de programacion, en lugar de escribir SQL directamente.

### El Problema que Resuelve

Sin ORM, para obtener estudiantes de una base de datos escribirias:

```sql
SELECT * FROM estudiantes WHERE edad >= 18 ORDER BY nombre;
```

Con el ORM de Django, escribes:

```python
Estudiante.objects.filter(edad__gte=18).order_by("nombre")
```

### Como Funciona Internamente

```
Tu Codigo Python  --->  ORM de Django  --->  SQL  --->  Base de Datos
     (objetos)        (traduccion)       (consulta)     (tablas/filas)
```

El ORM actua como un **traductor bidireccional**:

| Concepto Python | Concepto en Base de Datos |
|-----------------|--------------------------|
| Clase           | Tabla                     |
| Atributo        | Columna                   |
| Instancia       | Fila (registro)           |
| QuerySet        | Consulta SQL              |

### Ventajas del ORM

1. **Abstraccion**: No necesitas saber SQL para interactuar con la base de datos.
2. **Portabilidad**: El mismo codigo funciona con SQLite, PostgreSQL, MySQL, etc.
3. **Seguridad**: Proteccion automatica contra inyeccion SQL.
4. **Productividad**: Menos codigo, mas legible, mas mantenible.
5. **Migraciones**: Control de versiones del esquema de la base de datos.

### Desventajas del ORM

1. **Rendimiento**: Las consultas generadas pueden no ser optimas.
2. **Curva de aprendizaje**: Debes aprender la API del ORM.
3. **Caja negra**: Puede ocultar lo que realmente sucede en la base de datos.

### El Patron Active Record

Django usa el patron **Active Record**, donde cada instancia del modelo:
- Representa una fila en la tabla.
- Contiene metodos para guardar, eliminar y consultar.

```python
# La instancia 'alumno' ES una fila en la tabla
alumno = Estudiante(nombre="Ana", edad=20)
alumno.save()  # INSERT INTO estudiantes ...
```

---

## 2. Instalacion del Entorno con uv

### Que es uv?

`uv` es un gestor de paquetes y entornos virtuales para Python, escrito en Rust. Es extremadamente rapido comparado con `pip` y `venv`.

### Paso 1: Instalar uv

```bash
# En Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verificar instalacion
uv --version
```

### Paso 2: Crear el directorio del proyecto

```bash
mkdir mi_escuela
cd mi_escuela
```

### Paso 3: Inicializar el proyecto con uv

```bash
uv init
```

Esto crea la siguiente estructura:

```
mi_escuela/
    .python-version
    hello.py
    pyproject.toml
    README.md
```

El archivo `pyproject.toml` es el manifiesto del proyecto. Contiene metadatos y dependencias.

### Paso 4: Instalar Django

```bash
uv add django
```

Esto hace tres cosas:
1. Crea un entorno virtual en `.venv/` automaticamente.
2. Instala Django dentro de ese entorno.
3. Agrega `django` como dependencia en `pyproject.toml`.

Verifica que Django se instalo:

```bash
uv run python -c "import django; print(django.get_version())"
```

### Teoria: Entornos Virtuales

Un entorno virtual es un directorio aislado que contiene su propia instalacion de Python y paquetes. Esto evita conflictos entre proyectos que usan diferentes versiones de las mismas librerias.

```
Sistema operativo
  |
  |-- Python del sistema (NO tocar)
  |
  |-- mi_escuela/.venv/       <-- Entorno aislado
  |     |-- python
  |     |-- django 5.x
  |
  |-- otro_proyecto/.venv/    <-- Otro entorno aislado
        |-- python
        |-- django 4.x
```

`uv` gestiona esto automaticamente. Cada vez que usas `uv run`, ejecuta el comando dentro del entorno virtual del proyecto.

---

## 3. Creacion del Proyecto Django

### Teoria: Proyecto vs Aplicacion

En Django:

- **Proyecto**: Es la configuracion general (settings, URLs raiz, etc.). Solo hay uno.
- **Aplicacion (app)**: Es un modulo con funcionalidad especifica. Puede haber muchas.

```
Proyecto "mi_escuela"
  |
  |-- App "estudiantes"     (gestiona alumnos)
  |-- App "profesores"      (gestiona docentes)
  |-- App "calificaciones"  (gestiona notas)
```

### Paso 1: Crear el proyecto Django

```bash
uv run django-admin startproject config .
```

> **Nota**: El punto `.` al final indica que el proyecto se cree en el directorio actual, sin crear una carpeta adicional.

Estructura resultante:

```
mi_escuela/
    .python-version
    .venv/
    config/
        __init__.py
        asgi.py
        settings.py      <-- Configuracion principal
        urls.py           <-- URLs raiz
        wsgi.py
    manage.py             <-- Herramienta de administracion
    pyproject.toml
```

### Paso 2: Verificar que funciona

```bash
uv run python manage.py runserver
```

Abre `http://127.0.0.1:8000/` en tu navegador. Deberias ver la pagina de bienvenida de Django.

Presiona `Ctrl+C` para detener el servidor.

### Anatomia de los archivos clave

**`manage.py`**: Punto de entrada para comandos administrativos.

```bash
uv run python manage.py <comando>
```

**`config/settings.py`**: Controla el comportamiento de Django.

```python
# Base de datos (SQLite por defecto)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Apps instaladas
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
```

---

## 4. Creacion de la App y el Modelo Estudiantes

### Paso 1: Crear la aplicacion

```bash
uv run python manage.py startapp estudiantes
```

Estructura creada:

```
estudiantes/
    __init__.py
    admin.py          <-- Registro en el panel admin
    apps.py           <-- Configuracion de la app
    migrations/       <-- Historial de cambios en la BD
        __init__.py
    models.py         <-- AQUI DEFINIMOS EL ORM
    tests.py
    views.py
```

### Paso 2: Registrar la app en settings.py

Edita `config/settings.py`:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Apps propias
    "estudiantes",
]
```

### Paso 3: Definir el modelo Estudiante

Edita `estudiantes/models.py`:

```python
from django.db import models


class Estudiante(models.Model):
    """Representa un estudiante en el sistema."""

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    fecha_nacimiento = models.DateField()
    matricula = models.CharField(max_length=20, unique=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["apellido", "nombre"]
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"

    def __str__(self):
        return f"{self.apellido}, {self.nombre} ({self.matricula})"
```

### Teoria: Anatomia de un Modelo

Cada modelo de Django es una clase Python que hereda de `models.Model`:

```python
class Estudiante(models.Model):  # <-- Hereda de Model
    #    nombre_campo = tipo_de_campo(opciones)
    nombre = models.CharField(max_length=100)
```

**Equivalencia con SQL:**

```python
# Python (ORM)
nombre = models.CharField(max_length=100)
```

```sql
-- SQL generado
nombre VARCHAR(100) NOT NULL
```

### Tipos de Campos Comunes

| Campo Django           | Tipo SQL          | Uso                          |
|------------------------|-------------------|------------------------------|
| `CharField`            | `VARCHAR`         | Texto corto                  |
| `TextField`            | `TEXT`            | Texto largo                  |
| `IntegerField`         | `INTEGER`         | Numeros enteros              |
| `FloatField`           | `REAL`            | Numeros decimales            |
| `DecimalField`         | `DECIMAL`         | Dinero, valores precisos     |
| `BooleanField`         | `BOOLEAN`         | Verdadero/Falso              |
| `DateField`            | `DATE`            | Solo fecha                   |
| `DateTimeField`        | `DATETIME`        | Fecha y hora                 |
| `EmailField`           | `VARCHAR(254)`    | Email con validacion         |
| `URLField`             | `VARCHAR(200)`    | URLs                         |
| `FileField`            | `VARCHAR(100)`    | Archivos subidos             |
| `ImageField`           | `VARCHAR(100)`    | Imagenes subidas             |

### Opciones Comunes de los Campos

| Opcion           | Significado                                      |
|------------------|--------------------------------------------------|
| `max_length`     | Longitud maxima del texto                        |
| `unique`         | No puede repetirse en la tabla                   |
| `null=True`      | Permite `NULL` en la BD                          |
| `blank=True`     | Permite campo vacio en formularios               |
| `default`        | Valor por defecto                                |
| `choices`        | Lista de opciones permitidas                     |
| `auto_now_add`   | Asigna la fecha/hora al crear el registro        |
| `auto_now`       | Actualiza la fecha/hora cada vez que se guarda   |

### La clase Meta

```python
class Meta:
    ordering = ["apellido", "nombre"]     # Orden por defecto en consultas
    verbose_name = "Estudiante"           # Nombre singular en el admin
    verbose_name_plural = "Estudiantes"   # Nombre plural en el admin
```

### El metodo __str__

Define como se representa el objeto como texto. Es esencial para el panel admin y para depuracion:

```python
def __str__(self):
    return f"{self.apellido}, {self.nombre} ({self.matricula})"

# En la shell:
>>> print(alumno)
Garcia, Ana (MAT-001)
```

---

## 5. Migraciones: De Python a SQL

### Teoria: Que son las Migraciones?

Las migraciones son el sistema de **control de versiones para la base de datos**. Cada vez que modificas un modelo, creas una migracion que describe el cambio.

```
Modelo Python  -->  makemigrations  -->  Archivo de migracion  -->  migrate  -->  Base de Datos
  (codigo)           (detecta cambios)      (instrucciones)         (ejecuta)      (tablas reales)
```

### Paso 1: Crear la migracion

```bash
uv run python manage.py makemigrations
```

Salida esperada:

```
Migrations for 'estudiantes':
  estudiantes/migrations/0001_initial.py
    - Create model Estudiante
```

### Paso 2: Ver el SQL que se generara (opcional pero educativo)

```bash
uv run python manage.py sqlmigrate estudiantes 0001
```

Salida (SQLite):

```sql
BEGIN;
CREATE TABLE "estudiantes_estudiante" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "nombre" varchar(100) NOT NULL,
    "apellido" varchar(100) NOT NULL,
    "email" varchar(254) NOT NULL UNIQUE,
    "fecha_nacimiento" date NOT NULL,
    "matricula" varchar(20) NOT NULL UNIQUE,
    "activo" bool NOT NULL,
    "fecha_registro" datetime NOT NULL
);
COMMIT;
```

> Observa como Django automaticamente agrega un campo `id` como clave primaria autoincremental.

### Paso 3: Aplicar la migracion

```bash
uv run python manage.py migrate
```

Esto crea todas las tablas, incluyendo las del sistema de Django (usuarios, sesiones, etc.) y la tabla `estudiantes_estudiante`.

### Teoria: Convencion de nombres de tablas

Django nombra las tablas como `nombreapp_nombremodelo`:

```
App: estudiantes  +  Modelo: Estudiante  =  Tabla: estudiantes_estudiante
```

---

## 6. Operaciones CRUD con el ORM

CRUD = **C**reate, **R**ead, **U**pdate, **D**elete

### Abrir la shell interactiva de Django

```bash
uv run python manage.py shell
```

Esto abre un interprete Python con Django configurado.

### CREATE - Crear registros

Hay tres formas de crear un objeto:

**Forma 1: Instanciar y guardar**

```python
from estudiantes.models import Estudiante
from datetime import date

alumno = Estudiante(
    nombre="Ana",
    apellido="Garcia",
    email="ana@escuela.com",
    fecha_nacimiento=date(2000, 3, 15),
    matricula="MAT-001",
)
alumno.save()  # Ejecuta: INSERT INTO estudiantes_estudiante ...
```

**Forma 2: Usar create() (en un solo paso)**

```python
alumno = Estudiante.objects.create(
    nombre="Carlos",
    apellido="Lopez",
    email="carlos@escuela.com",
    fecha_nacimiento=date(1999, 7, 22),
    matricula="MAT-002",
)
# No necesita .save(), ya esta guardado en la BD
```

**Forma 3: get_or_create() (crea solo si no existe)**

```python
alumno, creado = Estudiante.objects.get_or_create(
    email="ana@escuela.com",
    defaults={
        "nombre": "Ana",
        "apellido": "Garcia",
        "fecha_nacimiento": date(2000, 3, 15),
        "matricula": "MAT-001",
    },
)
print(creado)  # True si lo creo, False si ya existia
```

**SQL equivalente:**

```python
Estudiante.objects.create(nombre="Ana", apellido="Garcia", ...)
```

```sql
INSERT INTO estudiantes_estudiante (nombre, apellido, ...) VALUES ('Ana', 'Garcia', ...);
```

### READ - Leer registros

**Todos los registros:**

```python
todos = Estudiante.objects.all()
# SELECT * FROM estudiantes_estudiante ORDER BY apellido, nombre;
```

**Un registro especifico:**

```python
alumno = Estudiante.objects.get(matricula="MAT-001")
# SELECT * FROM estudiantes_estudiante WHERE matricula = 'MAT-001';
```

> `get()` lanza `DoesNotExist` si no encuentra nada, y `MultipleObjectsReturned` si hay mas de uno.

**Filtrar registros:**

```python
activos = Estudiante.objects.filter(activo=True)
# SELECT * FROM estudiantes_estudiante WHERE activo = True;
```

**Excluir registros:**

```python
no_activos = Estudiante.objects.exclude(activo=True)
# SELECT * FROM estudiantes_estudiante WHERE NOT activo = True;
```

**Contar registros:**

```python
total = Estudiante.objects.count()
# SELECT COUNT(*) FROM estudiantes_estudiante;
```

**Verificar existencia:**

```python
existe = Estudiante.objects.filter(email="ana@escuela.com").exists()
# SELECT 1 FROM estudiantes_estudiante WHERE email = 'ana@escuela.com' LIMIT 1;
```

### Teoria: QuerySets y Evaluacion Perezosa (Lazy Evaluation)

Un **QuerySet** es un objeto que representa una consulta SQL. La consulta NO se ejecuta hasta que realmente necesitas los datos:

```python
# Esto NO ejecuta SQL (solo construye la consulta)
qs = Estudiante.objects.filter(activo=True)
qs = qs.filter(apellido__startswith="G")
qs = qs.order_by("nombre")

# Esto SI ejecuta SQL (cuando iteras, imprimes, o accedes a los datos)
for alumno in qs:
    print(alumno.nombre)

# Django ejecuta UNA sola consulta optimizada:
# SELECT * FROM estudiantes_estudiante
#   WHERE activo = True AND apellido LIKE 'G%'
#   ORDER BY nombre;
```

**Momentos en que un QuerySet se evalua:**

| Accion                          | Ejemplo                        |
|---------------------------------|--------------------------------|
| Iteracion                       | `for a in qs:`                 |
| Conversion a lista              | `list(qs)`                     |
| Slicing con step                | `qs[::2]`                      |
| `len()`                         | `len(qs)`                      |
| `bool()`                        | `if qs:`                       |
| `repr()`                        | `print(qs)`                    |
| Acceso por indice               | `qs[0]`                        |

### UPDATE - Actualizar registros

**Un solo registro:**

```python
alumno = Estudiante.objects.get(matricula="MAT-001")
alumno.email = "ana.garcia@escuela.com"
alumno.save()
# UPDATE estudiantes_estudiante SET email = 'ana.garcia@escuela.com' WHERE id = 1;
```

**Multiples registros (masivo):**

```python
Estudiante.objects.filter(activo=False).update(activo=True)
# UPDATE estudiantes_estudiante SET activo = True WHERE activo = False;
```

> `update()` es mas eficiente que obtener cada objeto y llamar `.save()`.

### DELETE - Eliminar registros

**Un solo registro:**

```python
alumno = Estudiante.objects.get(matricula="MAT-002")
alumno.delete()
# DELETE FROM estudiantes_estudiante WHERE id = 2;
```

**Multiples registros:**

```python
Estudiante.objects.filter(activo=False).delete()
# DELETE FROM estudiantes_estudiante WHERE activo = False;
```

**Todos los registros (cuidado):**

```python
Estudiante.objects.all().delete()
# DELETE FROM estudiantes_estudiante;
```

---

## 7. Consultas Avanzadas

### Field Lookups (Filtros de campo)

Los lookups se usan con doble guion bajo `__`:

```python
# Contiene (LIKE '%texto%')
Estudiante.objects.filter(nombre__contains="an")

# Contiene sin importar mayusculas/minusculas
Estudiante.objects.filter(nombre__icontains="ana")

# Empieza con
Estudiante.objects.filter(apellido__startswith="Gar")

# Termina con
Estudiante.objects.filter(email__endswith="@escuela.com")

# Mayor que
Estudiante.objects.filter(fecha_nacimiento__gt=date(2000, 1, 1))

# Mayor o igual que
Estudiante.objects.filter(fecha_nacimiento__gte=date(2000, 1, 1))

# Menor que
Estudiante.objects.filter(fecha_nacimiento__lt=date(2000, 1, 1))

# En una lista de valores
Estudiante.objects.filter(matricula__in=["MAT-001", "MAT-003", "MAT-005"])

# Rango (BETWEEN)
Estudiante.objects.filter(
    fecha_nacimiento__range=(date(1999, 1, 1), date(2001, 12, 31))
)

# Es NULL
Estudiante.objects.filter(email__isnull=True)

# Por anno, mes o dia de una fecha
Estudiante.objects.filter(fecha_nacimiento__year=2000)
Estudiante.objects.filter(fecha_nacimiento__month=3)
```

### Tabla de Lookups

| Lookup         | SQL Equivalente         | Ejemplo                                |
|----------------|-------------------------|----------------------------------------|
| `exact`        | `= valor`              | `nombre__exact="Ana"`                  |
| `iexact`       | `ILIKE valor`           | `nombre__iexact="ana"`                 |
| `contains`     | `LIKE '%valor%'`        | `nombre__contains="na"`                |
| `icontains`    | `ILIKE '%valor%'`       | `nombre__icontains="na"`               |
| `startswith`   | `LIKE 'valor%'`         | `apellido__startswith="Gar"`           |
| `endswith`     | `LIKE '%valor'`         | `email__endswith=".com"`               |
| `gt`           | `> valor`               | `fecha_nacimiento__gt=date(2000,1,1)`  |
| `gte`          | `>= valor`              | `fecha_nacimiento__gte=date(2000,1,1)` |
| `lt`           | `< valor`               | `fecha_nacimiento__lt=date(2000,1,1)`  |
| `lte`          | `<= valor`              | `fecha_nacimiento__lte=date(2000,1,1)` |
| `in`           | `IN (val1, val2)`       | `matricula__in=["MAT-001","MAT-002"]`  |
| `range`        | `BETWEEN val1 AND val2` | `fecha__range=(inicio, fin)`           |
| `isnull`       | `IS NULL / IS NOT NULL` | `email__isnull=True`                   |
| `year`         | `EXTRACT(YEAR)`         | `fecha_nacimiento__year=2000`          |
| `month`        | `EXTRACT(MONTH)`        | `fecha_nacimiento__month=3`            |

### Consultas con Q Objects (OR y NOT)

Por defecto, `filter()` usa `AND`. Para usar `OR` o `NOT`, importa `Q`:

```python
from django.db.models import Q

# OR: Estudiantes que se llamen Ana O Carlos
Estudiante.objects.filter(
    Q(nombre="Ana") | Q(nombre="Carlos")
)
# SELECT * FROM ... WHERE nombre = 'Ana' OR nombre = 'Carlos';

# AND con Q (equivalente a filter encadenado)
Estudiante.objects.filter(
    Q(activo=True) & Q(apellido__startswith="G")
)

# NOT: Estudiantes que NO esten activos
Estudiante.objects.filter(~Q(activo=True))
# SELECT * FROM ... WHERE NOT activo = True;

# Combinacion compleja
Estudiante.objects.filter(
    (Q(nombre="Ana") | Q(nombre="Carlos")) & Q(activo=True)
)
```

### Ordenamiento

```python
# Ascendente
Estudiante.objects.order_by("apellido")

# Descendente (signo menos)
Estudiante.objects.order_by("-fecha_registro")

# Multiples campos
Estudiante.objects.order_by("apellido", "nombre")

# Aleatorio
Estudiante.objects.order_by("?")
```

### Limitar resultados (Slicing)

```python
# Primeros 5 (LIMIT 5)
Estudiante.objects.all()[:5]

# Del 5 al 10 (OFFSET 5 LIMIT 5)
Estudiante.objects.all()[5:10]

# Solo el primero
Estudiante.objects.first()

# Solo el ultimo
Estudiante.objects.last()
```

### Agregaciones

```python
from django.db.models import Count, Avg, Max, Min, Sum

# Contar estudiantes activos
Estudiante.objects.filter(activo=True).aggregate(total=Count("id"))
# {'total': 15}

# Promedio, maximo y minimo de edad
from django.db.models import F
from datetime import date

# Contar por valor
Estudiante.objects.values("activo").annotate(total=Count("id"))
# [{'activo': True, 'total': 12}, {'activo': False, 'total': 3}]
```

### Seleccionar campos especificos

```python
# Solo nombre y email (retorna diccionarios)
Estudiante.objects.values("nombre", "email")
# [{'nombre': 'Ana', 'email': 'ana@escuela.com'}, ...]

# Solo nombre y email (retorna tuplas)
Estudiante.objects.values_list("nombre", "email")
# [('Ana', 'ana@escuela.com'), ...]

# Solo un campo como lista plana
Estudiante.objects.values_list("email", flat=True)
# ['ana@escuela.com', 'carlos@escuela.com', ...]
```

---

## 8. Relaciones entre Modelos

### Teoria: Tipos de Relaciones

| Relacion       | Django                | SQL                 | Ejemplo                        |
|----------------|-----------------------|---------------------|--------------------------------|
| Uno a Muchos   | `ForeignKey`          | `FOREIGN KEY`       | Estudiante -> muchas Notas     |
| Muchos a Muchos| `ManyToManyField`     | Tabla intermedia    | Estudiante <-> muchos Cursos   |
| Uno a Uno      | `OneToOneField`       | `UNIQUE FOREIGN KEY`| Estudiante <-> un Perfil       |

### Ejemplo: Agregar Cursos y Calificaciones

```python
# estudiantes/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    fecha_nacimiento = models.DateField()
    matricula = models.CharField(max_length=20, unique=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["apellido", "nombre"]

    def __str__(self):
        return f"{self.apellido}, {self.nombre} ({self.matricula})"


class Curso(models.Model):
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=10, unique=True)
    descripcion = models.TextField(blank=True)
    estudiantes = models.ManyToManyField(
        Estudiante,
        through="Calificacion",
        related_name="cursos",
    )

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Calificacion(models.Model):
    estudiante = models.ForeignKey(
        Estudiante,
        on_delete=models.CASCADE,
        related_name="calificaciones",
    )
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name="calificaciones",
    )
    nota = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    fecha = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ["estudiante", "curso"]

    def __str__(self):
        return f"{self.estudiante} - {self.curso}: {self.nota}"
```

### Teoria: on_delete

Cuando se elimina el objeto referenciado, `on_delete` define que sucede:

| Opcion               | Comportamiento                                           |
|----------------------|----------------------------------------------------------|
| `CASCADE`            | Elimina los objetos relacionados                         |
| `PROTECT`            | Impide la eliminacion (lanza error)                      |
| `SET_NULL`           | Pone el campo en NULL (requiere `null=True`)             |
| `SET_DEFAULT`        | Pone el valor por defecto                                |
| `DO_NOTHING`         | No hace nada (puede romper integridad referencial)       |

### Teoria: related_name

`related_name` define como accedes a la relacion desde el otro modelo:

```python
# En Calificacion:
estudiante = models.ForeignKey(Estudiante, related_name="calificaciones")

# Ahora desde un Estudiante puedes hacer:
alumno.calificaciones.all()
# En lugar del default: alumno.calificacion_set.all()
```

### Consultas con Relaciones

```python
# Crear datos de ejemplo
matematicas = Curso.objects.create(nombre="Matematicas", codigo="MAT101")
alumno = Estudiante.objects.get(matricula="MAT-001")

Calificacion.objects.create(estudiante=alumno, curso=matematicas, nota=8.5)

# Obtener calificaciones de un estudiante
alumno.calificaciones.all()

# Obtener estudiantes de un curso
matematicas.calificaciones.all()

# Filtrar a traves de relaciones (doble guion bajo)
Estudiante.objects.filter(calificaciones__nota__gte=9)
# Estudiantes con al menos una nota >= 9

# Filtrar por campo del modelo relacionado
Calificacion.objects.filter(curso__codigo="MAT101")
# Calificaciones del curso MAT101

# Anotar promedio de calificaciones por estudiante
from django.db.models import Avg

Estudiante.objects.annotate(
    promedio=Avg("calificaciones__nota")
).order_by("-promedio")
```

---

## 9. Ejercicios Practicos

### Ejercicio 1: Crear y Consultar

```python
# 1. Abre la shell de Django
# uv run python manage.py shell

from estudiantes.models import Estudiante
from datetime import date

# 2. Crea 5 estudiantes
datos = [
    ("Ana", "Garcia", "ana@mail.com", date(2000, 3, 15), "MAT-001"),
    ("Carlos", "Lopez", "carlos@mail.com", date(1999, 7, 22), "MAT-002"),
    ("Maria", "Martinez", "maria@mail.com", date(2001, 1, 10), "MAT-003"),
    ("Pedro", "Sanchez", "pedro@mail.com", date(2000, 11, 5), "MAT-004"),
    ("Laura", "Fernandez", "laura@mail.com", date(1998, 8, 30), "MAT-005"),
]

for nombre, apellido, email, fecha, matricula in datos:
    Estudiante.objects.create(
        nombre=nombre,
        apellido=apellido,
        email=email,
        fecha_nacimiento=fecha,
        matricula=matricula,
    )

# 3. Verifica que se crearon
print(f"Total: {Estudiante.objects.count()}")

# 4. Busca a Ana
ana = Estudiante.objects.get(nombre="Ana")
print(ana)

# 5. Estudiantes nacidos despues del 2000
jovenes = Estudiante.objects.filter(fecha_nacimiento__year__gte=2000)
for e in jovenes:
    print(f"  {e.nombre} - {e.fecha_nacimiento}")
```

### Ejercicio 2: Actualizar y Eliminar

```python
# 1. Desactivar a Pedro
pedro = Estudiante.objects.get(matricula="MAT-004")
pedro.activo = False
pedro.save()

# 2. Verificar
print(f"Pedro activo: {pedro.activo}")

# 3. Actualizar email de todos los que terminan en @mail.com
actualizados = Estudiante.objects.filter(
    email__endswith="@mail.com"
).update(
    email=models.F("email")  # Esto no cambia nada, solo como ejemplo
)

# 4. Eliminar estudiantes inactivos
eliminados, detalle = Estudiante.objects.filter(activo=False).delete()
print(f"Eliminados: {eliminados}")
print(f"Detalle: {detalle}")
```

### Ejercicio 3: Consultas Avanzadas

```python
from django.db.models import Q, Count

# 1. Estudiantes cuyo nombre empiece con 'A' O 'M'
resultado = Estudiante.objects.filter(
    Q(nombre__startswith="A") | Q(nombre__startswith="M")
)
for e in resultado:
    print(e)

# 2. Estudiantes nacidos entre 1999 y 2001
rango = Estudiante.objects.filter(
    fecha_nacimiento__range=(date(1999, 1, 1), date(2001, 12, 31))
)
print(f"En rango: {rango.count()}")

# 3. Lista de emails ordenados alfabeticamente
emails = Estudiante.objects.order_by("email").values_list("email", flat=True)
for email in emails:
    print(f"  {email}")
```

### Ejercicio 4: Ver el SQL generado

```python
# Puedes ver el SQL de cualquier QuerySet con .query
qs = Estudiante.objects.filter(activo=True).order_by("apellido")
print(qs.query)
# SELECT "estudiantes_estudiante"."id", ...
#   FROM "estudiantes_estudiante"
#   WHERE "estudiantes_estudiante"."activo" = True
#   ORDER BY "estudiantes_estudiante"."apellido" ASC
```

### Ejercicio 5: Panel de Administracion

Registra el modelo en el admin para gestionarlo visualmente:

```python
# estudiantes/admin.py
from django.contrib import admin
from .models import Estudiante


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ["matricula", "apellido", "nombre", "email", "activo"]
    list_filter = ["activo", "fecha_registro"]
    search_fields = ["nombre", "apellido", "matricula", "email"]
    list_editable = ["activo"]
```

Crea un superusuario y accede al admin:

```bash
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

Visita `http://127.0.0.1:8000/admin/` e inicia sesion.

---

## Resumen de Comandos

```bash
# Entorno
uv init                                    # Inicializar proyecto Python
uv add django                              # Instalar Django

# Proyecto Django
uv run django-admin startproject config .  # Crear proyecto
uv run python manage.py startapp nombre    # Crear app
uv run python manage.py runserver          # Iniciar servidor

# Base de datos
uv run python manage.py makemigrations     # Detectar cambios en modelos
uv run python manage.py migrate            # Aplicar cambios a la BD
uv run python manage.py sqlmigrate app N   # Ver SQL de una migracion

# Utilidades
uv run python manage.py shell              # Shell interactiva
uv run python manage.py createsuperuser    # Crear admin
uv run python manage.py dbshell            # Shell de la BD directa
```

## Resumen del ORM

```python
# CREAR
obj = Modelo.objects.create(campo=valor)

# LEER
Modelo.objects.all()                       # Todos
Modelo.objects.get(campo=valor)            # Uno exacto
Modelo.objects.filter(campo=valor)         # Filtrar
Modelo.objects.exclude(campo=valor)        # Excluir

# ACTUALIZAR
obj.campo = nuevo_valor
obj.save()
Modelo.objects.filter(...).update(campo=valor)  # Masivo

# ELIMINAR
obj.delete()
Modelo.objects.filter(...).delete()        # Masivo

# CONSULTAS
Modelo.objects.filter(campo__lookup=valor) # Lookups
Modelo.objects.filter(Q(...) | Q(...))     # OR
Modelo.objects.order_by("campo")           # Ordenar
Modelo.objects.values("campo1", "campo2")  # Campos especificos
Modelo.objects.annotate(total=Count("id")) # Agregaciones
Modelo.objects.count()                     # Contar
Modelo.objects.exists()                    # Existe?
```
