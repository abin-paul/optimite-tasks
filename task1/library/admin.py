from django.contrib import admin
from library.models import User, Book, Genre, RentalHistory

admin.site.register(User)
admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(RentalHistory)
