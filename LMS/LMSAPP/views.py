from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse,HttpResponse
# Create your views here.

class Login(APIView):

    def post(self,request):
        user = UserSerializer(data = request.data)
        if user.is_valid():
            email = user.validated_data("email")
            password = user.validated_data("password")
            auth_user = authenticate(request,email=email,password=password)
            if auth_user is not None:
                token = Token.objects.get(user=auth_user)
                user = UserSerializer(auth_user).data
                response = {
                    "status":status.HTTP_200_OK,
                    "message":"success",
                    "data":{
                        "Token":token.key,
                        "user":user
                    }
                }
                return Response (response,status = status.HTTP_200_OK)
            else:
                response = {
                     "status":status.HTTP_401_UNAUTHORIZED,
                    "message":"Invalid Username or password",
                }
                return Response(response,status=status.HTTP_401_UNAUTHORIZED)
        else:
            response = {
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"Bad Request"
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        

class Books(APIView):
    def get(self,request):
        books_db = Book.objects.filter(is_active=True)
        books = BookSerializer(books_db,many=True)
        return JsonResponse(books.data,safe=False,status=200)
    
    def post(self,request):
        books = BookSerializer(data=request.data)
        if books.is_valid():
            books_obj = books.save()
            print(books_obj)
            return JsonResponse(books.data,safe=False,status=201)
        else:
            return JsonResponse(books.errors,status=400)
        
    def put(self,request,id):
        books = Book.objects.get(id=id)
        print("hey",books)
        books_ser = BookSerializer(books,data=request.data,partial=True)
        if books_ser.is_valid():
            books_ser.save()
            return JsonResponse(books_ser.data,status=201,safe=False)
        else:
            return JsonResponse(books_ser.errors,status=400)
    
    def delete(self,request,id):
        book = Book.objects.get(id=id)
        book.is_active = False
        book.save()
        return JsonResponse({"message: Deleted successfully"},status=status.HTTP_204_NO_CONTENT)
    
class ParticularBook(APIView):
    def get(self,request,id):
        book = Book.objects.get(id=id)
        book_ser = BookSerializer(book,many=True)
        return JsonResponse(book_ser.data,status=200)
    

class Patrons(APIView):
    def get(self,request):
        patrons = User.objects.all()
        patrons_ser = UserSerializer(patrons,many=True)
        return JsonResponse(patrons_ser.data,status=200,safe=False)
    
    def post(self,request):
        patrons = UserSerializer(data=request.data)
        if patrons.is_valid():
            patrons.save()
            return JsonResponse(patrons.data,status=True,safe=False)
        else:
            return JsonResponse(patrons.errors,status=400)
        
    def put(self,request,id):
        patrons = User.objects.get(id=id)
        patrons_ser = UserSerializer(patrons,data=request.data,partial=True)
        if patrons_ser.is_valid():
            return JsonResponse(patrons_ser.data,status=200,safe=False)
        else:
            return JsonResponse(patrons_ser.errors,status=400)
        
    def delete(self,request,id):
        patrons = User.objects.get(id=id)
        patrons.is_active = False
        patrons.save()
        return JsonResponse({"message: Deleted successfully"},status=status.HTTP_204_NO_CONTENT)

        
