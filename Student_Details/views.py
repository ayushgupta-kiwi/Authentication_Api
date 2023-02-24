# Create your views here.
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Student_Info, Political_Leaders
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import RegistrationSerializer, LoginSerializer, CreateSerializer, UpdateSerializer
from .messages import Error_Messages


class StudentRegister(viewsets.ModelViewSet):
    """
        To Register the Validated User
    """
    queryset = Student_Info
    serializer_class = RegistrationSerializer
    http_method_names = ['post']

    def get_queryset(self):
        """
        The get_queryset method returns a queryset of Student_Info Model objects.
        """
        return Student_Info.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Creates a new instance of the Student_Info model.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(Error_Messages['Registration']['success'], status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentLogin(viewsets.ModelViewSet):
    queryset = Student_Info
    serializer_class = LoginSerializer
    http_method_names = ['post']

    def get_queryset(self):
        """
        The get_queryset method returns a queryset of Student_Info Model objects.
        """
        return Student_Info.objects.filter()

    def create(self, request, *args, **kwargs):
        """
        Allows only valid user to login.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh token': str(refresh),
                'access token': str(refresh.access_token),
                'message': Error_Messages['Login']['success'],
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class UserProfile(viewsets.ModelViewSet):
    """
        Display the listing of the Student Data for Authenticated User
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list', 'create']:
            return CreateSerializer
        return UpdateSerializer

    def get_queryset(self):
        return Political_Leaders.objects.filter().order_by('id')

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
            serializer.create(serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
            Update the instances of the Student.
        """
        stu = self.get_object()
        serializer = self.get_serializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.update(stu, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """
            Update the partial instances of the Student.
        """
        stu = self.get_object()
        serializer = self.get_serializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(stu, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
            Delete the selected Student instance.
        """
        stu = self.get_object()
        stu.delete()
        return Response(status=status.HTTP_200_OK)
