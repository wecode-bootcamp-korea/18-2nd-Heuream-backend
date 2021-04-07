import unittest
import json
import datetime


from django.test import TestCase, Client

from bidding.models import Bidding, Status
from account.models import User, Address
from product.models import (
    Product,
    ProductImage,
    ProductSize,
    Category,
    Brand,
    BrandLine,
    SubLine,
    Size,
    )

client = Client()

class BiddingDetailViewTest(TestCase):
    maxDiff = None
    def setUp(self):
        Category.objects.create(id=1, name='test_category'),
        Brand.objects.create(id=1, name='test_brand', image_url='www.naver.com'),
        BrandLine.objects.create(id=1, name='test_brandline', brand_id=1),
        SubLine.objects.create(id=1, name='test_subline', brand_line_id=1),
        Size.objects.create(id=1, size=255),
        Product.objects.create(id=1, korean_name='test_korean', english_name='test_english', models_number='test_model_number', best_color='test_best_color', release_price='300000.00', release_date='2021-04-01', sell_count=1, category_id=1, brand_id=1, brand_line_id=1, sub_line_id=1),
        ProductSize.objects.create(id=1, product_id=1, size_id=1),
        ProductImage.objects.create(id=1, image_url='www.naver.com', product_id=1),
        Status.objects.create(id=1, condition='bidding'),
        Status.objects.create(id=2, condition='bidded'),        
        User.objects.create(id=1, email='test_email', password='test_password', preferred_size_id=1),
        Address.objects.create(id=1, receiver='test_receiver', phone_number='01052097350', address='test_address', is_default=0, user_id=1),
        Bidding.objects.create(id=1, price='300000.00', bidding_type=0, update_at='2021-04-04 04:50:22', create_at='2021-04-01 06:48:50', deadline='2021-04-04 04:50:22', user_id=1, status_id=1, address_id=1, product_size_id=1),
        Bidding.objects.create(id=2, price='300000.00', bidding_type=1, update_at='2021-04-04 04:50:22', create_at='2021-04-01 06:48:50', deadline='2021-04-04 04:50:22', user_id=1, status_id=1, address_id=1, product_size_id=1),
        Bidding.objects.create(id=3, price='300000.00', bidding_type=0, update_at='2021-04-04 04:50:22', create_at='2021-04-01 06:48:50', deadline='2021-04-04 04:50:22', user_id=1, status_id=2, address_id=1, product_size_id=1),  

    def tearDown(self):
        Category.objects.all().delete(),
        Brand.objects.all().delete(),
        BrandLine.objects.all().delete(),
        SubLine.objects.all().delete(),
        Size.objects.all().delete(),
        Product.objects.all().delete(),
        ProductSize.objects.all().delete(),
        ProductImage.objects.all().delete(),
        Status.objects.all().delete(),
        User.objects.all().delete(),
        Bidding.objects.all().delete(),
        Address.objects.all().delete()
    
    def test_bidding_detail_view_success(self):
        response = client.get(f'/bidding',{'product_id':1})
        self.assertEqual(response.json(), {'result':{
            'korean_name'      :'test_korean',
            'english_name'     :'test_english',
            'model_number'     :'test_model_number',
            'best_color'       :'test_best_color',
            'release_date'     :'2021-04-01',
            'release_price'    :'300000.00',
            'brand':'test_brand',
            'product_image_url':'www.naver.com',
            'recent_price'     :'300000.00',            
            'direct_buy_price' :'300000.00',
            'direct_sale_price':'300000.00',
            'bidded':[
                {
                    'bidded_size' :'255',
                    'bidded_price':'300000.00',
                    'bidded_date' :'21/04/08'
                }
            ],
            'buy_bidding':[
                {
                    'buy_bidding_size':'255',
                    'buy_bidding_price':'300000.00',
                    'buy_bidding_quantity':3
                }
            ],
            'sale_bidding':[
                {
                    'sale_bidding_size':'255',
                    'sale_bidding_price':'300000.00',
                    'sale_bidding_quantity':3
                }
            ]
        }
    })
        self.assertEqual(response.status_code, 200)
    
    def test_bidding_detail_view_fail(self):
        response = client.get(f'/bidding',{'product_id':99999})
        self.assertEqual(response.json(),{'message':'INVALID_PAGE'})
        self.assertEqual(response.status_code, 400)
    
    def test_bidding_detail_view_buy_success(self):
        header = {'HTTP_Authorization':"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.IOGSFnezOAETXOTTFMJYwb7nv6lG14FqtahkW9ATL7s"}
        response = client.get(f'/bidding/buy',{'product_id':1}, **header)
        self.assertEqual(response.json(), {'result':{
            'cheap_buy_bidding_price':'300000.00',
            'buy_bidding':[
            {
                'size':'255',
                'buy_bidding_price':'300000.00'
            }
        ]
    }
})


if __name__ == '__main__':  
    unittest.main()

        