import traceback, sys

from django.shortcuts import render, redirect

from library.models import Book, Genre
from library.api.serializers.book import BookSerializer
from library.forms import BookForm

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser

@api_view(['GET'])
@permission_classes([AllowAny,])
def get_all_books(request):
    output = {}
    try:
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
    except:
        output['status'] = 'failed'
        output['status_text'] = 'Failed to fetch the books'
        return Response(output, status=status.HTTP_400_BAD_REQUEST)
    output['books'] = serializer.data
    output['status'] = 'success'
    output['status_text'] = "Successfully fetched all the books"
    return Response(output, status=status.HTTP_200_OK)

@api_view(['POST'])
@parser_classes([FormParser, MultiPartParser])
@permission_classes([AllowAny,])
def create_book(request):
    output = {}
    file = request.FILES['file']
    data = request.data
    try:
        title = data['title']
        genre = data['genre']
        try:
            genre, created = Genre.objects.get_or_create(name=genre)
            books = Book.objects.create(
                title=title,
                genre = genre,
                img=file
            )
            serializer = BookSerializer(books, many=True)
        except:
            traceback.print_exc(file=sys.stdout)
            output['status'] = 'failed'
            output['status_text'] = 'Failed to create the book'
            return Response(output, status=status.HTTP_400_BAD_REQUEST)
        output['books'] = serializer.data
        output['status'] = 'success'
        output['status_text'] = "Successfully created the book"
        return Response(output, status=status.HTTP_200_OK)
    except Exception as error:
        traceback.print_exc(file=sys.stdout)
        output['status'] = "failed"
        output['status_text'] = f"Ivalid data: {error}"
        return Response(output, status=status.HTTP_400_BAD_REQUEST)

def get_all_books_landing(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    form = BookForm()
    if books.exists():
        context = {
            "book_form": form,
            "books": serializer.data,
            "status": "success",
            "status_text": "Successfully fetched all the books"
        }
        return render(request, 'library/home.html', context)
    else:
        context = {
            "status": "failed",
            "status_text": "Failed to fetch the books"
        }
        return render(request, 'library/home.html', context)
    
def create_book_form(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

        context = {
            "status": "success",
            "status_text": "Successfully created the book"
        }

        return redirect('get_books_landing')
    
def view_or_update_book(request, pk):
    book = Book.objects.get(pk=pk)
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        print(form.errors)
        if form.is_valid():
            print("form is valid")
            form.save()
            return redirect('get_books_landing')
    else:
        form = BookForm(instance=book)

    context = {
        "status": "success",
        "status_text": "Successfully viewed the user",
        'books': serializer.data, 
        'book_update_form': form
    }
    return render(request, 'library/home.html', context)

def delete_book(request, pk):
    book = Book.objects.get(pk=pk)
    book.delete()
    return redirect('get_books_landing')
    
        