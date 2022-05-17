from django.contrib import admin

# Register your models here.
#admin panelinde gözükmesi için ekledik
from .models import *

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Order)
