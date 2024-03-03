# models.py
from django.db import models
from rest_framework import serializers
from django.contrib.auth.models import User
from datetime import datetime


class User(models.Model):
    register_no = models.CharField(max_length=100,primary_key=True)
    student_name = models.CharField(max_length=100,default='a')
    password = models.CharField(max_length=100)
    # You can add other fields as needed

    def __str__(self):
        return self.register_no

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    department = models.CharField(max_length=100, default='all')
    publisher_name = models.CharField(max_length=255, default='')
    status = models.BooleanField(default=True)  # True for available, False for not available
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.IntegerField(default=1)
    ebook_url = models.CharField(max_length=300, default='')

    def __str__(self):
        return self.title
    
class RentalBook(models.Model):
    book_name = models.ForeignKey(Book, on_delete=models.CASCADE)
    register_no = models.ForeignKey(User, on_delete=models.CASCADE)

    # You can include additional fields if necessary
    rental_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()

    def __str__(self):
        return f"{self.book.title} - {self.user.username}"

class Notifications(models.Model):
    student_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_student')
    register_no = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_register')
    book_name = models.ForeignKey(Book, on_delete=models.CASCADE)
    current_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name}'s notification for {self.book_name} on {self.current_date}"