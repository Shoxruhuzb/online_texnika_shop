from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.http import JsonResponse
# from django.shortcuts import redirect, render
from django.urls import reverse_lazy
# from django.views import View
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.contrib import messages
# from django.contrib.auth import get_user_model

from apps.forms import RegisterForm
from apps.models import Product
from apps.utils import CartManager


from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.db.models import F

from .models.cart import CartItem, Cart

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


class RegisterCreateView(CreateView):
    template_name = 'apps/auth/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('product_list_view')


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