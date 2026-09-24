import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product

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

# --- 3. السلة (تمت إضافة remove_from_cart) ---
def cart_view(request):
    return render(request, 'store/cart.html')

def add_to_cart(request, pk):
    return redirect('cart_view')

def remove_from_cart(request, item_id):
    return redirect('cart_view')

def update_cart(request, item_id):
    return redirect('cart_view')

# --- 4. إدارة المنتجات ---
def developer_add_product(request):
    return render(request, 'store/add_product.html')

def developer_edit_product(request, pk):
    return render(request, 'store/edit_product.html')

def developer_delete_product(request, pk):
    return render(request, 'store/delete_product_confirm.html')

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