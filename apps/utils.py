from decimal import Decimal
from apps.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product_id, quantity=1):
        product_id = str(product_id)
        product = Product.objects.get(id=product_id)
        price = product.discount_price or product.price

        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {
                'name': product.name,
                'price': str(price),
                'quantity': quantity,
                'image': product.first_image,
            }
        self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session['cart'] = {}
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        for product_id, item in self.cart.items():
            item['price'] = Decimal(item['price'])
            item['total'] = item['price'] * item['quantity']
            yield {'id': product_id, **item}

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
