"""
site info modules views
"""
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import (generics)
from rest_framework.response import Response

from siteinfo.serializers import AboutUsSerializer, ContactUsSerializer
from siteinfo.models import (AboutUs, ContactUs , Robots)

class AboutUsView(generics.RetrieveAPIView):
    """About Us View"""
    serializer_class = AboutUsSerializer
    queryset = AboutUs.objects.all()

    def get(self, request):
        about_us = AboutUs.objects.first()
        serializer = AboutUsSerializer(about_us)
        return Response(serializer.data)

class ContactUsView(generics.CreateAPIView):
    """Contact Us View"""
    serializer_class = ContactUsSerializer

class RobotsView(View):
    """Robots View"""
    def get(self, request):
        robot = get_object_or_404(Robots, pk=1)
        return HttpResponse(robot.text,content_type='text/plain')