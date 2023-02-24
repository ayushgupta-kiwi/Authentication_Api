from django.contrib.auth import authenticate
from rest_framework import serializers
from .messages import Validation_Error, Error_Messages
from .models import Student_Info, Political_Leaders
from django.contrib.auth.hashers import make_password


class RegistrationSerializer(serializers.ModelSerializer):
    """
        Serializers registration requests and creates a new user.
    """
    first_name = serializers.CharField(max_length=20, min_length=3, required=True, trim_whitespace=False,
                                       error_messages=Validation_Error['first_name'])
    last_name = serializers.CharField(max_length=20, min_length=3, required=True, trim_whitespace=False,
                                      error_messages=Validation_Error['last_name'])
    contact = serializers.CharField(max_length=20, min_length=10, required=True, trim_whitespace=False,
                                    error_messages=Validation_Error['contact'])
    email = serializers.EmailField(required=True, trim_whitespace=False, error_messages=Validation_Error['email'])
    username = serializers.CharField(max_length=20, min_length=3, required=True, trim_whitespace=False,
                                     error_messages=Validation_Error['username'])
    password = serializers.CharField(max_length=20, min_length=8, write_only=True, required=True,
                                     trim_whitespace=False, error_messages=Validation_Error['password'])
    c_password = serializers.CharField(max_length=20, min_length=8, write_only=True, required=True,
                                       trim_whitespace=False, error_messages=Validation_Error['password'])

    def validate(self, data):
        """
            Object level validation to check weather the given field exist or not and to match passwords
        """
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        c_password = data.get('c_password')

        if Student_Info.objects.filter(username=username).exists():
            raise serializers.ValidationError(Validation_Error['username']['exist'])
        if Student_Info.objects.filter(email=email).exists():
            raise serializers.ValidationError(Validation_Error['email']['exist'])
        elif password != c_password:
            raise serializers.ValidationError(Validation_Error['password']['equal'])
        return data

    def validate_first_name(self, value):
        """
            Field level validation to validate first name
        """
        if not value:
            raise serializers.ValidationError(Validation_Error['first_name']['blank'])
        if ' ' in value:
            raise serializers.ValidationError(Validation_Error['first_name']['spaces'])
        if not value.isalpha():
            raise serializers.ValidationError(Validation_Error['first_name']['invalid'])
        return value

    def validate_last_name(self, value):
        """
            Field level validation to validate last name
        """
        if not value:
            raise serializers.ValidationError(Validation_Error['last_name']['blank'])
        if ' ' in value:
            raise serializers.ValidationError(Validation_Error['last_name']['spaces'])
        if not value.isalpha():
            raise serializers.ValidationError(Validation_Error['last_name']['invalid'])
        return value

    def validate_contact(self, attrs):
        """
            Field level validation to validate contact details
        """
        if attrs is None:
            raise serializers.ValidationError(Validation_Error['contact']['blank'])
        if not str(attrs).isdigit() or len(str(attrs)) != 10:
            raise serializers.ValidationError(Validation_Error['contact']['invalid'])
        if Student_Info.objects.filter(contact=attrs).exists():
            raise serializers.ValidationError(Validation_Error['contact']['exist'])
        return attrs

    def validate_username(self, value):
        """
            Field level validation to validate username
        """
        if value is None:
            raise serializers.ValidationError(Validation_Error['username']['blank'])
        if not value.isalnum() or ' ' in value:
            raise serializers.ValidationError(Validation_Error['username']['invalid'])
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError(Validation_Error['username']['invalid'])
        return value

    def validate_password(self, value):
        """
            Validate if password contains uppercase, lowercase, digit, space and special character.
        """
        if not any(char.isupper() for char in value) or not any(char.islower() for char in value) or \
                not any(char.isdigit() for char in value) or \
                not any(char in "!@#$%^&*()-_+=[]{};:'\"<>,.?/\\|" for char in value):
            raise serializers.ValidationError(Validation_Error['password']['value'])
        if " " in value:
            raise serializers.ValidationError(Validation_Error['last_name']['spaces'])
        return value

    def create(self, validated_data):
        """
            create function to create validated user data
        """
        stu = Student_Info.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            contact=validated_data['contact'],
            email=validated_data['email'],
            password=make_password(validated_data['password'])
        )
        return stu

    class Meta:
        """
            Metaclass of the Student Info model to display the fields of Registration serializer
        """
        model = Student_Info
        fields = ['id', 'first_name', 'last_name', 'email', 'contact',
                  'username', 'password', 'c_password']


