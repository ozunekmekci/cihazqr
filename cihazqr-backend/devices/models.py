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

# --- Arıza Türü için seçenekler ---
ARIZA_TURU_CHOICES = [
    ('mekanik', 'Mekanik Arıza'),
    ('elektrik', 'Elektriksel Arıza'),
    ('elektronik', 'Elektronik Kart Arızası'),
    ('yazilim', 'Yazılımsal Sorun'),
    ('kullanici', 'Kullanıcı Hatası'),
    ('kalibrasyon', 'Kalibrasyon Gereksinimi'),
    ('sarf_malzeme', 'Sarf Malzeme Bitti/Değişimi'),
    ('periyodik_bakim', 'Periyodik Bakım'),
    ('diger', 'Diğer'),
]

# --- Gelişmiş Arıza Kayıt Modeli ---
# Arıza süreçlerinin tüm detaylarını ve ek belgeleri tutar.
class FaultRecord(models.Model):
    STATUS_CHOICES = [
        ("open", "Açık - Atanmadı"),
        ("assigned", "Atandı - Müdahale Bekliyor"),
        ("in_progress", "İşlemde - Müdahale Ediliyor"),
        ("on_hold", "Beklemede - Parça/Onay Bekliyor"),
        ("resolved", "Çözüldü - Test Edilecek"),
        ("closed", "Kapalı - Kullanıma Verildi"),
        ("cancelled", "İptal Edildi"),
    ]
    device = models.ForeignKey('Device', on_delete=models.CASCADE, related_name='faults')
    title = models.CharField(max_length=255)
    sira_no = models.CharField(max_length=50, blank=True, null=True)
    isleme_baslama_tarihi = models.DateTimeField(blank=True, null=True)
    sorumlu_personel = models.CharField(max_length=255, blank=True)
    ariza_tanimi = models.TextField(blank=True)
    ariza_turu = models.CharField(max_length=50, choices=ARIZA_TURU_CHOICES, blank=True)
    ariza_nedeni_tahmini = models.TextField(blank=True)
    ariza_nedeni_kesin = models.TextField(blank=True)
    yapilan_isler_sonuclar = models.TextField(blank=True)
    kullanilan_parcalar = models.TextField(blank=True)  # JSONField önerilir, şimdilik TextField
    dis_servis_bilgileri = models.TextField(blank=True) # JSONField önerilir, şimdilik TextField
    teslim_eden_kisi = models.CharField(max_length=255, blank=True)
    teslim_eden_tarih_saat = models.DateTimeField(blank=True, null=True)
    teslim_alan_kisi = models.CharField(max_length=255, blank=True)
    teslim_alan_tarih_saat = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    created_by = models.CharField(max_length=255, blank=True)  # User FK önerilir, şimdilik CharField
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.device.name} - {self.title} ({self.get_status_display()})"

# --- Arıza Kaydı Ek Belgeleri için Model ---
# Her arıza kaydına birden fazla dosya eklenmesini sağlar.
def fault_document_upload_to(instance, filename):
    from django.utils.text import slugify
    from datetime import datetime
    base, ext = os.path.splitext(filename)
    fault_title = slugify(instance.fault_record.title)
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"fault_documents/{fault_title}_{now}{ext}"

class FaultDocument(models.Model):
    fault_record = models.ForeignKey(FaultRecord, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to=fault_document_upload_to)
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # uploaded_by = models.CharField(max_length=255, blank=True)  # User FK önerilir

    def __str__(self):
        return f"Belge: {self.file.name} (Arıza: {self.fault_record.title})"
