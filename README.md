# Obida Store 🍉

متجر إلكتروني مبني بـ Django: عرض المنتجات مع المقاسات، سلة تسوق، تسجيل دخول وحسابات، لوحة إدارة للمنتجات (إضافة / تعديل / حذف)، ومساعد ذكي (شات بوت) يجاوب عن المنتجات والأسعار.

## المميزات

- صفحة رئيسية تعرض المنتجات وصفحة تفاصيل لكل منتج (مع المقاسات)
- تسجيل حساب جديد وتسجيل دخول وخروج
- سلة تسوق لكل مستخدم (إضافة / حذف / إجمالي السعر)
- إضافة وتعديل وحذف المنتجات (لحسابات الأدمن `is_staff` فقط)
- مساعد ذكي داخل الموقع

## طريقة التشغيل

يحتاج Python 3.12 أو أحدث.

```bash
# 1) تحميل المشروع
git clone https://github.com/obidasead-jpg/ecommerce_project1.git
cd ecommerce_project1

# 2) إنشاء بيئة افتراضية وتفعيلها (Windows)
python -m venv venv
venv\Scripts\activate
# على Mac / Linux:  source venv/bin/activate

# 3) تثبيت المكتبات
pip install -r requirements.txt

# 4) إعداد ملف البيئة
copy .env.example .env
# (Mac / Linux:  cp .env.example .env)
# ثم افتح .env وضع مفتاحك في GEMINI_API_KEY

# 5) تجهيز قاعدة البيانات
python manage.py migrate

# 6) إنشاء حساب أدمن
python manage.py createsuperuser

# 7) تشغيل الموقع
python manage.py runserver
```

افتح المتصفح على: http://127.0.0.1:8000/

## طريقة التجربة

1. سجّل الدخول بحساب الأدمن الذي أنشأته.
2. من الشريط العلوي اضغط **+ إضافة منتج** وأضف منتجات (الاسم، السعر، الوصف، المقاسات، الصورة).
3. من الصفحة الرئيسية جرّب **تعديل** و**حذف** و**إضافة للسلة**.
4. افتح **السلة** لمراجعة المنتجات والإجمالي.

> ملاحظة: قاعدة البيانات (`db.sqlite3`) وصور المنتجات (`media/`) وملف `.env` غير مرفوعة على GitHub عمداً، لذلك يبدأ المتجر فارغاً ويتم إضافة المنتجات من حساب الأدمن.

## هيكل المشروع

```
ecommerce_project/
├── ecommerce_project/   # إعدادات المشروع (settings, urls)
├── store/               # التطبيق الرئيسي (models, views, forms, templates, static)
├── chatbot/             # تطبيق الشات بوت
├── manage.py
└── requirements.txt
```
