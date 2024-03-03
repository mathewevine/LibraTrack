# views.py
from django.shortcuts import render
from .models import Book, User, RentalBook, Notifications
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie, csrf_protect
import json
from django.contrib import auth
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from datetime import datetime
from django.shortcuts import get_object_or_404

@method_decorator(csrf_protect, name='dispatch')
class CheckAuthenticatedView(APIView):
    def get(self, request, fomat=None):
        isAuthenticated = User.is_authenticated

        if isAuthenticated:
            return JsonResponse({'isAuthenticated': 'Success'})
        else:
            return JsonResponse({'isAuthenticated': 'Failed'})



@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        return JsonResponse({'success': 'CSRF cookie set'})



class LogoutView(APIView):
    def post(self, request, format=None):
        auth.logout(request)
        return JsonResponse({'message': 'Logged Out Successfully'})

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        register_no = data.get('registerNo')
        student_name = data.get('studentName')
        password = data.get('loginPassword')
        re_password = data.get('loginConfPassword')

        if password != re_password:
            return JsonResponse({'error': 'Password does not match'}, status=400)
        elif User.objects.filter(register_no=register_no).exists():
            return JsonResponse({'error': 'User with this registration number already exists'}, status=400)
        else:
        
            #hashed_password = make_password(password)
            # Save data to MySQL database
            # Example:
            user = User(register_no=register_no, password=password, student_name=student_name)
            user.save()
            return JsonResponse({'message': 'User registered successfully'}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def login_view(request):
    register_no = request.GET.get('register_no', None)
    #password = data.get('password')

    user = User.objects.get(register_no=register_no)
    data = {
                'register_no': user.register_no,
                'password': user.password,
                'student_name': user.student_name,
                # Add other fields as needed
            }
    return JsonResponse(data)
    # if user is not None:
    #     auth.login(request, user)
    #     return JsonResponse({'message': 'Login successful'})
    # else:
    #     return JsonResponse({'message': 'Invalid credentials'}, status=400)
    # else:
    #     return JsonResponse({'message': 'Method not allowed'}, status=405)


## Adding new Book
@csrf_exempt
def add_book(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("Received data:", data)
        book_id = data.get('bookId')
        title = data.get('title')
        author = data.get('author')
        department = data.get('department')
        publisher_name = data.get('publisherName')
        status = data.get('status')
        price = data.get('price')
        quantity = data.get('quantity')
        ebook_url = data.get('ebookURL')

        if title and author and publisher_name:
            # Create and save the book
            book = Book.objects.create(
                book_id=book_id,
                title=title,
                author=author,
                department=department,
                publisher_name=publisher_name,
                status=status,
                price=price,
                quantity=quantity,
                ebook_url=ebook_url
            )
            return JsonResponse({'message': 'Book added successfully!'}, status=201)
        else:
            return JsonResponse({'error': 'Missing fields'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

## Fetch all books

@csrf_exempt
def get_all_books(request):
    if request.method == 'GET':
        # Retrieve all books from the Book table
        books = Book.objects.all()

        # Serialize the queryset into JSON
        serialized_books = []
        for book in books:
            serialized_books.append({
                'book_id': book.book_id,
                'title': book.title,
                'author': book.author,
                'department': book.department,
                'publisher_name': book.publisher_name,
                'status': book.status,
                'price': book.price,
                'quantity': book.quantity,
                'ebook_url': book.ebook_url,
            })

        # Return the serialized books as JSON response
        return JsonResponse({'books': serialized_books}, safe=False)
    else:
        # If request method is not GET, return method not allowed
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def book_detail(request, book_id):
    book = Book.objects.get(pk=book_id)
    rental_records = Book.objects.filter(book=book)
    context = {
        'book': book,
        'rental_records': rental_records
    }
    return render(request, 'book_detail.html', context)

## Adding book to Rented books
#@csrf_exempt
# def rent_book(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        book_id = data.get('bookId')
        register_no = data.get('registerNo')

        try:
            book = Book.objects.get(book_id=book_id)
            user = User.objects.get(register_no=register_no)
        except Book.DoesNotExist:
            return JsonResponse({'error': 'Book not found'}, status=404)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        # Check if the book is already rented
        if RentalBook.objects.filter(book=book).exists():
            return JsonResponse({'error': 'Book is already rented'}, status=400)

        # Set rental_date to current date
        rental_date = datetime.now().date()

        # Set due_date to 7 days from today
        due_date = rental_date + timedelta(days=7)

        # Create RentalBook instance and save it
        rental_book = RentalBook(
            book=book,
            user=user,
            rental_date=rental_date,
            due_date=due_date
        )
        rental_book.save()

        return JsonResponse({'message': 'Book rented successfully'}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


## Get all users - 
@csrf_exempt
def get_all_users(request):
    if request.method == 'GET':
        # Retrieve all books from the Book table
        users = User.objects.all()

        # Serialize the queryset into JSON
        serialized_users = []
        index = 1
        for user in users:
            serialized_users.append({
                'S_No': index,
                'register_No': user.register_no,                
            })
            index += 1

        # Return the serialized books as JSON response
        return JsonResponse({'Users': serialized_users}, safe=False)
    else:
        # If request method is not GET, return method not allowed
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
## Get all Rented Books - 
@csrf_exempt
def get_all_rented_books(request):
    if request.method == 'GET':
        # Retrieve all books from the Book table
        rented_books = RentalBook.objects.all()

        # Serialize the queryset into JSON
        serialized_books = []
        for book_rental in rented_books:
            serialized_books.append({
                "book_id": book_rental.book_name.book_id,
                "book_title": book_rental.book_name.title,
                "user_id": book_rental.register_no.register_no,
                "user_name": book_rental.register_no.student_name,
                "rental_date": book_rental.rental_date.strftime("%d-%m-%Y"),
                "due_date": book_rental.due_date.strftime("%d-%m-%Y")
            })

        # Return the serialized books as JSON response
        return JsonResponse({'books': serialized_books}, safe=False)
    else:
        # If request method is not GET, return method not allowed
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
class DeleteAccountView(APIView):
    def delete(self, request, format=None):
        data = self.request.data

        user = User.objects.filter(register_no=data.register_no).delete()

        return JsonResponse({'message': 'User Removed Successfully'})
    
@csrf_exempt
def add_notification(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            register_no = data.get('register_no')
            book_id = data.get('book_id')  
            student_name = data.get('student_name')  

            # Retrieve user and book objects based on the provided data
            user = User.objects.get(register_no=register_no)
            book = Book.objects.get(book_id=book_id)

            # Create a new notification
            notification = Notifications.objects.create(
                student_name=user,
                register_no=user,
                book_name=book,
                current_date=datetime.now()
            )

            rented_book = RentalBook.objects.create(
                book_name=book,
                register_no=user,
                rental_date=datetime.now(),
                due_date = datetime.now() + timedelta(days=7)
            )
          
            return JsonResponse({'success': True, 'message': 'Book rented successfully. Please collect the book from the library.'})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User with the provided registration number does not exist.'}, status=400)
        except Book.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Book with the provided ID does not exist.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

def favicon_view(request):
    return HttpResponse(status=204)  # Respond with 204 No Content

@csrf_exempt
def get_all_notifications(request):
    if request.method == 'GET':
        # Retrieve all books from the Book table
        notifications = Notifications.objects.all()

        # Serialize the queryset into JSON
        serialized_notifications = []
        for notification in notifications:
            serialized_notifications.append({
                'student_name': notification.student_name.register_no,  # Assuming username is a field in the User model
                'register_no': notification.register_no.register_no,  # Assuming register_no is a field in the User model
                'book_name': notification.book_name.title,  # Assuming title is a field in the Book model
                'date': notification.current_date.strftime("%d-%m-%Y")
                })
        # Return the serialized books as JSON response
        return JsonResponse({'notifications': serialized_notifications}, safe=False)
    else:
        # If request method is not GET, return method not allowed
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
def reset_password(request, register_no):
    if request.method == 'PUT':
        try:
            user = get_object_or_404(User, register_no=register_no)
            # Change the user's password to '1234'
            user.password = '1234'
            user.save()
            return JsonResponse({'success': True, 'message': 'Password reset successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def delete_user(request, register_no):
    if request.method == 'DELETE':
        try:
            user = get_object_or_404(User, register_no=register_no)
            user.delete()
            return JsonResponse({'success': True, 'message': 'User deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
def update_user(request, register_no):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            user = get_object_or_404(User, register_no=register_no)
            # Change the user's password to '1234'
            user.student_name = data.get('studentName')
            user.password = data.get('password')
            user.save()
            return JsonResponse({'success': True, 'message': 'Password reset successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def update_book(request, book_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            book = get_object_or_404(Book, book_id=book_id)
            # Change the user's password to '1234'
            book.title = data.get('title')    
            book.author = data.get('author')
            book.department = data.get('department')
            book.publisher_name = data.get('publisherName')
            book.status = data.get('status')
            book.price = data.get('price')
            book.quantity = data.get('quantity')
            book.save()
            return JsonResponse({'success': True, 'message': 'Book Updated Successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
def delete_book(request, book_id):
    if request.method == 'DELETE':
        try:
            book = get_object_or_404(Book, book_id=book_id)
            book.delete()
            return JsonResponse({'success': True, 'message': 'Book deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
## Saving ebook pdf

def upload_ebook(request):
    if request.method == 'POST' and request.FILES['ebook']:
        ebook_file = request.FILES['ebook']
        # Handle saving the ebook file to the desired location
        # For example, using FileSystemStorage
        with open('path/to/save/ebook.pdf', 'wb') as f:
            for chunk in ebook_file.chunks():
                f.write(chunk)
        return JsonResponse({'message': 'Ebook uploaded successfully'}, status=200)
    else:
        return JsonResponse({'error': 'File upload failed'}, status=400)