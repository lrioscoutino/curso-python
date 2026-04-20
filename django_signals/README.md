# Tutorial: Signals en Django

## ¿Qué son los Signals?

Los signals son un sistema de **notificaciones** en Django. Cuando algo pasa (se guarda un modelo, se elimina, etc.), Django envía una señal y cualquier código que esté "escuchando" puede reaccionar.

**Analogía simple:** Piensa en una campana de tienda. Cuando un cliente entra (evento), la campana suena (signal), y el vendedor reacciona (receiver).

```
Evento (save/delete)  →  Signal (notificación)  →  Receiver (tu código)
```

| Signal | ¿Cuándo se dispara? |
|--------|-------------------|
| `pre_save` | **Antes** de guardar un objeto |
| `post_save` | **Después** de guardar un objeto |
| `pre_delete` | **Antes** de eliminar un objeto |
| `post_delete` | **Después** de eliminar un objeto |
| `m2m_changed` | Cuando cambia una relación ManyToMany |

---

## ¿Signals o sobreescribir `save()`?

| Criterio | Signals | Sobreescribir `save()` |
|----------|---------|----------------------|
| ¿Quién reacciona? | Código **externo** al modelo | El **propio** modelo |
| ¿Acoplamiento? | Bajo (desacoplado) | Alto (todo en el modelo) |
| ¿Cuándo usar? | Cuando **otro** modelo necesita enterarse | Cuando es lógica **interna** del modelo |
| ¿Ejemplo? | Crear perfil al crear usuario | Calcular total antes de guardar |

> **Regla práctica:** Si la acción afecta al **mismo** modelo → `save()`. Si afecta a **otro** modelo o sistema externo → signal.

---

## Nuestro proyecto: Tienda Online

Vamos a construir una tienda simple con 4 modelos y conectarlos con signals.

### `tienda/models.py`

```python
from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    """Perfil extendido del usuario."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    address = models.TextField(blank=True, verbose_name='Dirección')

    def __str__(self):
        return f'Perfil de {self.user.username}'


class Product(models.Model):
    """Producto de la tienda."""
    name = models.CharField(max_length=200, verbose_name='Nombre')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    stock = models.PositiveIntegerField(default=0, verbose_name='Stock')

    def __str__(self):
        return self.name


class Order(models.Model):
    """Pedido de un cliente."""

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pendiente'
        COMPLETED = 'completed', 'Completado'
        CANCELLED = 'cancelled', 'Cancelado'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name='Cantidad')
    total = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0, verbose_name='Total'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pedido #{self.pk} - {self.user.username}'


class ActivityLog(models.Model):
    """Registro de actividad (auditoría simple)."""
    description = models.TextField(verbose_name='Descripción')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.created_at:%Y-%m-%d %H:%M}] {self.description[:50]}'
```

```bash
python3 manage.py makemigrations tienda
python3 manage.py migrate
```

---

## ¿Dónde poner los signals?

Django recomienda crear un archivo `signals.py` en tu app y conectarlo desde `apps.py`.

### Estructura

```
tienda/
├── __init__.py
├── apps.py          ← conecta los signals aquí
├── models.py
├── signals.py       ← defines los receivers aquí
└── ...
```

### `tienda/apps.py`

```python
from django.apps import AppConfig


class TiendaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tienda'

    def ready(self):
        import tienda.signals  # noqa: F401
```

> **Importante:** El `import` en `ready()` es lo que activa los signals. Sin esto, tus receivers nunca se ejecutan.

---

## Paso 1: `post_save` — Crear perfil automáticamente

Cuando se crea un usuario nuevo, queremos que se cree su `UserProfile` automáticamente.

