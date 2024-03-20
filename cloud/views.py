from rest_framework import generics, views, viewsets, status, response, authentication

from cloud import models, serializers
from config import permissions


class CloudyCustomerViewSet(
    generics.RetrieveAPIView, generics.CreateAPIView, viewsets.GenericViewSet
):
    permission_classes = [permissions.HasCafe]
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = serializers.CloudyCustomerSerializer
    queryset = models.CloudyCustomer.objects.all()

    def get_object(self):
        if models.CloudyCustomer.objects.filter(cafe=self.request.user.cafe).exists():
            cloud = models.CloudyCustomer.objects.filter(
                cafe=self.request.user.cafe
            ).first()
            return cloud

        return None

    def create(self, request, *args, **kwargs):
        if models.CloudyCustomer.objects.filter(cafe=self.request.user.cafe).exists():
            return response.Response(
                {"message": "درخواست شما قبلا ثبت شده است"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            return super().create(request, *args, **kwargs)

        return response.Response(
            {"message": "مشکلی در ارسال اطلاعات وجود دارد"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def perform_create(self, serializer):
        return serializer.save(cafe=self.request.user.cafe)
