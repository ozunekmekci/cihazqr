from rest_framework import serializers
from .models import Device, DeviceNote, DeviceDocument

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