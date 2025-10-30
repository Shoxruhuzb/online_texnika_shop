from django.urls import path

from apps.views import ProductListView, RegisterCreateView, LoginView, ProductDetailView, LogoutPageView, \
    UserProfileTemplateView, CartView, AddToCartView, RemoveFromCartView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list_view'),
    path('register', RegisterCreateView.as_view(), name='register_view'),
    path('login', LoginView.as_view(), name='login_view'),
    path('logout', LogoutPageView.as_view(), name='logout_page_view'),
    path('product/<uuid:pk>', ProductDetailView.as_view(), name='product_detail_view'),
    path('profile', UserProfileTemplateView.as_view(), name='profile_view'),
    path('cart', CartView.as_view(), name='cart_view'),
    path('cart/add/<uuid:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/remove/<int:product_id>', RemoveFromCartView.as_view(), name='remove_from_cart'),
]
