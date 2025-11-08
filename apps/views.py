from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.views.generic import DetailView, TemplateView, CreateView
from django.contrib import messages

from apps.forms import RegisterForm
from apps.models import Product
from apps.utils import CartManager

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import F

from .helper import MessageHandler, is_otp_valid
from .models.cart import CartItem, Cart

import random
from django.http import HttpResponse

User = get_user_model()


class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'apps/products/product.html', {'products': products})


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'apps/products/product-detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_products'] = Product.objects.all()[:3]
        cart = CartManager(self.request)
        context['cart_count'] = len(cart)
        return context


class RegisterCreateView(View):
    template_name = 'apps/auth/register.html'

    def get(self, request):
        return render(request, self.template_name, {'form': RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            phone = form.cleaned_data['phone']

            if User.objects.filter(phone=phone).exists():
                return render(request, self.template_name,
                              {'form': form, 'error': 'Bu telefon raqam allaqachon mavjud.'})

            user.save()

            otp = MessageHandler(phone).send_otp_via_message()
            request.session['pending_phone'] = phone
            return redirect(f"/otp/{user.uid}/")

        return render(request, self.template_name, {'form': form})


# class otpVerifyView(View):
#     template_name = 'apps/auth/otp.html'
#
#     def get(self, request, uid):
#         return render(request, self.template_name, {'id': uid})
#
#     def post(self, request, uid):
#         try:
#             user = User.objects.get(uid=uid)
#         except User.DoesNotExist:
#             return HttpResponse("User not found")
#
#         if not request.COOKIES.get('can_otp_enter'):
#             return HttpResponse('10 minutes passed')
#
#         entered_otp = request.POST.get('otp')
#         if user.otp == entered_otp:
#             user.is_active = True
#             user.save()
#             response = redirect(reverse_lazy("product_list_view"))
#             response.set_cookie('verified', True)
#             return response
#         else:
#             return HttpResponse("WRONG code")
class otpVerifyView(View):
    template_name = 'apps/auth/otp.html'

    def get(self, request, uid):
        return render(request, self.template_name, {'id': uid})

    def post(self, request, uid):
        try:
            user = User.objects.get(uid=uid)
        except User.DoesNotExist:
            return HttpResponse("User not found")

        phone = user.phone
        entered_otp = request.POST.get('otp')

        if is_otp_valid(phone, entered_otp):
            user.is_active = True
            user.save()
            return redirect(reverse_lazy("product_list_view"))
        else:
            return render(request, self.template_name, {
                'id': uid,
                'error_message': "❌ Siz kiritgan kod noto‘g‘ri yoki muddati tugagan."
            })


@method_decorator(csrf_exempt, name='dispatch')
class ResendOtpView(View):
    def post(self, request, uid):
        try:
            user = User.objects.get(uid=uid)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found'})

        otp = str(random.randint(1000, 9999))
        MessageHandler(user.phone, otp, user).send_otp_via_message()
        return JsonResponse({'success': True})


class LoginView(View):
    def get(self, request):
        cart = CartManager(request)
        return render(request, 'apps/auth/login.html', {'cart_count': len(cart)})

    def post(self, request):
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user = authenticate(request, username=phone, password=password)

        if user is not None:
            login(request, user)
            return redirect(reverse_lazy('product_list_view'))
        else:
            messages.error(request, "Bunday foydalanuvchi mavjud emas.")
        return render(request, 'apps/auth/login.html')


class LogoutPageView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('login_view'))


class UserProfileTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'apps/auth/profile.html'


class CartView(View):
    def get_cart_items(self, request):
        cart_items = []
        total_price = 0
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)
            for item in cart.items.all():
                cart_items.append(item)
                total_price += item.total_price
        else:
            session_cart = request.session.get('cart', {})
            for product_id, qty in session_cart.items():
                product = get_object_or_404(Product, id=product_id)
                total = product.price * qty
                cart_items.append({'product': product, 'quantity': qty, 'total_price': total})
                total_price += total
        return cart_items, total_price

    def get(self, request):
        cart_items, total_price = self.get_cart_items(request)
        return render(request, 'apps/products/cart.html', {
            'cart_items': cart_items,
            'total_price': total_price
        })


class AddToCartView(View):
    def post(self, request, product_id):
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)

        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
            item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            item.quantity = F('quantity') + quantity
            item.save()
        else:
            cart = request.session.get('cart', {})
            if str(product_id) in cart:
                cart[str(product_id)] += quantity
            else:
                cart[str(product_id)] = quantity
            request.session['cart'] = cart
            request.session.modified = True

        return JsonResponse({'success': True})


class RemoveFromCartView(View):
    def post(self, request, product_id):
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user, is_active=True).first()
            if cart:
                CartItem.objects.filter(cart=cart, product_id=product_id).delete()
        else:
            cart = request.session.get('cart', {})
            cart.pop(str(product_id), None)
            request.session['cart'] = cart
            request.session.modified = True
        return JsonResponse({'success': True})
