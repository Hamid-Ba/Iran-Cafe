from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from rest_framework.views import APIView
from rest_framework import mixins, viewsets
from django.conf import settings
from django.shortcuts import redirect
import datetime

from .models import Payment , StorePayment
from plan.models import Plan
from store.models import StoreOrder
from config.permissions import HasCafe
from .zp import Zarinpal, ZarinpalError
from .serializers import PaymentSerializer , StorePaymentSerializer
from . import pagination

zarin_pal = Zarinpal(settings.MERCHANT_ID, settings.VERIFY_URL, sandbox=True)
FRONT_VERIFY = settings.FRONT_VERIFY


class PlaceOrderView(APIView):
    """Making Payment View."""

    permission_classes = (HasCafe,)
    authentication_classes = (authentication.TokenAuthentication,)

    def post(self, request, plan_id, *args, **kwargs):
        try:
            cafe = self.request.user.cafe
        except:
            return Response(
                {"detial": "شما قادر به خرید تعرفه نمی باشید"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        plan = get_object_or_404(Plan, id=plan_id)
        desc = f"تعرفه {plan.title}"
        try:
            # try to create payment if success get url to redirect it
            redirect_url = zarin_pal.payment_request(
                int(plan.price.amount), desc, mobile=self.request.user.phone, email=None
            )

            payment = Payment.objects.create(
                cafe=cafe,
                plan=plan,
                pay_amount=plan.price,
                desc=desc,
                authority=zarin_pal.authority,
            )
            payment.save()

            # redirect user to zarinpal payment gate to paid
            return Response({"detail": redirect_url}, status=status.HTTP_201_CREATED)
            # return redirect(redirect_url)

        # if got error from zarinpal
        except ZarinpalError as e:
            return Response(e)


class VerifyOrderView(APIView):
    """Verify Order View"""

    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        try:
            res_data = request.query_params
            authority = res_data["Authority"]
        except ZarinpalError:
            return redirect(FRONT_VERIFY + "?status=NOK")

        payment = get_object_or_404(Payment, authority=authority)

        if res_data["Status"] != "OK":
            payment.status = 3
            payment.save()
            return redirect(FRONT_VERIFY + "?status=CANCELLED")
        try:
            code, message, ref_id = zarin_pal.payment_verification(
                int(payment.pay_amount.amount), authority
            )

            # everything is ok
            if code == 100:
                payment.ref_id = ref_id
                payment.is_payed = True
                payment.payed_date = datetime.datetime.now()
                payment.status = 2
                payment.save()
                
                return redirect(FRONT_VERIFY + "?status=OK&RefID=" + str(ref_id))
            # operation was successful but PaymentVerification operation on this transaction have already been done
            elif code == 101:
                return redirect(FRONT_VERIFY + "?status=PAYED")

        # if got an error from zarinpal
        except ZarinpalError:
            return redirect(FRONT_VERIFY + "?status=NOK")


class CafesPaymentsView(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """Cafe Payments View"""

    permission_classes = (HasCafe,)
    serializer_class = PaymentSerializer
    queryset = Payment.objects.order_by("-created_date")
    pagination_class = pagination.StandardPagination
    authentication_classes = (authentication.TokenAuthentication,)

    def get_serializer_context(self):
        context = {"request": self.request}
        return context

    def get_queryset(self):
        cafe = self.request.user.cafe
        return self.queryset.filter(cafe=cafe)


class PlaceStoreOrderView(APIView):
    """Making Store Payment View."""

    permission_classes = (HasCafe,)
    authentication_classes = (authentication.TokenAuthentication,)

    def post(self, request, order_id, *args, **kwargs):
        try:
            user = self.request.user
            cafe = self.request.user.cafe
        except:
            return Response(
                {"detial": "شما قادر به ثبت سفارش نمی باشید"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order = get_object_or_404(StoreOrder, id=order_id)
        desc = f"سفارش {str(order)}"
        try:
            # try to create payment if success get url to redirect it
            redirect_url = zarin_pal.payment_request(
                int(order.total_price.amount), desc, mobile=user.phone, email=None
            )

            payment = StorePayment.objects.create(
                cafe=cafe,
                user=user,
                order=order,
                pay_amount=order.total_price.amount,
                desc=desc,
                authority=zarin_pal.authority,
            )
            payment.save()

            # redirect user to zarinpal payment gate to paid
            return Response({"detail": redirect_url}, status=status.HTTP_201_CREATED)
            # return redirect(redirect_url)

        # if got error from zarinpal
        except ZarinpalError as e:
            return Response(e)

class VerifyStoreOrderView(APIView):
    """Verify Order View"""

    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        try:
            res_data = request.query_params
            authority = res_data["Authority"]
        except ZarinpalError:
            return redirect(FRONT_VERIFY + "?status=NOK")

        payment = get_object_or_404(StorePayment, authority=authority)

        if res_data["Status"] != "OK":
            payment.status = 3
            payment.save()
            return redirect(FRONT_VERIFY + "?status=CANCELLED")
        try:
            code, message, ref_id = zarin_pal.payment_verification(
                int(payment.pay_amount.amount), authority
            )

            # everything is ok
            if code == 100:
                payment.ref_id = ref_id
                payment.is_payed = True
                payment.payed_date = datetime.datetime.now()
                payment.status = 2
                payment.save()
                
                return redirect(FRONT_VERIFY + "?status=OK&RefID=" + str(ref_id))
            # operation was successful but PaymentVerification operation on this transaction have already been done
            elif code == 101:
                return redirect(FRONT_VERIFY + "?status=PAYED")

        # if got an error from zarinpal
        except ZarinpalError:
            return redirect(FRONT_VERIFY + "?status=NOK")
        
class CafesStorePaymentsView(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """Cafe Store Payments View"""

    permission_classes = (HasCafe,)
    serializer_class = StorePaymentSerializer
    queryset = StorePayment.objects.order_by("-created_date")
    pagination_class = pagination.StandardPagination
    authentication_classes = (authentication.TokenAuthentication,)

    def get_serializer_context(self):
        context = {"request": self.request}
        return context

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)