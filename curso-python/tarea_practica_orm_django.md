
# 📝 Tarea Práctica: ORM en Django

## 🎯 Objetivo
Aprender a crear modelos en Django, aplicar migraciones y realizar consultas con el **ORM (Object-Relational Mapping)** para manipular datos en una base de datos relacional.

---

## 1️⃣ Preparación del proyecto

1. Crea un proyecto Django llamado **libreria**
   ```bash
   django-admin startproject libreria
   cd libreria
   python manage.py startapp catalogo
   ```

2. Agrega la app `catalogo` en `INSTALLED_APPS` dentro de `settings.py`.

---

## 2️⃣ Definición de modelos

En `catalogo/models.py` define los siguientes modelos:

```python
from django.db import models

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    fecha_publicacion = models.DateField()
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name="libros")
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo
```

Ejecuta migraciones:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 3️⃣ Inserción de datos (Shell de Django)

Abre el shell interactivo:
```bash
python manage.py shell
```

Ejecuta lo siguiente:

```python
from catalogo.models import Autor, Libro
from datetime import date

# Crear autores
a1 = Autor.objects.create(nombre="Gabriel García Márquez", nacionalidad="Colombiana")
a2 = Autor.objects.create(nombre="Isabel Allende", nacionalidad="Chilena")

# Crear libros
Libro.objects.create(titulo="Cien años de soledad", fecha_publicacion=date(1967, 5, 30), autor=a1)
Libro.objects.create(titulo="El amor en los tiempos del cólera", fecha_publicacion=date(1985, 9, 5), autor=a1)
Libro.objects.create(titulo="La casa de los espíritus", fecha_publicacion=date(1982, 4, 12), autor=a2)
```

---

## 4️⃣ Consultas con el ORM

Realiza y guarda el resultado de estas consultas:

1. Obtener todos los autores registrados.
   ```python
   Autor.objects.all()
   ```

2. Buscar un autor por nombre exacto.
   ```python
   Autor.objects.get(nombre="Gabriel García Márquez")
   ```

3. Filtrar libros publicados después de 1980.
   ```python
   Libro.objects.filter(fecha_publicacion__year__gt=1980)
   ```

4. Listar todos los libros de un autor específico (usando `related_name`).
   ```python
   a1.libros.all()
   ```

5. Actualizar el campo `disponible=False` para un libro.
   ```python
   libro = Libro.objects.get(titulo="La casa de los espíritus")
   libro.disponible = False
   libro.save()
   ```

6. Eliminar un autor y verificar qué sucede con sus libros.
   ```python
   a2.delete()
   ```

---

## 5️⃣ Consultas Avanzadas (Nivel Intermedio)

1. Ordenar los libros por fecha de publicación descendente.
   ```python
   Libro.objects.order_by('-fecha_publicacion')
   ```

2. Contar cuántos libros tiene cada autor (usando `annotate`).
   ```python
   from django.db.models import Count
   Autor.objects.annotate(num_libros=Count('libros'))
   ```

3. Obtener el libro más antiguo y el más reciente (usando `aggregate`).
   ```python
   from django.db.models import Min, Max
   Libro.objects.aggregate(mas_antiguo=Min('fecha_publicacion'), mas_reciente=Max('fecha_publicacion'))
   ```

4. Buscar libros cuyo título contenga la palabra "amor".
   ```python
   Libro.objects.filter(titulo__icontains="amor")
   ```

5. Obtener solo los nombres de los autores en una lista (usando `values_list`).
   ```python
   Autor.objects.values_list('nombre', flat=True)
   ```

---

## 6️⃣ Entregables

- Código de los modelos.
- Capturas o registros en consola de las consultas realizadas.
- Respuesta escrita:
  - ¿Qué pasa con los libros cuando se elimina un autor?
  - ¿Qué ventajas tiene usar el ORM en lugar de SQL puro?
