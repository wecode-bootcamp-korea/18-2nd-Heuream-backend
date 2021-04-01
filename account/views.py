import re
import jwt
import json
import bcrypt
import django
import requests

from django.views import View
from django.http  import JsonResponse

from account.models import User
from product.models import Size
from my_settings    import SECRET_KEY, ALGORITHM

MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 16

class UserSignUp(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            password  = data['password']
            email     = data['email']
            size      = data.get('size', None)
                
            if not (re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)):
                return JsonResponse({"message":"INVALID_EMAIL"}, status = 400)

            if not (re.findall('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,16}', password)):
                return JsonResponse({"message":"INVALID_PASSWORD"}, status = 400)

            password_hashed = (bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())).decode('utf-8')
                
            User.objects.create(
                email=email,
                password=password_hashed,
                preferred_size=size
            )

            return JsonResponse({'message':'SUCCESS'}, status = 201)
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)
        
        except json.decoder.JSONDecodeError:
            return JsonResponse({"message": "INVALID_JSON"}, status = 400)
        
        except django.db.utils.IntegrityError:
            return JsonResponse({'message':'REGISTERED_EMAIL'}, status = 400)

class UserSignIn(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email    = data["email"]
            password = data["password"]
            
            if User.objects.filter(email = email).exists():
                user = User.objects.get(email = email)

                if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                    access_token = jwt.encode({'user_id': user.id}, SECRET_KEY, ALGORITHM)

                    return JsonResponse({"message":"SUCCESS", 'access_token':access_token}, status = 200)
                                
                else:
                    return JsonResponse({"message":"INVALID_USER"}, status = 401)    
            else:
                return JsonResponse({"message":"INVALID_USER"}, status = 401)
                
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)
        
        except json.decoder.JSONDecodeError:
            return JsonResponse({"message": "INVALID_JSON"}, status = 400)
from my_settings    import SECRET_KEY, ALGORITHM

class KakaoSignin(View):
    def post(self, request):
        access_token = request.headers['Authorization']
        url = 'https://kapi.kakao.com/v2/user/me'
        headers = {
                'Authorization': f'Bearer {access_token}',
        }

        response = requests.get(url, headers=headers)

        profile  = response.json()
        email    = profile['kakao_account']['email']
        kakao_id = profile['id']
        
        if User.objects.filter(email=email).exists():
            user         = User.objects.get(email=email)
            access_token = jwt.encode({'user_id':user.id}, SECRET_KEY, ALGORITHM)
            
            return JsonResponse({'message':'SUCCESS', 'access_token':access_token}, status = 200)

        password_hashed = (bcrypt.hashpw(str(kakao_id).encode('utf-8'), bcrypt.gensalt())).decode('utf-8')
        user = User.objects.create(email=email, password=password_hashed)

        access_token = jwt.encode({'user_id':user.id}, SECRET_KEY, ALGORITHM)

        return JsonResponse({'message':'SUCCESS', 'access_token':access_token}, status = 201)
