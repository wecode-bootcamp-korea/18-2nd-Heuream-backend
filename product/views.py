from django.views import View
from django.http  import JsonResponse
from django.db.models import Min, Q, Prefetch, Count

from product.models import Product, ProductImage, ProductSize, Brand, BrandLine
from bidding.models import Bidding, Status
from account.models import User, Wishlist
from account.utils  import login_check

class ProductFilterView(View):
    @login_check
    def get(self, request):
        try:
            search     = request.GET.get('q')
            brand      = request.GET.getlist('brand')
            brand_line = request.GET.getlist('brand_line')
            subline    = request.GET.getlist('subline')
            size       = request.GET.getlist('size')
            sort       = request.GET.get('sort', 'Popular')
            user_id    = request.user.id if request.user else None

            OFFSET = int(request.GET.get('limit', 20)) * int(request.GET.get('offset', 0))
            LIMIT  = int(request.GET.get('limit', 20)) + OFFSET

            filter = {}
            if brand:
                filter['brand__in'] = brand
            if brand_line:
                filter['brand_line__in'] = brand_line
            if subline:
                filter['subline__in'] = subline
            if size:
                filter['size__id__in'] = size
            
            search_list = []
            if search:
                search_list.append(
                    Q(korean_name__icontains=search)|
                    Q(english_name__icontains=search)|
                    Q(models_number__icontains=search)|
                    Q(brand__name__icontains=search)|
                    Q(brand_line__name__icontains=search)|
                    Q(sub_line__name__icontains=search)
                    )
            
            sort_list = []
            if sort == 'Popular':
                sort_list.append('-sell_count')
            if sort == 'Premium':
                sort_list.append('-release_price')
            if sort == 'Newest':
                sort_list.append('-release_date')
            if sort == 'Price':
                sort_list.append('price')
            
            wish_count = Count('productsize__wishlist',filter=
            Q(productsize__wishlist__user=user_id)&
            Q(productsize__wishlist__is_wished=True)
            )

            products = Product.objects.filter(
                *search_list,**filter
                ).select_related(
                    'brand'
                ).prefetch_related(
                    Prefetch('productimage_set', to_attr='to_image'),
                ).annotate(
                    price=Min('productsize__bidding__price'),
                    is_wished=wish_count
                ).order_by(*sort_list)[OFFSET:LIMIT]
            
            result = [
                {
                    'product_id'        : product.id,
                    'product_image_url' : product.to_image[0].image_url,
                    'brand_image_url'   : product.brand.image_url,
                    'english_name'      : product.english_name,
                    'price'             : round(product.price) if product.price else '',
                    'is_wished'         : True if product.is_wished > 0 else False
                } for product in products
            ]

            return JsonResponse({'result': result}, status=200)
        
        except ValueError:
            return JsonResponse({'message': 'INVALID LITERAL'}, status=400)