import datetime

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Count

from bidding.models import Bidding
from product.models import Product, ProductImage, ProductSize

class BiddingDetailView(View):
    def get(self, request):
        try:
            product_id = request.GET.get("product_id")
            product = Product.objects.get(id=product_id)

            result = {
                'korean_name'       : product.korean_name,
                'english_name'      : product.english_name,
                'model_number'      : product.models_number,
                'best_color'        : product.best_color,
                'release_date'      : product.release_date,
                'release_price'     : round(product.release_price, 2),
                'brand'             : product.brand.name,
                'product_image_url' : product.productimage_set.all()[0].image_url,
                'recent_price'      : round(Bidding.objects.filter(status=2, product_size__product=product).order_by('update_at').first().price, 2),
                'direct_buy_price'  : round(Bidding.objects.filter(status=1, bidding_type =0, product_size__product=product).order_by('price').first().price, 2),
                'direct_sale_price' : round(Bidding.objects.filter(status=1, bidding_type =1, product_size__product=product).order_by('-price').first().price, 2),
                'bidded'            : [{
                    'bidded_size' : bidded_item.product_size.size.size,
                    'bidded_price': round(bidded_item.price, 2),
                    'bidded_date' : bidded_item.update_at.strftime('%y/%m/%d')
                } for bidded_item in Bidding.objects.filter(product_size__product=product, status_id=2).order_by('update_at')],
                'buy_bidding'       : [{
                    'buy_bidding_size'     : buy_bidding_item.product_size.size.size,
                    'buy_bidding_price'    : round(buy_bidding_item.price, 2),
                    'buy_bidding_quantity' : Bidding.objects.filter(price=buy_bidding_item.price, product_size=buy_bidding_item.product_size).aggregate(quantity=Count('id'))["quantity"]
                } for buy_bidding_item in Bidding.objects.filter(product_size__product=product, status=1, bidding_type=1)],
                'sale_bidding'       : [{
                    'sale_bidding_size'     : sale_bidding_item.product_size.size.size,
                    'sale_bidding_price'    : round(sale_bidding_item.price, 2),
                    'sale_bidding_quantity' : Bidding.objects.filter(price=sale_bidding_item.price, product_size=sale_bidding_item.product_size).aggregate(quantity=Count('id'))["quantity"]
                } for sale_bidding_item in Bidding.objects.filter(product_size__product=product, status=1, bidding_type=0)],
            }

            return JsonResponse({'result':result}, status=200)
        
        except Product.DoesNotExist:
            return JsonResponse({'message':'INVALID_PAGE'}, status=400)