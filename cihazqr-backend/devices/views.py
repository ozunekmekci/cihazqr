from django.shortcuts import render
from rest_framework import viewsets
from .models import Device, DeviceNote, DeviceDocument
from .serializers import DeviceSerializer, DeviceNoteSerializer, DeviceDocumentSerializer

# Create your views here.

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class DeviceNoteViewSet(viewsets.ModelViewSet):
    queryset = DeviceNote.objects.all()
    serializer_class = DeviceNoteSerializer
    # Bu ViewSet, cihaz notlarını eklemek, listelemek ve silmek için kullanılır.

class DeviceDocumentViewSet(viewsets.ModelViewSet):
    queryset = DeviceDocument.objects.all()
    serializer_class = DeviceDocumentSerializer
    # Bu ViewSet, cihaz belgelerini eklemek, listelemek ve silmek için kullanılır.
