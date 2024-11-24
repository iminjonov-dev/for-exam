from datetime import date, timedelta
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem, Category

# Categoryalarni korish va ichidan Search qilish
class CategoryView(ListView):
    model = Category
    template_name = 'app_product/categories.html'
    context_object_name = 'categories'
    paginate_by = 3

    def get_queryset(self):
        search = self.request.GET.get('q', '')

        if search:
            return Category.objects.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        else:
            return Category.objects.all()

# Productlarni korish va ichidan Search qilish
class ProductView(ListView):
    model = Product
    template_name = 'app_main/index.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        search = self.request.GET.get('q', '')
        category_id = self.kwargs.get('category_id')

        if search:
            return Product.objects.filter(
                Q(title__icontains=search) | Q(description__icontains=search) | Q(category__title__icontains=search)
            )
        else:
            return Product.objects.filter(category__id=category_id)

# Productlarni detail qismini korish
class ProductDetailView(DetailView):
    model = Product
    template_name = 'app_product/product_detail.html'
    context_object_name = 'product'


def cart(request):
    return render(request, 'app_product/cart.html')


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total_price = sum(item.get_total_price() for item in items)
    shipping_cost = 0

    context = {
        'cart_items': items,
        'total_price': total_price,
        'shipping_cost': shipping_cost,
        'grand_total': total_price + shipping_cost,
    }
    return render(request, 'app_product/cart.html', context)




class CartView(ListView):
    model = Cart
    template_name = 'app_product/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_price = sum(item.total_price for item in context["cart_items"])
        context["total_price"] = total_price
        context["10_days_later"] = date.today() + timedelta(days=10)
        context["today"] = date.today()
        context["total_amount"] = total_price + 10
        return context




def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart')


def add_to_cart(request, pk):
    product = get_object_or_404(Product, id=pk)
    cart, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart.quantity += 1
        cart.save()

    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'app_product/cart.html', {'cart_items': cart_items})



def delete_product_card(request, product_id):
    cart_item = get_object_or_404(Cart, product__id=product_id, user=request.user)

    if cart_item.quantity <= 1:
        cart_item.delete()
    else:
        cart_item.quantity -= 1
        cart_item.save()

    return redirect('cart')

#
# def add_product_card(request, pk, action):
#     cart_item = get_object_or_404(Cart, pk=pk, user=request.user)
#
#     if action == 'increment':
#         cart_item.quantity += 1
#     elif action == 'decrement' and cart_item.quantity > 1:
#         cart_item.quantity -= 1
#     elif action == 'decrement' and cart_item.quantity == 1:
#         cart_item.delete()
#         return redirect('cart')
#
#     cart_item.save()
#
#     return redirect('cart')
