from django.contrib import admin
from .models import Device, DeviceNote, DeviceDocument

# Register your models here.
admin.site.register(Device)
admin.site.register(DeviceNote)  # Cihaz notlarını admin panelinden yönetmek için
admin.site.register(DeviceDocument)  # Cihaz belgelerini admin panelinden yönetmek için
