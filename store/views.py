import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Product, Cart, CartItem
from .forms import ProductForm

staff_required = user_passes_test(lambda u: u.is_staff, login_url='login')

# --- 1. الرئيسية والتفاصيل ---
def store_home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    sizes_list = []
    if hasattr(product, 'sizes') and product.sizes:
        sizes_list = [s.strip() for s in product.sizes.split(',')]
    return render(request, 'store/product_detail.html', {'product': product, 'sizes_list': sizes_list})

# --- 2. التسجيل والتعريف (Register & Login) ---
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('store_home')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('store_home')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('store_home')

# --- 3. السلة ---
def _get_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart

@login_required
def cart_view(request):
    cart = _get_cart(request.user)
    items = cart.items.select_related('product')
    total = sum(item.get_total_price() for item in items)
    return render(request, 'store/cart.html', {'items': items, 'total': total})

@login_required
def add_to_cart(request, product_id):   # الاسم لازم يطابق <int:product_id> في urls.py
    product = get_object_or_404(Product, pk=product_id)
    cart = _get_cart(request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    return redirect('cart_view')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart_view')

# --- 4. إدارة المنتجات (للمطور/الأدمن فقط) ---
@staff_required
def developer_add_product(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('store_home')
    return render(request, 'store/add_product.html', {'form': form})

@staff_required
def developer_edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('store_home')
    return render(request, 'store/edit_product.html', {'form': form, 'product': product})

@staff_required
def developer_delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('store_home')
    return render(request, 'store/delete_product_confirm.html', {'product': product})

# --- 5. الشات بوت الذكي AI ---
def ai_chatbot(request):
    if request.method == 'POST':
        user_message = ""
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_message = data.get('message', '').strip()
        except Exception:
            user_message = request.POST.get('message', '').strip()

        if not user_message:
            return JsonResponse({'reply': 'عذراً، لم أستلم أي نص. يرجى كتابة سؤالك.'})

        products = Product.objects.all()
        matched = [p for p in products if user_message.lower() in p.name.lower() or (p.description and user_message.lower() in p.description.lower())]

        if matched:
            p = matched[0]
            reply = f"نعم! منتج '{p.name}' متوفر حالياً بسعر ${p.price}."
            if hasattr(p, 'sizes') and p.sizes:
                reply += f" المقاسات المتاحة: {p.sizes}."
        elif any(word in user_message for word in ["مقاس", "مقاسات", "المقاس"]):
            reply = "تتوفر لدينا مقاسات متنوعة (S, M, L, XL). يمكنك الضغط على 'عرض التفاصيل' للتحقق من مقاسات كل قطعة."
        elif any(word in user_message for word in ["سعر", "أسعار", "بكام", "تكلفة"]):
            reply = "تختلف الأسعار حسب القطعة. يمكنك تصفح المنتجات في المعرض مباشرةً لمعرفة تفاصيل الأسعار."
        elif any(word in user_message for word in ["مرحبا", "أهلا", "سلام", "هاي", "hello"]):
            reply = "أهلاً بك في Obida Store! 🍉 كيف يمكنني مساعدتك في التسوق اليوم؟"
        else:
            reply = f"شكراً لسؤالك عن '{user_message}'. يسعدنا خدمتك! يمكنك تصفح معرض المنتجات أو الاستفسار عن قطعة معينة."

        return JsonResponse({'reply': reply})

    return JsonResponse({'reply': 'أهلاً بك في Obida Store! كيف يمكنني مساعدتك اليوم؟'})