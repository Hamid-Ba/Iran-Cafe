"""
Iran Cafe Query Views
"""
from rest_framework import (permissions , authentication ,status ,views)
from rest_framework.response import Response
from cafe.models import MenuItem, Order
from django.db.models import Sum

from config.permissions import HasCafe
from queries.pagination import StandardPagination

class OrderQueryView(views.APIView):
    """Order Query View"""
    permission_classes = [permissions.IsAuthenticated , HasCafe]
    authentication_classes = [authentication.TokenAuthentication]    

    def get(self, request, *args, **kwargs):
        """Get Action"""
        res = {}
        orders = Order.objects.filter(cafe=request.user.cafe)
        items = MenuItem.objects.filter(cafe=request.user.cafe).order_by('-order_count')[:3]

        try :
            if request.query_params['start_date'] :
                start_date = request.query_params.get('start_date', None)
                orders = orders.filter(registered_date__gte=start_date)
        except : None

        try :
            if request.query_params['end_date'] :
                end_date = request.query_params.get('end_date', None)
                orders = orders.filter(registered_date__lte=end_date)
        except : None

        # Process On Query
        res = orders.aggregate(total_prices = Sum('total_price'))
        res['most_purchesd'] = items.values()
        paginator = StandardPagination()
        res['orders'] = paginator.paginate_queryset(orders.values(), request)
        # Calculate Most Item Purchesd
        # items = items.order_by('-count').values()
        # most_purchesd_item = {}
        # for item in items:
        #     if item['menu_item_id'] in most_purchesd_item.keys(): most_purchesd_item[item['menu_item_id']] += item['count']
        #     else : most_purchesd_item[item['menu_item_id']] = item['count']
        
        
        # if most_purchesd_item :
        #     most_purchesd_item_id = list(most_purchesd_item)[:3]
        #     for item_id in most_purchesd_item_id:
        #         item = items.filter(menu_item_id=item_id).first()
        #         item['count'] = most_purchesd_item[item_id]
        #         res['most_purchesd'].append(item)
                
        return Response(res ,status=status.HTTP_200_OK)