from django.urls import path
from core.views import (HomeView,
                        AddBookView,
                        add_book,
                        UpdateBookInventory,
                        BookInventory,
                        delete_book_inventory,
                        AboutView)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('add_book/', AddBookView.as_view(), name='add-book'),
    path('add/', add_book, name='add'),
    path('update_book/<int:book_id>/', UpdateBookInventory.as_view(), name='update-book'),
    path('books/inventory/', BookInventory.as_view(), name='all-book'),
    path('delete/inventory/<int:book_id>', delete_book_inventory, name='delete-book'),
    path('about', AboutView.as_view(), name='about')
]