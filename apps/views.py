from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from apps.forms import RegisterForm

from apps.models import Product


from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()


# """Bu user oldin borligini tekshirish uchun"""
# def form_valid(self, form):
#     username = form.cleaned_data['username']
#     if User.objects.filter(username=username).exists():
#         form.add_error('username', 'This username is already taken.')
#         return self.form_invalid(form)
#     user = form.save()
#     return super().form_valid(form)


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
    form_class = RegisterForm
    success_url = reverse_lazy('product_list_view')


class LoginView(View):
    def get(self, request):
        return render(request, 'apps/auth/login.html')

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

    # def post(self, request):
    #     identifier = request.POST.get('identifier')
    #     password = request.POST.get('password')
    #
    #     try:
    #         user = User.objects.get(Q(email=identifier) | Q(phone=identifier))
    #
    #         auth_user = authenticate(request, username=user.username, password=password)
    #
    #         if auth_user:
    #             login(request, auth_user)
    #             return redirect(reverse_lazy('product_list_view'))
    #         else:
    #             messages.error(request, "Parol noto‘g‘ri.")
    #
    #     except User.DoesNotExist:
    #         messages.error(request, "Bunday foydalanuvchi mavjud emas.")
    #
    #     return render(request, 'apps/auth/login.html')


class LogoutPageView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('login'))

    # success_url = reverse_lazy('product_list_view')
    #
    # def get(self, request, *args, **kwargs):
    #     logout(request)
    #     return redirect(self.success_url)


class UserProfileTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'apps/auth/profile.html'
