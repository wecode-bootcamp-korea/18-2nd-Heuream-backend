from django.urls import path

from product.views import ProductFilterView, WishlistView

urlpatterns = [
    path('', ProductFilterView.as_view()),
    path('/<int:product_id>', WishlistView.as_view())
]
