from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

import datetime
from books.models import Book
from books.converters import PubDateConverter

def books_view(request, pub_date=None):
    template = 'books/books_list.html'
    all_books = Book.objects.all()
    list_of_date_books = sorted(list(set([PubDateConverter().to_python(book.pub_date) for book in all_books])))
    if pub_date == None:
        context = {
            'books': Book.objects.all()
        }
    else:
        pub_date = datetime.datetime.strptime(pub_date, '%Y-%m-%d').date()
        ind = list_of_date_books.index(pub_date)
        if ind > 0 and ind < len(list_of_date_books)-1:
            pre = PubDateConverter().to_url(list_of_date_books[ind-1])
            next = PubDateConverter().to_url(list_of_date_books[ind+1])
        elif ind == 0 and ind < len(list_of_date_books)-1:
            pre = None
            next = PubDateConverter().to_url(list_of_date_books[ind+1])
        else:
            pre = PubDateConverter().to_url(list_of_date_books[ind-1])
            next = None
        context = {
            'books': Book.objects.filter(pub_date__exact=pub_date).order_by('pub_date'),
            'pre' : pre,
            'next' : next
        }
    return render(request, template, context)
