from django.contrib import admin
from .models import Student_Info, Political_Leaders


# Register the Student_Info model with the admin site
@admin.register(Student_Info)
class DetailsAdmin(admin.ModelAdmin):
    """
        Define which fields to display in the list view of the admin page
    """
    list_display = ('id', 'first_name', 'last_name', 'username', 'email', 'contact', 'password')


@admin.register(Political_Leaders)
class LeaderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_of_birth', 'date_of_death', 'place_of_birth', 'description')
