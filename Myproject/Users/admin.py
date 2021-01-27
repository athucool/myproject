from django.contrib import admin
# from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import UserLoginHistory
 

@admin.register(UserLoginHistory)
class Useradmin(ImportExportModelAdmin):
    list_display=("username","ip")

