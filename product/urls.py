from django.urls import path

from product.views import ProductFilterView, WishlistView, SearchView

urlpatterns = [
    path('', ProductFilterView.as_view()),
    path('/<int:product_id>', WishlistView.as_view()),
    path('/search', SearchView.as_view())
]
