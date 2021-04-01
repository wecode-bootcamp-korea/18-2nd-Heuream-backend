from django.urls import path

from bidding.views import BiddingDetailView

urlpatterns = [
    path('', BiddingDetailView.as_view()),
]