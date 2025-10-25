from django.urls import path

from apps.views import ProductListView, RegisterCreateView, LoginView, ProductDetailView, LogoutPageView, \
    UserProfileTemplateView, cart_view, add_to_cart, remove_from_cart

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list_view'),
    path('register', RegisterCreateView.as_view(), name='register_view'),
    path('login', LoginView.as_view(), name='login_view'),
    path('logout', LogoutPageView.as_view(), name='logout_page_view'),
    path('product/<uuid:pk>', ProductDetailView.as_view(), name='product_detail_view'),
    path('profile', UserProfileTemplateView.as_view(), name='profile_view'),
    path('cart', cart_view, name='cart_view'),
    path('cart/add/<uuid:product_id>', add_to_cart, name='add_to_cart'),
    path('cart/remove/<uuid:product_id>', remove_from_cart, name='remove_from_cart'),
]
