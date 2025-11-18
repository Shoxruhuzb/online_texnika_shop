from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class LoginNotRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('product_list_view')
        return super().dispatch(request, *args, **kwargs)
