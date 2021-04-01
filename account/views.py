import jwt
import json
import bcrypt
import requests

from django.views import View
from django.http  import JsonResponse

from account.models import User
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
                access_token = jwt.encode({'id':user.id}, SECRET_KEY, ALGORITHM)

                return JsonResponse({'message':'SUCCESS', 'access_token':access_token}, status = 200)

        password_hashed = (bcrypt.hashpw(str(kakao_id).encode('utf-8'), bcrypt.gensalt())).decode('utf-8')
        User.objects.create(email=email, password=password_hashed)

        return JsonResponse({'message':'SUECCESS', 'access_token':access_token}, status = 200)
