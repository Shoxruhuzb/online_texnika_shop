from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from apps.forms import CustomUserCreationForm

from apps.models import Product
from apps.utils import send_email

from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'apps/products/product.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'apps/products/product-detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_products'] = Product.objects.all()[:3]
        return context


class RegisterCreateView(CreateView):
    template_name = 'apps/auth/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('product_list_view')

    def form_valid(self, form):
        _form = super().form_valid(form)

        send_email.delay(form.instance.email)
        return _form


# class LoginTemplateView(LoginView):
#     template_name = 'apps/auth/login.html'
#     next_page = reverse_lazy('product_list_view')
#
#     def form_valid(self, form):
#         return super().form_valid(form)
#
#     def form_invalid(self, form):
#         return super().form_invalid(form)


class CustomLoginView(View):
    def get(self, request):
        return render(request, 'apps/auth/login.html')

    def post(self, request):
        username = request.POST.get('username')
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)

            if (user.email == identifier) or (user.profile.phone == identifier):
                auth_user = authenticate(request, username=username, password=password)

                if auth_user is not None:
                    login(request, auth_user)
                    return redirect(reverse_lazy('product_list_view'))
                else:
                    messages.error(request, "Parol noto‘g‘ri.")
            else:
                messages.error(request, "Email yoki telefon noto‘g‘ri.")
        except User.DoesNotExist:
            messages.error(request, "Bunday foydalanuvchi mavjud emas.")

        return render(request, 'apps/auth/login.html')


class LogoutPageView(View):
    success_url = reverse_lazy('product_list_view')

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(self.success_url)


class UserProfileTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'apps/auth/profile.html'
