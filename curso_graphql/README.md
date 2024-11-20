# Introducción a GraphQL en Django

## ¿Qué es GraphQL?
GraphQL es un lenguaje de consulta y manipulación de datos desarrollado por Facebook. A diferencia de REST, GraphQL permite a los clientes solicitar exactamente los datos que necesitan, nada más y nada menos. Esto resulta en:
- Menor uso de ancho de banda
- Menos round-trips al servidor
- Mayor flexibilidad para el cliente
- Documentación automática
- Tipado fuerte

## Ventajas de usar GraphQL en Django
1. **Consultas Flexibles**: Los clientes pueden solicitar exactamente los campos que necesitan
2. **Resolución Eficiente**: Django + Graphene optimiza automáticamente las consultas a la base de datos
3. **Tipado Fuerte**: Validación automática de tipos y documentación
4. **Una Única URL**: Todos los endpoints se consolidan en una única URL

## Componentes Principales
1. **Schema**: Define los tipos de datos y operaciones disponibles
2. **Types**: Representación de los modelos en GraphQL
3. **Queries**: Operaciones de lectura
4. **Mutations**: Operaciones de escritura
5. **Resolvers**: Funciones que definen cómo obtener los datos

## Caso Práctico: Sistema de Biblioteca
Implementaremos un sistema de gestión de biblioteca con:
- Autores
- Libros
- Relaciones entre ellos
- Operaciones CRUD
- Búsqueda avanzada

## Requisitos Previos
```bash
pip install django graphene-django
```

## Estructura del Proyecto
```
biblioteca/
├── manage.py
├── biblioteca/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── schema.py
└── libros/
    ├── __init__.py
    ├── models.py
    ├── schema.py
    └── migrations/
```

## Ejemplo
# models.py
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField()
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    description = models.TextField()
    publication_date = models.DateField()
    is_published = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.title

# schema.py
import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q

class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = ('id', 'name', 'email', 'bio', 'books')

class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'description', 'publication_date', 'is_published', 'price')

# Mutations
class CreateAuthor(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        bio = graphene.String()

    author = graphene.Field(AuthorType)
    
    def mutate(self, info, name, email, bio=""):
        author = Author.objects.create(
            name=name,
            email=email,
            bio=bio
        )
        return CreateAuthor(author=author)

class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author_id = graphene.ID(required=True)
        description = graphene.String()
        publication_date = graphene.Date(required=True)
        price = graphene.Decimal(required=True)
        is_published = graphene.Boolean()

    book = graphene.Field(BookType)
    
    def mutate(self, info, title, author_id, description="", publication_date=None, 
               price=0.0, is_published=False):
        author = Author.objects.get(pk=author_id)
        book = Book.objects.create(
            title=title,
            author=author,
            description=description,
            publication_date=publication_date,
            price=price,
            is_published=is_published
        )
        return CreateBook(book=book)

class Query(graphene.ObjectType):
    # Queries individuales
    author = graphene.Field(AuthorType, id=graphene.ID())
    book = graphene.Field(BookType, id=graphene.ID())
    
    # Queries de lista
    all_authors = graphene.List(AuthorType)
    all_books = graphene.List(BookType)
    
    # Búsqueda de libros
    search_books = graphene.List(
        BookType,
        search=graphene.String(),
        published_only=graphene.Boolean()
    )

    def resolve_author(self, info, id):
        return Author.objects.get(pk=id)

    def resolve_book(self, info, id):
        return Book.objects.get(pk=id)

    def resolve_all_authors(self, info):
        return Author.objects.all()

    def resolve_all_books(self, info):
        return Book.objects.all()
    
    def resolve_search_books(self, info, search="", published_only=False):
        queryset = Book.objects.all()
        
        if published_only:
            queryset = queryset.filter(is_published=True)
            
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(author__name__icontains=search)
            )
            
        return queryset

class Mutation(graphene.ObjectType):
    create_author = CreateAuthor.Field()
    create_book = CreateBook.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

# settings.py (añadir a INSTALLED_APPS)
INSTALLED_APPS = [
    ...
    'graphene_django',
    ...
]

GRAPHENE = {
    'SCHEMA': 'myapp.schema.schema'
}

# urls.py
from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]