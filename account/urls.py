from django.urls import path

from .views import UserSignIn, UserSignUp

urlpatterns = [
   path('/signin', UserSignIn.as_view()),
   path('/signup', UserSignUp.as_view()),
]
