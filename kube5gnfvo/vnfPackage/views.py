from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import *
from .serializers import *
import  json


class VnfPkgInfoView(viewsets.ModelViewSet):
    queryset = VnfPkgInfo.objects.all()
    serializer_class = VnfPkgInfoSerializer

    def create(self, request, **kwargs):
        if (request.data.get('userDefinedData') != None):
            request.data['userDefinedData'] = json.dumps(request.data['userDefinedData'])

        request.data['_links'] = {
            'self': request.build_absolute_uri(),
            'vnfd': request.build_absolute_uri(),
            'packageContent': request.build_absolute_uri()
        }

        return super().create(request)
