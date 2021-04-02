import jwt
import json
import bcrypt

from django.views import View
from django.http  import JsonResponse

from account.models import User
from my_settings    import SECRET_KEY, ALGORITHM

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