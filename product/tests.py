import json
import jwt
import bcrypt

from product.models import Product, Brand, BrandLine, SubLine, Category, ProductImage, Size, ProductSize
from bidding.models import Bidding, Status
from account.models import User, Address, Wishlist
from account.utils  import login_check
from my_settings    import SECRET_KEY, ALGORITHM

from django.test   import TestCase
from django.test   import Client

class ProductFilterTest(TestCase):

    def setUp(self):
        client = Client()
        Category.objects.create(
            id   = 1,
            name = '스니커즈'
        )

        Brand.objects.create(
            id        = 1,
            name      = 'Jordan',
            image_url = 'https://heuream-images.s3.ap-northeast-2.amazonaws.com/heuream-brand_image/heuream-brand_image/d_5_dc2727e24e2f4741b4afde50f4f4a5f0.png'
        )

        Brand.objects.create(
            id        = 2,
            name      = 'Adidas',
            image_url = 'https://heuream-images.s3.ap-northeast-2.amazonaws.com/heuream-brand_image/heuream-brand_image/p_1_ec2229e75cb1407696b209ddda0e3f5b.png'
        )

        BrandLine.objects.create(
            id    = 1,
            name  = '1',
            brand = Brand.objects.get(id=1)
        )

        BrandLine.objects.create(
            id    = 2,
            name  = 'Yeeze',
            brand = Brand.objects.get(id=2)
        )

        Product.objects.create(
            id = 1,
            korean_name   = '엄청 이쁜 조던 1',
            english_name  = 'Ultra Super Jordan 1',
            models_number = 'WO123on',
            best_color    = 'REALRED',
            release_date  = '2222-12-01',
            release_price = 1299999.00,
            sell_count    = 0,
            category      = Category.objects.get(id=1),
            brand         = Brand.objects.get(id=1),
            brand_line    = BrandLine.objects.get(id=1)
        )

        Product.objects.create(
            id = 2,
            korean_name   = '엄청 이쁜 조던 이지',
            english_name  = 'Ultra Super Yeeze',
            models_number = 'YESSSS-11',
            best_color    = 'REALWHITE',
            release_date  = '2000-11-01',
            release_price = 3590422.00,
            sell_count    = 5,
            category      = Category.objects.get(id=1),
            brand         = Brand.objects.get(id=2),
            brand_line    = BrandLine.objects.get(id=2)
        )

        ProductImage.objects.create(
            id        = 1,
            image_url = 'https://kream-phinf.pstatic.net/MjAyMTAyMDNfMjY2/MDAxNjEyMzE3NDQ1NTAx.Oejtk7Y6zAvCrjhtND50c7JClIDq5g75DlJ391D3Rfkg.nukMbPmTeoKRGgSvfzBM9ZoF0JaqIw6Ge5TkWfncHHUg.PNG/p_56ffd2340d6c476da2f58c151e0205c2.png?type=m',
            product   = Product.objects.get(id=1)
        )
        ProductImage.objects.create(
            id        = 2,
            image_url = 'https://kream-phinf.pstatic.net/MjAyMTAxMDZfMTQx/MDAxNjA5OTAyNjc4Mzk4.f65bXKS5WJHYhIrRGZxh8YWqmq3ufBo_NwrFqxU6sOog.4LtLePf3Qn67chfRJlhjlzxt7zmcv48Onx0LMbSP034g.PNG/p_86841c19c5154db3ac24f1f74378c5e6.png?type=m',
            product   = Product.objects.get(id=2)
        )

        Size.objects.create(
            id   = 1,
            size = '210'
        )

        ProductSize.objects.create(
            id      = 1,
            product = Product.objects.get(id=1),
            size    = Size.objects.get(id=1)
        )

        User.objects.create(
            id       = 1,
            email    = 'jungwon@wecode.com',
            password = '12345678'
        )

        Address.objects.create(
            id           = 1,
            receiver     = '곽두팔',
            phone_number = '01052741421',
            address      = '서울시 어딘가',
            user         = User.objects.get(id=1)
        )

        Status.objects.create(
            id        = 1,
            condition = '입찰중',
        )

        Status.objects.create(
            id        = 2,
            condition = '입찰완료',
        )

        Bidding.objects.create(
            id           = 1,
            price        = 1500000.00,
            deadline     = '2021-05-31 04:50:22',
            bidding_type = False,
            address      = Address.objects.get(id=1),
            product_size = ProductSize.objects.get(id=1),
            status       = Status.objects.get(id=1)
        )

        Wishlist.objects.create(
            id = 1,
            user         = User.objects.get(id=1),
            product_size = ProductSize.objects.get(id=1)
        )

        self.access_token = jwt.encode({'user_id': User.objects.get(id=1).id}, SECRET_KEY, ALGORITHM)

    def tearDown(self):
        Category.objects.all().delete()
        Brand.objects.all().delete()
        BrandLine.objects.all().delete()
        Product.objects.all().delete()
        ProductImage.objects.all().delete()
        Wishlist.objects.all().delete()
        Bidding.objects.all().delete()
        Status.objects.all().delete()
        Address.objects.all().delete()
        User.objects.all().delete()
    
    def test_productfilter_get_success(self):
        client   = Client()
        response = client.get('/product?brand=1&brand_line=1&sort=Premium&q=jor', **{'HTTP_AUTHORIZATION':self.access_token, 'content_type' : 'application/json'})
        self.assertEqual(response.json(),
            {
                "result": [
                    {
                        "product_id": 1,
                        "product_image_url": "https://kream-phinf.pstatic.net/MjAyMTAyMDNfMjY2/MDAxNjEyMzE3NDQ1NTAx.Oejtk7Y6zAvCrjhtND50c7JClIDq5g75DlJ391D3Rfkg.nukMbPmTeoKRGgSvfzBM9ZoF0JaqIw6Ge5TkWfncHHUg.PNG/p_56ffd2340d6c476da2f58c151e0205c2.png?type=m",
                        "brand_image_url": "https://heuream-images.s3.ap-northeast-2.amazonaws.com/heuream-brand_image/heuream-brand_image/d_5_dc2727e24e2f4741b4afde50f4f4a5f0.png",
                        "english_name": "Ultra Super Jordan 1",
                        'price': 1500000,
                        'is_wished': True
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)
    
    def test_productfilter_get_fail(self):
        client   = Client()
        response = client.get('/product?offset=100')
        self.assertEqual(response.json(),
            {
                'result': []
            }
        )
        self.assertEqual(response.status_code, 200)
    
    def test_productfilter_get_not_found(self):
        client   = Client()
        response = client.get('/product?offset=wecode')
        self.assertEqual(response.json(), 
            {
                'message': 'INVALID LITERAL'
            }
        )
        self.assertEqual(response.status_code, 400)