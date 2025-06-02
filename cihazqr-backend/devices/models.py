from django.db import models
import os
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.utils.text import slugify
from datetime import datetime
import hashlib

# Create your models here.

class Device(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    brand = models.CharField(max_length=255, blank=True)
    model = models.CharField(max_length=255, blank=True)
    serial = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50, blank=True)
    last_maintenance = models.DateField(null=True, blank=True)
    qr_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hash_id = models.CharField(max_length=10, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Cihaz adı, seri no, marka ve model birleştirilip SHA256 ile hashlenir, ilk 10 karakter alınır.
        if not self.hash_id:
            base = f"{self.name or ''}{self.serial or ''}{self.brand or ''}{self.model or ''}"
            if not base:
                base = str(self.created_at)  # fallback
            hash_val = hashlib.sha256(base.encode()).hexdigest()[:10]
            self.hash_id = hash_val
        super().save(*args, **kwargs)

class DeviceNote(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='notes')
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Not: {self.note[:30]}... (Cihaz: {self.device.name})"

    # Bu model, cihazlara serbest formatta not eklemek için kullanılır.
    # Notlar cihaz detayında listelenir ve cihazdan silinirse notlar da silinir.

def device_document_upload_to(instance, filename):
    # Dosya adını cihaz adı, tarih ve rastgele bir ek ile oluşturur
    base, ext = os.path.splitext(filename)
    device_name = slugify(instance.device.name)
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"device_documents/{device_name}_{now}{ext}"

class DeviceDocument(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to=device_document_upload_to)
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Belge: {self.file.name} (Cihaz: {self.device.name})"

    # Bu model, cihazlara belge (PDF, resim, vs.) eklemek için kullanılır.
    # Belgeler cihaz detayında listelenir ve cihazdan silinirse belgeler de silinir.

# --- Dosya silindiğinde fiziksel dosyayı da silen sinyal ---
@receiver(post_delete, sender=DeviceDocument)
def delete_file_on_document_delete(sender, instance, **kwargs):
    # Belge silindiğinde dosya da fiziksel olarak silinir
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
