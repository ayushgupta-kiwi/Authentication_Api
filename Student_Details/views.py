# Create your views here.
from django.contrib import auth
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Student_Info
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import RegistrationSerializer, LoginSerializer, UserProfileSerializer
from .constants import INVALID, REGISTER, LOGIN, DATA_CREATED, DATA_NOT_UPDATED, DATA_DELETED


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


class StudentRegister(viewsets.ModelViewSet):
    """
        To Register the Validated User
    """
    queryset = Student_Info
    serializer_class = RegistrationSerializer
    http_method_names = ['post']

    def get_queryset(self):
        """
        The get_queryset method returns a queryset of Student Model objects.
        """
        return Student_Info.objects.filter()

    def create(self, request, *args, **kwargs):
        """
        Creates a new instance of the Student model.
        """
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response({'message': REGISTER}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class StudentLogin(viewsets.ModelViewSet):
    queryset = Student_Info
    serializer_class = LoginSerializer
    http_method_names = ['post']

    def get_queryset(self):
        """
        The get_queryset method returns a queryset of Student Model objects.
        """
        return Student_Info.objects.filter()

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            token = get_token_for_user(user)
            return Response({'token': token, 'message': LOGIN}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'message': INVALID}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfile(viewsets.ModelViewSet):
    """
        Display the listing of the Student Data for Authenticated User
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_queryset(self, pk=None):
        return Student_Info.objects.filter().order_by('id')

    def list(self, request, *args, **kwargs):
        """
            Display the instances of the Student.
        """
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
            Display the single instance of the Student.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
            Create an instance of the Student.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': DATA_CREATED}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
            Update the instances of the Student.
        """
        stu = self.get_object()
        serializer = self.get_serializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.update(stu, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'msg': DATA_NOT_UPDATED}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """
            Update the partial instances of the Student.
        """
        stu = self.get_object()
        serializer = self.get_serializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(stu, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'msg': DATA_NOT_UPDATED}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
            Delete the selected Student instance.
        """
        stu = self.get_object()
        stu.delete()
        return Response({'msg': DATA_DELETED})

