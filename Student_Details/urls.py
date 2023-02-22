from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


# Creating Router Object
router = DefaultRouter()

"""
    Register the views with the router
"""
router.register('register', views.StudentRegister, basename='register'),
router.register('login', views.StudentLogin, basename='login'),
router.register('listings', views.UserProfile, basename='listings')

urlpatterns = [
    path('student/', include(router.urls)),
]
