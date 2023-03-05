from django.contrib import admin
from search.models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)
