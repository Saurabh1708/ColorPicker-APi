from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from basic.models import Picker
from django.views.generic import View, TemplateView, ListView, DetailView, UpdateView, DeleteView, CreateView
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework import viewsets
from basic.serializers import PickerSerializer
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from colorthief import ColorThief
from PIL import Image
import requests

class PickerViewSet(viewsets.ModelViewSet):
    serializer_class=PickerSerializer
    queryset=Picker.objects.all()


class IndexView(TemplateView):
    template_name='index.html'


@api_view(['GET', 'POST'])
def color_picker_view(request):
    if request.method=='GET':
        images=Picker.objects.all()
        serializer=PickerSerializer(images, many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        data={'url': request.DATA.get('url')}
        serializer=PickerSerializer(data=data)
        if serializer.is_valid():
            img=Image.open(requests.get(data, stream=True).raw)
            img_copy=img.copy()
            img.thumbnail((150,150))
            color_thief=ColorThief()
            dom_color=color_thief.get_color(quality=1)
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
