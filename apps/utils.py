from apps.models.cart import Cart, CartItem
from apps.models.products import Product
from django.contrib.auth.hashers import check_password, make_password


class CartManager:
    def __init__(self, request):
        self.request = request
        self.user = request.user if request.user.is_authenticated else None
        self.session = request.session
        if not self.session.session_key:
            self.session.create()
        self.session_key = self.session.session_key

    def _get_or_create_cart(self):
        if self.user:
            cart, _ = Cart.objects.get_or_create(user=self.user)
        else:
            cart, _ = Cart.objects.get_or_create(session_key=self.session_key)
        return cart

    def add(self, product_id, quantity=1):
        product = Product.objects.get(id=product_id)
        cart = self._get_or_create_cart()

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += quantity
        item.save()

    def remove(self, product_id):
        cart = self._get_or_create_cart()
        CartItem.objects.filter(cart=cart, product_id=product_id).delete()

    def clear(self):
        cart = self._get_or_create_cart()
        cart.items.all().delete()

    def get_items(self):
        cart = self._get_or_create_cart()
        return cart.items.select_related('product')

    def get_total_price(self):
        cart = self._get_or_create_cart()
        return cart.total_price

    def __len__(self):
        cart = self._get_or_create_cart()
        return cart.items.count()


class PasswordManager:

    def __init__(self, hasher='argon2'):
        self.hasher = hasher

    def hash(self, password: str) -> str:
        return make_password(password, hasher=self.hasher)

    def verify(self, password: str, hashed_password: str) -> bool:
        return check_password(password, hashed_password)
