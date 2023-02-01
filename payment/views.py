from django.shortcuts import  get_object_or_404
from rest_framework.response import (Response)
from rest_framework import status , authentication
from rest_framework.views import APIView
from django.conf import settings

from payment.models import Payment
from plan.models import Plan
from config.permissions import HasCafe
from .zp import Zarinpal , ZarinpalError

zarin_pal = Zarinpal(settings.MERCHANT_ID,
                    settings.VERIFY_URL,
                    sandbox = True)

class MakePaymentView(APIView):
    """Making Payment View."""
    permission_classes = (HasCafe,)
    authentication_classes = (authentication.TokenAuthentication,)

    def post(self, request,plan_id, *args, **kwargs):
        try: cafe = self.request.user.cafe
        except :
            return Response({'detial' : 'شما قادر به خرید تعرفه نمی باشید'} , status=status.HTTP_400_BAD_REQUEST)
        
        plan = get_object_or_404(Plan,id=plan_id)
        desc = f'تعرفه {plan.title}'
        try:
            # try to create payment if success get url to redirect it
            redirect_url = zarin_pal.payment_request(int(plan.price.amount), desc, mobile=self.request.user.phone, email=None)

            payment = Payment.objects.create(cafe=cafe,plan=plan,pay_amount=plan.price,desc=desc,authority=zarin_pal.authority)
            payment.save()
            
            # redirect user to zarinpal payment gate to paid
            return Response({'detail' : redirect_url} , status=status.HTTP_200_OK)
            # return redirect(redirect_url)

        # if got error from zarinpal 
        except ZarinpalError as e:  
            return Response(e)