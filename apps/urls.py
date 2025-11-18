from apps.views import (
    # AddToCartView,
    CartListView,
    LoginFormView,
    LogoutPageView,
    ProductDetailView,
    ProductListView,
    RegisterCreateView,
    # RemoveFromCartView,
    # ResendOtpView,
    UserProfileTemplateView,
    # otpVerifyView,
)
from django.urls import path

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list_view'),
    path('login', LoginFormView.as_view(), name='login_view'),
    path('logout', LogoutPageView.as_view(), name='logout_view'),
    path('product/<uuid:pk>', ProductDetailView.as_view(), name='product_detail_view'),
    path('profile', UserProfileTemplateView.as_view(), name='profile_view'),
    path('cart', CartListView.as_view(), name='cart_view'),
    path('register', RegisterCreateView.as_view(), name='register_view'),

    # path('cart/add/<uuid:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    # path('cart/remove/<uuid:product_id>', RemoveFromCartView.as_view(), name='remove_from_cart'),
    # path('otp/<str:uid>/', otpVerifyView.as_view(), name='otp_view'),
    # path('otp/resend/<str:uid>/', ResendOtpView.as_view(), name='resend_otp_view'),
]
