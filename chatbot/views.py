import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai

# إعداد مفتاح الـ API من متغيرات البيئة
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            if not user_message:
                return JsonResponse({'error': 'الرجاء إدخال رسالة صحيحة.'}, status=400)
            
            # تعليمات مشددة ومباشرة للـ AI ليتعامل مع كافة الأسئلة فوراً
            system_instruction = (
                "أنت مساعد افتراضي ذكي وودود لمتجر إلكتروني شامل. "
                "مهمتك الرئيسية هي مساعدة العملاء في أي شيء يطلبونه فوراً وبدون تعقيد. "
                "قواعد الرد الخاصة بك: "
                "1. إذا سأل العميل عن (تسجيل الدخول، إنشاء حساب، أو كيفية استخدام الموقع)، اشرح له الخطوات ببساطة شديدة (مثل: اضغط على زر التسجيل في الأعلى، أدخل بريدك، إلخ). "
                "2. إذا سأل عن (طرق الدفع، الشحن، أو الاسترجاع)، اذكر له الخيارات المتاحة مباشرة. "
                "3. ممنوع نهائياً أن تطلب من العميل اسم المنتج بالضبط إذا سأل بشكل عام، بل اقترح عليه خيارات أو اسأله عن ذوقه لمساعدته. "
                "4. كن دائماً مباشراً، ولا تدفع العميل للبحث بنفسه، بل قدم له الحل أو الشرح فوراً باللغة العربية."
            )
            
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=system_instruction
            )
            
            response = model.generate_content(user_message)
            bot_reply = response.text
            
            return JsonResponse({'reply': bot_reply})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'طريقة الطلب غير صحيحة.'}, status=405)