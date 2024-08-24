from django.db import models
from django.utils import timezone
from datetime import timedelta

class Member(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    penalty_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def is_penalized(self):
        return self.penalty_until and self.penalty_until > timezone.now()

class Book(models.Model):
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    stock = models.IntegerField(default=1)

    def __str__(self):
        return self.title

class BorrowRecord(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)

    def is_overdue(self):
        return self.return_date and self.return_date > self.borrow_date + timedelta(days=7)
