from django.views     import View
from django.http      import JsonResponse
from django.db.models import Min, Q, Prefetch, Count
from django.db        import IntegrityError

from product.models import Product, ProductImage, ProductSize, Brand, BrandLine, Size, ProductSize
from bidding.models import Bidding, Status
from account.models import User, Wishlist
from account.utils  import login_check, login_decorator


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

class WishlistView(View):
    @login_decorator
    def get(self, request, product_id):
        wish_count = Count('productsize__wishlist',filter=
        Q(productsize__wishlist__user=request.user.id)&
        Q(productsize__wishlist__is_wished=True)&
        Q(productsize__wishlist__product_size__product=product_id))

        sizes = Size.objects.annotate(is_wished=wish_count).all()

        result = [
            {
                'size_id': size.id,
                'size_name': size.size,
                'is_wished': bool(size.is_wished)
            } for size in sizes
        ]
        
        return JsonResponse({'result': result}, status=200)

    @login_decorator
    def post(self, request, product_id):
        try:
            size_id = request.GET.get('size_id')

            product_size = ProductSize.objects.get(product_id=product_id, size_id=size_id)
            
            if not size_id:
                return JsonResponse({'message': 'TYPE SIZE_ID'}, status=400)
            
            wish_obj, flag = Wishlist.objects.get_or_create(user_id=request.user.id, product_size_id=product_size.id)
            
            if not flag:
                wish_obj.is_wished = not wish_obj.is_wished
                wish_obj.save()

            return JsonResponse({'message': 'SUCCESS'}, status=200)
        
        except ValueError:
            return JsonResponse({'message': 'INVALID SIZE_ID'}, status=400)
        
        except IntegrityError:
            return JsonResponse({'message': 'OUT OF INDEX'}, status=400)
        
        except ProductSize.DoesNotExist:
            return JsonResponse({'message': 'OUT OF SIZE INDEX'}, status=400)
            
class SearchView(View):
    def get(self, request):
        try:
            search = request.GET.get('q')
            products = Product.objects.filter(
                Q(korean_name__icontains=search)|
                Q(english_name__icontains=search)|
                Q(models_number__icontains=search)|
                Q(brand__name__icontains=search)|
                Q(brand_line__name__icontains=search)|
                Q(sub_line__name__icontains=search)
            ).prefetch_related(Prefetch('productimage_set', to_attr='to_image'))

            count = products.aggregate(count=Count('id'))

            result = [
                {   
                    'product_id': product.id,
                    'korean_name': product.korean_name,
                    'english_name': product.english_name,
                    'product_image_url': product.to_image[0].image_url,
                } for product in products.order_by('-sell_count')[:10]
            ]
            result.append(count)

            return JsonResponse({'result': result}, status=200)

        except ValueError:
            return JsonResponse({'message': 'VALUE_ERROR'}, status=400)
