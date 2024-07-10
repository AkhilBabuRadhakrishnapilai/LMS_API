from django.urls import path
from .views import *

urlpatterns = [
    path('login/',Login.as_view()),

    #books
    #get
    path('GET/api/books/',Books.as_view()),
    #post
    path('POST/api/books/',Books.as_view()),
    #update
    path('PUT/api/books/<int:id>/',Books.as_view()),
    #dele
    path('DELETE/api/books/<int:id>/',Books.as_view()),
    #retrive particular book
    path('GET/api/books/<int:id>/',ParticularBook.as_view()),


    #patrons
    path('GET/api/patrons/',Patrons.as_view()),
    path('POST/api/patrons/',Patrons.as_view()),
    path('PUT/api/patrons/<int:id>/',Patrons.as_view()),
    path('DELETE/api/patrons/<int:id>/',Patrons.as_view())
]