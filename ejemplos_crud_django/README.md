# models.py
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    
    def __str__(self):
        return self.title

# views.py
from django.shortcuts import get_object_or_404
from .models import Book

def create_book(title, author, publication_date, isbn):
    book = Book.objects.create(
        title=title,
        author=author,
        publication_date=publication_date,
        isbn=isbn
    )
    return book

def get_all_books():
    return Book.objects.all()

def get_book_by_id(book_id):
    return get_object_or_404(Book, id=book_id)

def update_book(book_id, **kwargs):
    book = get_object_or_404(Book, id=book_id)
    for key, value in kwargs.items():
        setattr(book, key, value)
    book.save()
    return book

def delete_book(book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()

# Ejemplo de uso
from datetime import date

# Create
new_book = create_book(
    title="Django for Beginners",
    author="William S. Vincent",
    publication_date=date(2020, 1, 1),
    isbn="1234567890123"
)
print(f"Nuevo libro creado: {new_book}")

# Read
all_books = get_all_books()
print(f"Todos los libros: {all_books}")

book = get_book_by_id(new_book.id)
print(f"Libro obtenido por ID: {book}")

# Update
updated_book = update_book(new_book.id, title="Django for Professionals")
print(f"Libro actualizado: {updated_book}")

# Delete
delete_book(new_book.id)
print("Libro eliminado")

# Verificar que el libro fue eliminado
try:
    get_book_by_id(new_book.id)
except:
    print("El libro ya no existe en la base de datos")
