from rest_framework import serializers
from .models import Device, DeviceNote, DeviceDocument, FaultRecord, FaultDocument

class DeviceNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceNote
        fields = ['id', 'device', 'note', 'created_at']
        # Bu serializer, cihaz notlarını API'de göstermek için kullanılır.

class DeviceDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceDocument
        fields = ['id', 'device', 'file', 'description', 'uploaded_at']
        # device alanı eklendi! Böylece belge eklerken cihaz id'si de işlenir ve NOT NULL hatası alınmaz.

class DeviceSerializer(serializers.ModelSerializer):
    notes = DeviceNoteSerializer(many=True, read_only=True)
    documents = DeviceDocumentSerializer(many=True, read_only=True)
    class Meta:
        model = Device
        fields = [
            'id', 'hash_id', 'name', 'description', 'brand', 'model', 'serial', 'location', 'status',
            'last_maintenance', 'qr_url', 'created_at', 'notes', 'documents'
        ]
        # notes ve documents alanları, cihaz detayında ilişkili not ve belgeleri göstermek için eklendi. 

# Arıza kaydı ek belgeleri için serializer
class FaultDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaultDocument
        fields = '__all__'

# Gelişmiş arıza kaydı serializer'ı
class FaultRecordSerializer(serializers.ModelSerializer):
    documents = FaultDocumentSerializer(many=True, read_only=True)
    class Meta:
        model = FaultRecord
        fields = [
            'id', 'device', 'title', 'sira_no', 'isleme_baslama_tarihi',
            'sorumlu_personel', 'ariza_tanimi', 'ariza_turu',
            'ariza_nedeni_tahmini', 'ariza_nedeni_kesin',
            'yapilan_isler_sonuclar', 'kullanilan_parcalar',
            'dis_servis_bilgileri', 'teslim_eden_kisi', 'teslim_eden_tarih_saat',
            'teslim_alan_kisi', 'teslim_alan_tarih_saat', 'status',
            'created_by', 'updated_by', 'created_at', 'updated_at',
            'documents'
        ]
        read_only_fields = ['created_at', 'updated_at']