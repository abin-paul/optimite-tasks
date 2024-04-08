from django.urls import path
from library.api.views.crud_book import get_all_books, get_all_books_landing, create_book, create_book_form, view_or_update_book, delete_book
from library.api.views.crud_users import get_all_users, get_all_user_landing, view_or_update_user, create_user_form, delete_user

urlpatterns = [
    path('', get_all_books_landing, name='get_books_landing'),
    path('get-books', get_all_books, name='get_books'),
    path('create-book', create_book, name='create_book'),
    path('create-book-form', create_book_form, name='create_book_form'),
    path('view-or-update-book/<int:pk>/', view_or_update_book, name='view_or_update_book'),
    path('delete-book/<int:pk>/', delete_book, name='delete_book'),

    path('users-landing', get_all_user_landing, name='get_users_landing'),
    path('get-users', get_all_users, name='get_users'),
    path('create-user-form', create_user_form, name='create_user_form'),
    path('view-or-update-user/<int:pk>/', view_or_update_user, name='view_or_update_user'),
    path('delete-user/<int:pk>/', delete_user, name='delete_user'),
]
