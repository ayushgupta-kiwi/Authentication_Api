from django.contrib.auth.handlers.modwsgi import check_password
from rest_framework import serializers
from .constants import UserName, UserName1, Email, Password, Password1, REQUIRED, CONTACT, EXIST
from .models import Student_Info
from django.contrib.auth.hashers import make_password


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializers registration requests and creates a new user.
    """
    first_name = serializers.CharField(max_length=20, required=True)
    last_name = serializers.CharField(max_length=20, required=True)
    contact = serializers.CharField(max_length=10, min_length=10, required=True)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(max_length=10, required=True)
    password = serializers.CharField(max_length=20, min_length=8, write_only=True, required=True)
    c_password = serializers.CharField(max_length=20, min_length=8, write_only=True, required=True)

    class Meta:
        model = Student_Info
        fields = ['id', 'first_name', 'last_name', 'email', 'contact', 'username', 'password', 'c_password']

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        c_password = data.get('c_password')

        if Student_Info.objects.filter(username=username).exists():
            raise serializers.ValidationError(UserName1)
        elif Student_Info.objects.filter(email=email).exists():
            raise serializers.ValidationError(Email)
        elif password != c_password:
            raise serializers.ValidationError(Password1)
        return data

    def validate_contact(self, attrs):
        if attrs is None:
            raise serializers.ValidationError({'error': REQUIRED})
        if not str(attrs).isdigit() or len(str(attrs)) != 10:
            raise serializers.ValidationError({'error': CONTACT})
        if Student_Info.objects.filter(contact=attrs).exists():
            raise serializers.ValidationError({'error': EXIST})
        return attrs

    def create(self, validated_data):
        stu = Student_Info.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            contact=validated_data['contact'],
            email=validated_data['email'],
            password=make_password(validated_data['password'])
        )
        return stu


class LoginSerializer(serializers.ModelSerializer):
    """
        Define a serializer for a login view in Django
    """
    username = serializers.CharField(max_length=10, required=True)
    password = serializers.CharField(max_length=10, min_length=8, write_only=True, required=True)

    class Meta:
        model = Student_Info
        fields = ['username', 'password']

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        stu = Student_Info.objects.filter(username=username)
        if not stu:
            raise serializers.ValidationError({'error': UserName})
        if not check_password(password):
            raise serializers.ValidationError({'error': Password})
        return {
            'username': stu.username,
        }


class UserProfileSerializer(serializers.ModelSerializer):
    """
        Define a serializer for a display view in Django
    """

    class Meta:
        model = Student_Info
        fields = ['id', 'email', 'first_name', 'last_name', 'contact']
