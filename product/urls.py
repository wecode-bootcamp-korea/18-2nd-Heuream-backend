from django.urls import path

from product.views import ProductFilterView

urlpatterns = [
    path('', ProductFilterView.as_view())
]
