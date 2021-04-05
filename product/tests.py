import json
import jwt
import bcrypt

from product.models import Product, Brand, BrandLine, SubLine, Category, ProductImage, Size, ProductSize
from bidding.models import Bidding, Status
from account.models import User, Address, Wishlist
from account.utils  import login_check, login_decorator
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

class WishlistTest(TestCase):
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

        Size.objects.bulk_create(
            [
            Size(id=1, size=215),
            Size(id=2,size=220),
            Size(id=3,size=225),
            Size(id=4,size=230),
            Size(id=5,size=235),
            Size(id=6,size=240),
            Size(id=7,size=245),
            Size(id=8,size=250),
            Size(id=9,size=255),
            Size(id=10,size=260),
            Size(id=11,size=265),
            Size(id=12,size=270),
            Size(id=13,size=275),
            Size(id=14,size=280),
            Size(id=15,size=285),
            Size(id=16,size=290),
            Size(id=17,size=295),
            Size(id=18,size=300),
            Size(id=19,size=305),
            Size(id=20,size=310),
            Size(id=21,size=315),
            Size(id=22,size=320),
            ]
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
        User.objects.all().delete()
        Wishlist.objects.all().delete()
        Size.objects.all().delete()
        ProductSize.objects.all().delete()

    def test_wishlist_get_success(self):
        client = Client()
        response =  client.get('/product/1', **{'HTTP_AUTHORIZATION' : self.access_token, 'content_type' : 'application/json'})
        self.assertEqual(response.json(),
            {
                'result': [
                    {
                        "size_id": 1,
                        "size_name": "215",
                        "is_wished": True
                    },
                    {
                        "size_id": 2,
                        "size_name": "220",
                        "is_wished": False
                    },
                    {
                        "size_id": 3,
                        "size_name": "225",
                        "is_wished": False
                    },
                    {
                        "size_id": 4,
                        "size_name": "230",
                        "is_wished": False
                    },
                    {
                        "size_id": 5,
                        "size_name": "235",
                        "is_wished": False
                    },
                    {
                        "size_id": 6,
                        "size_name": "240",
                        "is_wished": False
                    },
                    {
                        "size_id": 7,
                        "size_name": "245",
                        "is_wished": False
                    },
                    {
                        "size_id": 8,
                        "size_name": "250",
                        "is_wished": False
                    },
                    {
                        "size_id": 9,
                        "size_name": "255",
                        "is_wished": False
                    },
                    {
                        "size_id": 10,
                        "size_name": "260",
                        "is_wished": False
                    },
                    {
                        "size_id": 11,
                        "size_name": "265",
                        "is_wished": False
                    },
                    {
                        "size_id": 12,
                        "size_name": "270",
                        "is_wished": False
                    },
                    {
                        "size_id": 13,
                        "size_name": "275",
                        "is_wished": False
                    },
                    {
                        "size_id": 14,
                        "size_name": "280",
                        "is_wished": False
                    },
                    {
                        "size_id": 15,
                        "size_name": "285",
                        "is_wished": False
                    },
                    {
                        "size_id": 16,
                        "size_name": "290",
                        "is_wished": False
                    },
                    {
                        "size_id": 17,
                        "size_name": "295",
                        "is_wished": False
                    },
                    {
                        "size_id": 18,
                        "size_name": "300",
                        "is_wished": False
                    },
                    {
                        "size_id": 19,
                        "size_name": "305",
                        "is_wished": False
                    },
                    {
                        "size_id": 20,
                        "size_name": "310",
                        "is_wished": False
                    },
                    {
                        "size_id": 21,
                        "size_name": "315",
                        "is_wished": False
                    },
                    {
                        "size_id": 22,
                        "size_name": "320",
                        "is_wished": False
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)
    
    def test_wishlist_get_authorization_fail(self):
        client = Client()
        response = client.get('/product/1?size_id=1')
        self.assertEqual(response.json(),
            {
                'message': 'Please sign in'
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_wishlist_post_success(self):
        client = Client()
        response =  client.post('/product/1?size_id=1', **{'HTTP_AUTHORIZATION' : self.access_token, 'content_type' : 'application/json'})
        self.assertEqual(response.json(),
            {
                'message': 'SUCCESS'
            }
        )
        self.assertEqual(response.status_code, 200)
    
    def test_wishlist_post_query_params_fail(self):
        client = Client()
        response =  client.post('/product/1', **{'HTTP_AUTHORIZATION' : self.access_token, 'content_type' : 'application/json'})
        self.assertEqual(response.json(),
            {
                'message': 'OUT OF SIZE INDEX'
            }
        )
        self.assertEqual(response.status_code, 400)
    
    def test_wishlist_post_authorization_fail(self):
        client = Client()
        response = client.post('/product/1?size_id=1')
        self.assertEqual(response.json(),
            {
                'message': 'Please sign in'
            }
        )
        self.assertEqual(response.status_code, 400)
    
    def test_wishlist_post_not_found_value_erorr(self):
        client = Client()
        response =  client.post('/product/1?size_id=wecode', **{'HTTP_AUTHORIZATION' : self.access_token, 'content_type' : 'application/json'})
        self.assertEqual(response.json(),
            {
                'message': 'INVALID SIZE_ID'
            }
        )
        self.assertEqual(response.status_code, 400)
    
    def test_wishlist_post_not_found_integrity_erorr(self):
        client = Client()
        response =  client.post('/product/1?size_id=111111111', **{'HTTP_AUTHORIZATION' : self.access_token, 'content_type' : 'application/json'})
        self.assertEqual(response.json(),
            {
                'message': 'OUT OF SIZE INDEX'
            }
        )
        self.assertEqual(response.status_code, 400)