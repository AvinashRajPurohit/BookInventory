from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views import View
import requests
from core.models import Books

'''
Solution Steps:
1. Integrate Google book api
2. keep track of books (number of copies)
list of all books in inventory
search for book using google book api (searched books available in inventory
 or not if yes than out of stock or not)
 
Add new book (write name of book google books api will
give you books after that add a new book which you want end enter the copies in your stock)

Update the copies of books.

Remove from the inventory  
'''


def get_books(q):
    data = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={q}')
    books = []
    if len(data.content) != 0:
        content = data.json().get('items')
        book_info = {}
        for book in content:
            book_info['title'] = book.get('volumeInfo',{}).get('title','')
            book_info['image'] = book.get('volumeInfo',{}).get('imageLinks',{}).get('thumbnail', '')
            book_info['description'] = book.get('volumeInfo',{}).get('description','')
            book_info['preview_link'] = book.get('volumeInfo',{}).get('previewLink', '')
            book_info['info_link'] = book.get('volumeInfo',{}).get('infoLink','')
            book_info['book_id'] = book.get('id')
            books.append(book_info)
            book_info = {}
    return books


class HomeView(View):
    def get(self, request):
        q = request.GET.get('q', None)
        books = Books.objects.all()
        if q is not None:
            books = get_books(q)

        context = {
            'books': books,
            'home': 'active'
        }
        return render(request, 'core/home.html', context)


class AddBookView(View):
    def get(self,request):
        q = request.GET.get('q', None)
        books = None
        if q is not None:
            books = get_books(q)

        context = {
            'books': books,
            'add_book': 'active'
        }
        return render(request, 'core/add_book.html', context)


def add_book(request):
    book_info = request.GET
    title = book_info.get('title', '')
    book_id = book_info.get('book_id', '')
    description = book_info.get('description', '')
    image = f'http://books.google.com/books/content?id={book_id}&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api '
    info_link = f"https://play.google.com/store/books/details?id={book_id}&source=gbs_api"
    preview_link = f"http://books.google.co.in/books?id={book_id}&printsec=frontcover&dq=flutter&hl=&cd=1&source=gbs_api"
    book = Books.objects.get_or_create(title=title,
                                image=image,
                                description=description,
                                preview_link=preview_link,
                                info_link=info_link,
                                book_id=book_id)
    messages.success(request, f"{book[0].title}'s has been added successfully")
    return redirect('update-book', book_id=book[0].id)


class UpdateBookInventory(View):

    def get(self, request, book_id):
        book = get_object_or_404(Books, id=book_id)
        context = {
            'book': book,
            'update': 'active'
        }
        return render(request, 'core/update_book_inventory.html', context)

    def post(self, request, book_id):
        book = get_object_or_404(Books, id=book_id)
        number = request.POST.get('copies', None)
        print(number)
        if number is not None:
            book.number_of_copies = int(number)
            book.save()
            messages.success(request, f"{book.title}'s inventory updated successfully")
            return redirect('update-book', book_id=book_id)
        context = {
            'book': book
        }
        return render(request, 'core/update_book_inventory.html', context)


class BookInventory(View):

    def get(self, request):
        books = Books.objects.all().order_by('-created')
        context = {
            'books': books,
            'update': 'active'
        }
        return render(request, 'core/all_books.html', context)


def delete_book_inventory(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    book.delete()
    messages.success(request, f"{book.title}'s inventory deleted successfully")
    return redirect('all-book')


class AboutView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AboutView, self).get_context_data(*args, **kwargs)
        context['about'] = 'active'
        return context
