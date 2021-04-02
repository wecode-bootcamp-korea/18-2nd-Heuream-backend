import json, bcrypt, jwt

from django.http  import JsonResponse

from my_settings    import SECRET_KEY
from account.models import User


def login_decorator(func):
    
    def wrapper(self, request, *arg, **karg):
        try: 
            token = request.headers['Authorization']

            if not token:
                return JsonResponse({'message': 'Please sign in'}, status=400)

            decoded_token = jwt.decode(token, SECRET_KEY, algorithms='HS256')
            request.user  = User.objects.get(pk=decoded_token['user_id'])

            return func(self, request, *arg, **karg)
        
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'JsonDecodeError'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID USER'}, status=400)

    return wrapper
    

def login_check(func):
    
    def wrapper(self, request, *arg, **karg):
        try: 
            token = request.headers.get('Authorization')

            if not token:
                request.user = None
                return func(self, request, *arg, **karg)
                
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms='HS256')
            request.user  = User.objects.get(pk=decoded_token['user_id'])

            return func(self, request, *arg, **karg)
        
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'JsonDecodeError'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID USER'}, status=400)

    return wrapper
