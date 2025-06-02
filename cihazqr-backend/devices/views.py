from django.shortcuts import render
from rest_framework import viewsets
from .models import Device, DeviceNote, DeviceDocument, FaultRecord, FaultDocument
from .serializers import DeviceSerializer, DeviceNoteSerializer, DeviceDocumentSerializer, FaultRecordSerializer, FaultDocumentSerializer

# Create your views here.

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    lookup_field = 'hash_id'  # Artık cihazlar hash_id ile sorgulanacak

class DeviceNoteViewSet(viewsets.ModelViewSet):
    queryset = DeviceNote.objects.all()
    serializer_class = DeviceNoteSerializer
    filterset_fields = ['device']  # Sadece ilgili cihaza ait notlar
    # Bu ViewSet, cihaz notlarını eklemek, listelemek ve silmek için kullanılır.

class DeviceDocumentViewSet(viewsets.ModelViewSet):
    queryset = DeviceDocument.objects.all()
    serializer_class = DeviceDocumentSerializer
    filterset_fields = ['device']  # Sadece ilgili cihaza ait belgeler
    # Bu ViewSet, cihaz belgelerini eklemek, listelemek ve silmek için kullanılır.

# Arıza kayıtları için ViewSet
from rest_framework import filters
class FaultRecordViewSet(viewsets.ModelViewSet):
    queryset = FaultRecord.objects.all()
    serializer_class = FaultRecordSerializer
    filterset_fields = ['device', 'status', 'isleme_baslama_tarihi', 'sorumlu_personel']
    search_fields = ['title', 'ariza_tanimi', 'sorumlu_personel']
    ordering_fields = ['created_at', 'isleme_baslama_tarihi']
    # Bu ViewSet, arıza kayıtlarını ekleme, listeleme, güncelleme ve silme işlemleri için kullanılır.

# Arıza kaydı ek belgeleri için ViewSet
class FaultDocumentViewSet(viewsets.ModelViewSet):
    queryset = FaultDocument.objects.all()
    serializer_class = FaultDocumentSerializer
    filterset_fields = ['fault_record']
    # Bu ViewSet, arıza kaydına ait belgeleri eklemek, listelemek ve silmek için kullanılır.
