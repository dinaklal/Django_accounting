from django.contrib import admin

# Register your models here.
from company.models import Company,DelNote,Rate

admin.site.register(Company)
admin.site.register(DelNote)
admin.site.register(Rate)