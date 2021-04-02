import jwt
import json
import bcrypt

from django.test import TestCase, Client

from account.models import User
from my_settings    import SECRET_KEY, ALGORITHM

class SignInTest(TestCase):
    def setUp(self):
        password = 'paper1594'
        password = (bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())).decode('utf-8')
        User.objects.create(email='gyudong1594@wecode.com', password=password)
    
    def tearDown(self):
        User.objects.all().delete()

    def test_signin_success(self):
        client = Client()

        user = {
            'email':'gyudong1594@wecode.com',
            'password':'paper1594'
        }

        reponse = client.post('/account/signin', json.dumps(user), content_type='application/json')
        access_token = jwt.encode({'user_id':5}, SECRET_KEY, ALGORITHM)

        self.assertEqual(reponse.status_code, 200)
        self.assertEqual(reponse.json(), {'message':'SUCCESS', 'access_token':access_token})
    
    def test_signin_invalid_password(self):
        client = Client()

        user = {
            'email':'gyudong1594@wecode.com',
            'password':'error_password'
        }

        reponse = client.post('/account/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(reponse.status_code, 400)
        self.assertEqual(reponse.json(), {'message':'INVALID_USER'})

    def test_signin_invalid_email(self):
        client = Client()

        user = {
            'email':'error_email',
            'password':'paper1594'
        }

        reponse = client.post('/account/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(reponse.status_code, 400)
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
