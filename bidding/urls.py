from django.urls import path

from bidding.views import BiddingDetailView, BiddingDetailBuyView, BiddingDetailSaleView

urlpatterns = [
    path('', BiddingDetailView.as_view()),
    path('/buy', BiddingDetailBuyView.as_view()),
    path('/sale', BiddingDetailSaleView.as_view()),
]

