from django.contrib import admin
from .models import Student_Info


# Register the Student_Info model with the admin site
@admin.register(Student_Info)
class DetailsAdmin(admin.ModelAdmin):
    """
        Define which fields to display in the list view of the admin page
    """
    list_display = ('id', 'first_name', 'last_name', 'username', 'email', 'contact', 'password')
