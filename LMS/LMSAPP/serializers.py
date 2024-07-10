from rest_framework import serializers
from .models import *
#login
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password= serializers.CharField(max_length=128,write_only=True)
    role = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ['email','password','role']

class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    #roles
    role = RolesSerializer(read_only = True)
    role_id = serializers.PrimaryKeyRelatedField(queryset = Roles.objects.all())
    class Meta:
        model = User
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BorrowingHistorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    book = BookSerializer(read_only = True)
    class Meta:
        model = BorrowingHistory
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    book = BookSerializer(read_only = True)
    class Meta:
        model= Reservation
        fields = '__all__'