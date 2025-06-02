from django.shortcuts import render
from rest_framework import viewsets
from .models import Device, DeviceNote, DeviceDocument
from .serializers import DeviceSerializer, DeviceNoteSerializer, DeviceDocumentSerializer

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