class LoginSerializer(serializers.ModelSerializer):
    """
        Define a serializer for a login view in Django
    """
    username = serializers.CharField(max_length=20,min_length=3, required=True, trim_whitespace=False,
                                     error_messages=Validation_Error['username'])
    password = serializers.CharField(max_length=20, min_length=8, write_only=True, required=True,
                                     trim_whitespace=False, error_messages=Validation_Error['password'])

    def validate(self, data):
        """
            Validate if username or password is incorrect.
        """
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError(Error_Messages['Login']['bad_request'])

        data['user'] = user
        return data

    class Meta:
        """
            Metaclass of the Student Info model to display the fields of Login serializer
        """
        model = Student_Info
        fields = ['username', 'password']


class CreateSerializer(serializers.ModelSerializer):
    """
        Define a serializer for a display view in Django
    """
    name = serializers.CharField(max_length=30, min_length=3, required=True, trim_whitespace=False,
                                 error_messages=Validation_Error['name'])
    date_of_birth = serializers.DateField(required=True)
    date_of_death = serializers.DateField(required=True)
    place_of_birth = serializers.CharField(max_length=30, required=True)
    description = serializers.CharField(max_length=500, required=True)

    def validate_name(self, value):
        """
            Field level validation to validate name
        """
        if not value:
            raise serializers.ValidationError(Validation_Error['name']['blank'])
        if ' ' in value:
            raise serializers.ValidationError(Validation_Error['name']['spaces'])
        if not value.isalpha():
            raise serializers.ValidationError(Validation_Error['name']['invalid'])
        return value

    def create(self, validated_data):
        """
         override the create method to add custom behavior
        :param validated_data: validated data
        :return: user object
        """
        user = Political_Leaders.objects.create(**validated_data)
        return user

    class Meta:
        """
            Metaclass of the Student Info model to display the fields of UserProfile serializer
        """
        model = Political_Leaders
        fields = ['id', 'name', 'date_of_birth', 'date_of_death', 'place_of_birth', 'description']


class UpdateSerializer(serializers.ModelSerializer):
    """
        Define a serializer for a display view in Django
    """
    name = serializers.CharField(max_length=30, required=True, trim_whitespace=False,
                                 error_messages=Validation_Error["name"])
    date_of_birth = serializers.DateField(required=True)
    date_of_death = serializers.DateField(required=True)
    place_of_birth = serializers.CharField(max_length=30, required=True)
    description = serializers.CharField(max_length=500, required=True)

    def validate_name(self, value):
        """
            Field level validation to validate name
        """
        if not value:
            raise serializers.ValidationError(Validation_Error['name']['blank'])
        if ' ' in value:
            raise serializers.ValidationError(Validation_Error['name']['spaces'])
        if not value.isalpha():
            raise serializers.ValidationError(Validation_Error['name']['invalid'])
        return value

    def update(self, instance, validated_data):
        """
         override the create method to add custom behavior
        :param validated_data: validated data
        :return: user object
        """
        stu = Political_Leaders.objects.filter(id=instance.id).update(**validated_data)
        return stu

    class Meta:
        """
            Metaclass of the Political Leader model to display the fields of Update serializer
        """
        model = Political_Leaders
        fields = ['id', 'name', 'date_of_birth', 'date_of_death', 'place_of_birth', 'description']