### `tienda/signals.py`

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import UserProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crea un perfil automáticamente cuando se registra un usuario."""
    if created:
        UserProfile.objects.create(user=instance)
```

### ¿Qué recibe el receiver?

| Parámetro | Significado |
|-----------|------------|
| `sender` | El modelo que envió la señal (`User`) |
| `instance` | El objeto que se guardó (el usuario específico) |
| `created` | `True` si es nuevo, `False` si es update |
| `**kwargs` | Siempre incluirlo (compatibilidad futura) |

### Probar en shell

```python
from django.contrib.auth.models import User

user = User.objects.create_user('carlos', 'carlos@test.com', 'pass1234')
user.profile  # <UserProfile: Perfil de carlos> ← ¡Se creó solo!
```

> **¿Por qué `created`?** Sin este check, el signal se ejecutaría cada vez que el usuario se guarda (incluso al cambiar su email). Solo queremos crear el perfil **una vez**.

---

## Paso 2: `pre_save` — Calcular total automáticamente

Antes de guardar un pedido, calculamos `total = quantity × price`.

### Agregar a `tienda/signals.py`

```python
from django.db.models.signals import pre_save

from .models import Order


@receiver(pre_save, sender=Order)
def calculate_order_total(sender, instance, **kwargs):
    """Calcula el total del pedido antes de guardarlo."""
    instance.total = instance.quantity * instance.product.price
```

### Probar

```python
from django.contrib.auth.models import User
from tienda.models import Product, Order

user = User.objects.get(username='carlos')
laptop = Product.objects.create(name='Laptop', price=15000, stock=10)

order = Order.objects.create(user=user, product=laptop, quantity=2)
order.total  # Decimal('30000.00') ← calculado automáticamente
```

> **Nota:** `pre_save` es ideal para esto porque modifica el objeto **antes** de que llegue a la base de datos. No necesitas llamar `save()` de nuevo.

### ¿Por qué signal y no `save()`?

En este caso, ambos funcionarían. Pero si `Order` estuviera en una app y la lógica de precios en otra, el signal mantiene el desacoplamiento. Para un proyecto simple, sobreescribir `save()` también es válido:

```python
# Alternativa: en el modelo directamente
class Order(models.Model):
    # ...
    def save(self, *args, **kwargs):
        self.total = self.quantity * self.product.price
        super().save(*args, **kwargs)
```

---

## Paso 3: `post_save` — Registrar actividad

Cada vez que se crea un pedido, lo registramos en `ActivityLog`.

### Agregar a `tienda/signals.py`

```python
from .models import ActivityLog


@receiver(post_save, sender=Order)
def log_new_order(sender, instance, created, **kwargs):
    """Registra en el log cuando se crea un pedido nuevo."""
    if created:
        ActivityLog.objects.create(
            description=(
                f'Nuevo pedido #{instance.pk}: '
                f'{instance.quantity}x {instance.product.name} '
                f'por {instance.user.username} '
                f'(total: ${instance.total})'
            )
        )
```

### Probar

```python
from tienda.models import Order, ActivityLog, Product
from django.contrib.auth.models import User

user = User.objects.get(username='carlos')
laptop = Product.objects.get(name='Laptop')

Order.objects.create(user=user, product=laptop, quantity=1)

ActivityLog.objects.first()
# [2026-04-20 15:30] Nuevo pedido #1: 1x Laptop por carlos (total: $15000.00)
```

---

## Paso 4: `post_save` — Descontar stock

Cuando se crea un pedido, descontamos la cantidad del stock del producto.

### Agregar a `tienda/signals.py`

```python
from django.db.models import F


@receiver(post_save, sender=Order)
def update_stock_on_order(sender, instance, created, **kwargs):
    """Descuenta stock del producto cuando se crea un pedido."""
    if created:
        Product.objects.filter(pk=instance.product_id).update(
            stock=F('stock') - instance.quantity
        )
```

### ¿Por qué `F('stock')` y no `instance.product.stock -= quantity`?

| Método | ¿Qué hace? | ¿Seguro con concurrencia? |
|--------|------------|--------------------------|
| `product.stock -= qty; product.save()` | Lee, modifica en Python, guarda | **No** — dos pedidos simultáneos pueden leer el mismo stock |
| `Product.objects.filter().update(stock=F('stock') - qty)` | Operación directa en SQL | **Sí** — la base de datos maneja la resta atómicamente |

### Probar

```python
from tienda.models import Product, Order
from django.contrib.auth.models import User

laptop = Product.objects.get(name='Laptop')
print(laptop.stock)  # 10

user = User.objects.get(username='carlos')
Order.objects.create(user=user, product=laptop, quantity=3)

laptop.refresh_from_db()
print(laptop.stock)  # 7 ← se descontó automáticamente
```

---

## Paso 5: `post_delete` — Restaurar stock

Si se elimina un pedido, devolvemos el stock.

### Agregar a `tienda/signals.py`

```python
from django.db.models.signals import post_delete


@receiver(post_delete, sender=Order)
def restore_stock_on_delete(sender, instance, **kwargs):
    """Restaura el stock cuando se elimina un pedido."""
    Product.objects.filter(pk=instance.product_id).update(
        stock=F('stock') + instance.quantity
    )
```

### Probar

```python
from tienda.models import Product, Order

laptop = Product.objects.get(name='Laptop')
print(laptop.stock)  # 7

order = Order.objects.last()
order.delete()

laptop.refresh_from_db()
print(laptop.stock)  # 10 ← stock restaurado
```

> **`pre_delete` vs `post_delete`:** Usa `post_delete` para restaurar stock — garantiza que la eliminación fue exitosa antes de devolver. Usa `pre_delete` cuando necesitas datos del objeto que podrían perderse tras eliminar (ej: borrar archivos relacionados).

| Signal | ¿Cuándo? | Caso de uso |
|--------|----------|-------------|
| `pre_delete` | Antes de borrar | Limpiar archivos, validar si se puede borrar |
| `post_delete` | Después de borrar | Restaurar stock, actualizar contadores |

---

## Paso 6: `m2m_changed` — Reaccionar a relaciones ManyToMany

Agreguemos tags a los productos para ver cómo funciona `m2m_changed`.

### Agregar al modelo

```python
# En tienda/models.py, agregar:

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
```

Y en `Product`:

```python
class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nombre')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    stock = models.PositiveIntegerField(default=0, verbose_name='Stock')
    tags = models.ManyToManyField('Tag', blank=True, related_name='products')

    def __str__(self):
        return self.name
```

### Agregar a `tienda/signals.py`

```python
from django.db.models.signals import m2m_changed

from .models import Product, Tag


@receiver(m2m_changed, sender=Product.tags.through)
def log_tags_changed(sender, instance, action, pk_set, **kwargs):
    """Registra cuando se agregan o quitan tags de un producto."""
    if action == 'post_add':
        tag_names = Tag.objects.filter(pk__in=pk_set).values_list('name', flat=True)
        ActivityLog.objects.create(
            description=f'Tags agregados a "{instance.name}": {", ".join(tag_names)}'
        )
    elif action == 'post_remove':
        tag_names = Tag.objects.filter(pk__in=pk_set).values_list('name', flat=True)
        ActivityLog.objects.create(
            description=f'Tags removidos de "{instance.name}": {", ".join(tag_names)}'
        )
```

### Acciones de `m2m_changed`

| Acción | ¿Cuándo? |
|--------|----------|
| `pre_add` | Antes de agregar relaciones |
| `post_add` | Después de agregar relaciones |
| `pre_remove` | Antes de quitar relaciones |
| `post_remove` | Después de quitar relaciones |
| `pre_clear` | Antes de `tags.clear()` |
| `post_clear` | Después de `tags.clear()` |

> **Nota:** El `sender` en `m2m_changed` es la **tabla intermedia**, no el modelo. Por eso usamos `Product.tags.through`.

### Probar

```python
from tienda.models import Product, Tag

laptop = Product.objects.get(name='Laptop')
t1 = Tag.objects.create(name='electrónica')
t2 = Tag.objects.create(name='oferta')

laptop.tags.add(t1, t2)
# Log: Tags agregados a "Laptop": electrónica, oferta
```

---

## Paso 7: Custom Signals — Crear tus propias señales

Django permite crear signals personalizados para eventos de tu negocio.

### `tienda/signals.py` — Definir el signal

```python
from django.dispatch import Signal

# Definir signal personalizado
order_completed = Signal()  # Se enviará cuando un pedido se complete
```

### Disparar el signal

Puedes dispararlo desde una vista, un servicio, o donde tenga sentido:

```python
# En una vista o servicio:
from tienda.signals import order_completed


def complete_order(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    order.status = Order.Status.COMPLETED
    order.save()

    # Disparar signal personalizado
    order_completed.send(
        sender=Order,
        order=order,
        user=request.user
    )
```

### Escuchar el signal

```python
# En tienda/signals.py

@receiver(order_completed)
def on_order_completed(sender, order, user, **kwargs):
    """Registra cuando un pedido se completa."""
    ActivityLog.objects.create(
        description=f'Pedido #{order.pk} completado por {user.username}'
    )


@receiver(order_completed)
def notify_stock_low(sender, order, user, **kwargs):
    """Alerta si el stock queda bajo después de completar pedido."""
    product = order.product
    product.refresh_from_db()
    if product.stock < 5:
        ActivityLog.objects.create(
            description=f'⚠ Stock bajo: {product.name} tiene solo {product.stock} unidades'
        )
```

> **¿Cuándo crear custom signals?** Cuando un evento de negocio no corresponde a un save/delete. Ejemplos: "pedido completado", "pago recibido", "usuario verificó email".

---

## Errores comunes

### 1. Olvidar conectar en `apps.py`

```python
# ❌ Signals definidos pero nunca se ejecutan
# tienda/signals.py existe pero apps.py no lo importa

# ✅ Correcto
class TiendaConfig(AppConfig):
    def ready(self):
        import tienda.signals  # noqa: F401
```

### 2. No verificar `created` en `post_save`

```python
# ❌ Se ejecuta en CADA save (crear Y actualizar)
@receiver(post_save, sender=Order)
def log_order(sender, instance, **kwargs):
    ActivityLog.objects.create(description=f'Pedido {instance.pk}')

# ✅ Solo cuando se CREA
@receiver(post_save, sender=Order)
def log_order(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(description=f'Nuevo pedido {instance.pk}')
```

### 3. Llamar `save()` dentro de `pre_save` (loop infinito)

```python
# ❌ LOOP INFINITO — save() dispara pre_save de nuevo
@receiver(pre_save, sender=Order)
def bad_signal(sender, instance, **kwargs):
    instance.total = instance.quantity * instance.product.price
    instance.save()  # ¡NO!

# ✅ Solo modificar atributos — Django guarda después
@receiver(pre_save, sender=Order)
def good_signal(sender, instance, **kwargs):
    instance.total = instance.quantity * instance.product.price
    # No llamar save(), Django lo hace automáticamente
```

### 4. Imports circulares

```python
# ❌ Importar signals en models.py causa imports circulares
# models.py
from .signals import some_signal  # ¡NO!

# ✅ Importar modelos en signals.py (no al revés)
# signals.py
from .models import Order  # Correcto
```

### 5. Signal se ejecuta durante migraciones

```python
# ❌ Puede fallar si la tabla aún no existe
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# ✅ Agregar try/except solo si tienes problemas con migraciones
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        try:
            UserProfile.objects.create(user=instance)
        except Exception:
            pass  # Durante migraciones la tabla puede no existir
```

---

## Archivo completo: `tienda/signals.py`

```python
from django.db.models.signals import post_save, post_delete, pre_save, m2m_changed
from django.dispatch import receiver, Signal
from django.db.models import F
from django.contrib.auth import get_user_model

from .models import UserProfile, Order, Product, Tag, ActivityLog

User = get_user_model()

# ── Custom signal ──
order_completed = Signal()


# ── post_save: crear perfil de usuario ──
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# ── pre_save: calcular total del pedido ──
@receiver(pre_save, sender=Order)
def calculate_order_total(sender, instance, **kwargs):
    instance.total = instance.quantity * instance.product.price


# ── post_save: registrar nuevo pedido ──
@receiver(post_save, sender=Order)
def log_new_order(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            description=(
                f'Nuevo pedido #{instance.pk}: '
                f'{instance.quantity}x {instance.product.name} '
                f'por {instance.user.username} '
                f'(total: ${instance.total})'
            )
        )


# ── post_save: descontar stock ──
@receiver(post_save, sender=Order)
def update_stock_on_order(sender, instance, created, **kwargs):
    if created:
        Product.objects.filter(pk=instance.product_id).update(
            stock=F('stock') - instance.quantity
        )


# ── post_delete: restaurar stock ──
@receiver(post_delete, sender=Order)
def restore_stock_on_delete(sender, instance, **kwargs):
    Product.objects.filter(pk=instance.product_id).update(
        stock=F('stock') + instance.quantity
    )


# ── m2m_changed: log de tags ──
@receiver(m2m_changed, sender=Product.tags.through)
def log_tags_changed(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add' and pk_set:
        tag_names = Tag.objects.filter(pk__in=pk_set).values_list('name', flat=True)
        ActivityLog.objects.create(
            description=f'Tags agregados a "{instance.name}": {", ".join(tag_names)}'
        )
    elif action == 'post_remove' and pk_set:
        tag_names = Tag.objects.filter(pk__in=pk_set).values_list('name', flat=True)
        ActivityLog.objects.create(
            description=f'Tags removidos de "{instance.name}": {", ".join(tag_names)}'
        )


# ── Custom signal: pedido completado ──
@receiver(order_completed)
def on_order_completed(sender, order, user, **kwargs):
    ActivityLog.objects.create(
        description=f'Pedido #{order.pk} completado por {user.username}'
    )


@receiver(order_completed)
def notify_stock_low(sender, order, user, **kwargs):
    product = order.product
    product.refresh_from_db()
    if product.stock < 5:
        ActivityLog.objects.create(
            description=f'Stock bajo: {product.name} tiene solo {product.stock} unidades'
        )
```

---

## Estructura final de archivos

```
tienda/
├── management/
│   └── commands/
├── migrations/
├── __init__.py
├── apps.py              ← ready() importa signals
├── models.py            ← Product, Order, UserProfile, ActivityLog, Tag
├── signals.py           ← todos los receivers + custom signal
├── admin.py
├── urls.py
└── views.py
```

---

## Resumen

| Concepto | Detalle |
|----------|---------|
| `pre_save` | Se ejecuta **antes** de guardar. Ideal para calcular/modificar campos |
| `post_save` | Se ejecuta **después** de guardar. Ideal para crear objetos relacionados |
| `post_delete` | Se ejecuta **después** de eliminar. Ideal para restaurar/limpiar |
| `m2m_changed` | Se ejecuta al modificar relaciones ManyToMany |
| Custom signal | `Signal()` + `send()` para eventos de negocio personalizados |
| `created` | Parámetro de `post_save`: `True` = nuevo, `False` = actualización |
| `F()` | Operaciones atómicas en BD para evitar problemas de concurrencia |
| `apps.py` → `ready()` | **Obligatorio** para que los signals se conecten |
| `sender` | Filtra qué modelo dispara el signal |
| `@receiver` | Decorador que conecta una función a un signal |
