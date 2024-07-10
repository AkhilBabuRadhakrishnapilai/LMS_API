from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin,Group,Permission
from django.dispatch import receiver
from .managers import UserManager
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token
# Create your models here.

class Roles(models.Model):
    role_name = models.CharField(max_length=50,null=False,blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.role_name
    
class User(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(max_length=20,null=False,blank=False)
    last_name = models.CharField(max_length=20,null=True,blank=True)
    email = models.EmailField(unique=True,blank=False,null=False,max_length=50)
    password = models.CharField(max_length=128,null=False,blank=False,default=first_name)
    address = models.CharField(max_length=100,null=False,blank=False)
    dob = models.DateField(null=False,blank=False)
    contact_number = models.CharField(max_length=10,null=False,blank=False)
    role = models.ForeignKey(Roles,on_delete=models.CASCADE,related_name="roles")
    is_staff = models.BooleanField()
    is_active=models.BooleanField(default=True)
    created_date = models.DateField(auto_now_add=True,null=False)
    groups = models.ManyToManyField(Group,related_name='custom_user_groups',blank=True)
    user_permissions = models.ManyToManyField(Permission,related_name='custom_user_permissions',blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['first_name','last_name','dob','password','is_staff']

    def __str__(self):
        return self.first_name


class Book(models.Model):
    title = models.CharField(max_length=100,null=False,blank=False)
    description = models.CharField(max_length=100,null=True,blank=False)
    author = models.CharField(max_length=100,null=False,blank=False)
    genre = models.CharField(max_length=50,null=False,blank=False)
    pubslished_date = models.DateField(null=False,blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class BorrowingHistory(models.Model):
    user = models.ForeignKey(User,null=False,blank=False,related_name="users",on_delete=models.CASCADE)
    book = models.ForeignKey(Book,null=False,blank=False,related_name="books",on_delete=models.CASCADE)
    date_taken = models.DateField(null=True,blank=True)
    returned_date = models.DateField(null=True,blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.first_name} borrowed {self.book.title}" 

class Reservation(models.Model):
    user=models.ForeignKey(User,related_name="userz",on_delete=models.CASCADE)
    book = models.ForeignKey(Book,related_name="bookz",on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.user.first_name


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)