from django.urls import path

from account.views import KakaoSignin

urlpatterns = [
    path('/kakaosignin', KakaoSignin.as_view()),
]