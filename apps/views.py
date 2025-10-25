from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth import get_user_model
from apps.forms import RegisterForm
from apps.models import Product
from apps.utils import Cart

User = get_user_model()


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'apps/products/product.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context['cart_count'] = len(cart)
        return context


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'apps/products/product-detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_products'] = Product.objects.all()[:3]
        cart = Cart(self.request)
        context['cart_count'] = len(cart)
        return context


class RegisterCreateView(CreateView):
    template_name = 'apps/auth/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('product_list_view')


class LoginView(View):
    def get(self, request):
        cart = Cart(request)
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


@require_POST
def add_to_cart(request, product_id):
    quantity = int(request.POST.get('quantity', 1))
    cart = Cart(request)
    cart.add(product_id, quantity)
    return JsonResponse({'cart_count': len(cart)})


def cart_view(request):
    cart = Cart(request)
    context = {'cart': cart, 'cart_count': len(cart)}
    return render(request, 'apps/products/cart.html', context)


@require_POST
def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return JsonResponse({'cart_count': len(cart)})
