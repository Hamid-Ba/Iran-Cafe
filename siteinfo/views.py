"""
site info modules views
"""
from rest_framework import (generics)
from rest_framework.response import Response

from siteinfo.serializers import AboutUsSerializer
from siteinfo.models import (AboutUs)

class AboutUsView(generics.RetrieveAPIView):
    """About Us View"""
    serializer_class = AboutUsSerializer
    queryset = AboutUs.objects.all()

    def get(self, request):
        about_us = AboutUs.objects.first()
        serializer = AboutUsSerializer(about_us)
        return Response(serializer.data)