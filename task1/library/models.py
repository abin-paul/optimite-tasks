from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    library_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name} {self.library_id}"
    
    @property
    def rented(self):
        return self.book_set.all()

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    img = models.ImageField(upload_to='books')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    rented_by = models.ManyToManyField(User, blank=True)
    is_active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class RentalHistory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    rented_on = models.DateTimeField(auto_now_add=True)
    returned_on = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title}/{self.user.name}: {self.rented_on}"


