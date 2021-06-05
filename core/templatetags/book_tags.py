from django import template
from django.shortcuts import get_object_or_404

from core.models import Books

register = template.Library()


@register.simple_tag
def return_out_of(book_id):
    book = Books.objects.filter(book_id=book_id)
    if book.count() != 0:
        if book[0].number_of_copies == 0:
            return "OUT OF STOCK"
        else:
            return f"Available Copies ({book[0].number_of_copies})"
    else:
        return "NOT AVAILABLE"
