from django.contrib import admin

# Register your models here.


from .models import *

admin.site.register(Etl_table)
admin.site.register(Etl_load)
admin.site.register(Etl_table_property)
