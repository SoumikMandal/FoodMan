from django.contrib import admin
from .models import Company, MenuItem, partners

admin.site.register(partners)
admin.site.register(Company)
admin.site.register(MenuItem)