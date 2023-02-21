from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from . import views

# Swagger Implementation
schema_view = get_schema_view(
    openapi.Info(
        title="Student Authentication",
        default_version='Student Details',
        description="This API is created to provide student details to perform CRUD functions for the Authenticated "
                    "user.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# Creating Router Object
router = DefaultRouter()

"""
    Register the views with the router
"""
router.register('register', views.StudentRegister, basename='register'),
router.register('login', views.StudentLogin, basename='login'),
router.register('listings', views.UserProfile, basename='listings')

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
    path('student/', include(router.urls)),
]
