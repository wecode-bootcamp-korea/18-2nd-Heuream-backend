import re
import jwt
import json
import bcrypt
import django
from unittest.mock import patch, MagicMock


from django.test  import TestCase, Client, TransactionTestCase
from django.http  import JsonResponse
from django.db    import transaction

from account.models import User
from my_settings    import SECRET_KEY, ALGORITHM

class SignUpTest(TransactionTestCase):
    def setUp(self):
        with transaction.atomic():
            User.objects.create(email='gyudong1594@wecode.com', password='paper1594@')

    def test_signup_success(self):
        client = Client()

        user = {
            'email':'test@test.com',
            'password':'testpSassword@1'
        }

        reponse = client.post('/account/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(reponse.status_code, 201)
        self.assertEqual(reponse.json(), {'message':'SUCCESS'})
    
    def test_signup_invalid_email(self):
        client = Client()

        user = {
            'email':'testtest.com',
            'password':'testpassword@1'
        }

        reponse = client.post('/account/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(reponse.status_code, 400)
        self.assertEqual(reponse.json(), {'message':'INVALID_EMAIL'})

    def test_signup_invalid_password(self):
        client = Client()

        user = {
            'email':'tes@test.com',
            'password':'testpassword'
        }

        reponse = client.post('/account/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(reponse.status_code, 400)
        self.assertEqual(reponse.json(), {'message':'INVALID_PASSWORD'})

    def test_signup_key_error(self):
        client = Client()

        user = {
            'email':'testtest.com'
        }

        reponse = client.post('/account/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(reponse.status_code, 400)
        self.assertEqual(reponse.json(), {'message':'KEY_ERROR'})

    def test_signup_invalid_json(self):
        client = Client()

        reponse = client.post('/account/signup')

        self.assertEqual(reponse.status_code, 400)
        self.assertEqual(reponse.json(), {'message':'INVALID_JSON'})

    def test_signup_registered_email(self):
        client = Client()

        user = {
            'email':'gyudong1594@wecode.com',
            'password':'testpasswoSrd@1'
        }

        reponse = client.post('/account/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(reponse.status_code, 400)
        self.assertEqual(reponse.json(), {'message':'REGISTERED_EMAIL'})

class SignInTest(TestCase):
    def setUp(self):
        password = 'paper1594'
        password = (bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())).decode('utf-8')
        User.objects.create(email='gyudong1594@wecode.com', password=password)

    def test_signin_success(self):
        client = Client()

        user = {
            'email':'gyudong1594@wecode.com',
            'password':'paper1594'
        }

        reponse = client.post('/account/signin', json.dumps(user), content_type='application/json')
        access_token = jwt.encode({'user_id':7}, SECRET_KEY, ALGORITHM)

        self.assertEqual(reponse.status_code, 200)
        self.assertEqual(reponse.json(), {'message':'SUCCESS', 'access_token':access_token})
    
    def test_signin_invalid_password(self):
        client = Client()

        user = {
            'email':'gyudong1594@wecode.com',
            'password':'error_password'
        }

        reponse = client.post('/account/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(reponse.status_code, 401)
        self.assertEqual(reponse.json(), {'message':'INVALID_USER'})

    def test_signin_invalid_email(self):
        client = Client()

        user = {
            'email':'error_email',
            'password':'paper1594'
        }

        reponse = client.post('/account/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(reponse.status_code, 401)
        self.assertEqual(reponse.json(), {'message':'INVALID_USER'})

    def test_signin_key_error(self):
        client = Client()

        user = {
            'password':'no_email'
        }

        reponse = client.post('/account/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(reponse.status_code, 400)
        self.assertEqual(reponse.json(), {'message':'KEY_ERROR'})
    
    def test_signin_invalid_json(self):
        client = Client()

        reponse = client.post('/account/signin')

        self.assertEqual(reponse.status_code, 400)
        self.assertEqual(reponse.json(), {'message':'INVALID_JSON'})

class KakaoSignUpTest(TestCase):
    @patch('account.views.requests')
    def test_kakao_signup(self, mocked_request):
        client = Client()
        class MockResponse:
            def json(self):
                return {
                    'id':1,
                    'kakao_account':{
                        'email':'test_email@kakao.com'
                    }
                }
        
        mocked_request.get = MagicMock(return_value = MockResponse())
        headers = {'HTTP_Authorization':'kakao_token'}
        access_token = jwt.encode({'user_id':2}, SECRET_KEY, ALGORITHM)
        response = client.post('/account/kakaosignin', content_type='application/json', **headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message':'SUCCESS', 'access_token':access_token})

class KakaoSignInTest(TestCase):
    def setUp(self):
        User.objects.create(email='gyudong1594@wecode.com', password='12345678')
    
    def tearDown(self):
        User.objects.all().delete()

    @patch('account.views.requests')
    def test_kakao_signin(self, mocked_request):
        client = Client()
        class MockResponse:
            def json(self):
                return {
                    'id':1,
                    'kakao_account':{
                        'email':'gyudong1594@wecode.com'
                    }
                }
        
        mocked_request.get = MagicMock(return_value = MockResponse())
        headers = {'HTTP_Authorization':'kakao_token'}
        access_token = jwt.encode({'user_id':1}, SECRET_KEY, ALGORITHM)
        response = client.post('/account/kakaosignin', content_type='application/json', **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message':'SUCCESS', 'access_token':access_token})