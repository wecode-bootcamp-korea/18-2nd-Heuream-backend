from django.urls import path

from .views import UserSignIn, UserSignUp, KakaoSignin

urlpatterns = [
    path('/signin', UserSignIn.as_view()),
    path('/signup', UserSignUp.as_view()),
    path('/kakaosignin', KakaoSignin.as_view()),

]
