from django.urls import path

from bidding.views import BiddingDetailView, BiddingDetailBuyView

urlpatterns = [
    path('', BiddingDetailView.as_view()),
    path('/buy', BiddingDetailBuyView.as_view()),
]