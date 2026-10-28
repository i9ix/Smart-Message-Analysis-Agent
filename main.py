import json
import ollama

MODEL = "llama3"

PROMPT = """أنت محلل رسائل عملاء. حلل الرسالة وأرجع JSON فقط بهذا الشكل:
{{
  "sentiment": "إيجابي أو سلبي أو محايد",
  "topic": "جملة عربية واحدة قصيرة تلخص موضوع الرسالة، وليس كلمات منفصلة",
  "category": "شكوى أو استفسار أو طلب أو شكر أو أخرى",
  "urgency": رقم من 1 إلى 5,
  "urgent_request": "الطلب الملح أو null"
}}

قواعد:
- إذا الرسالة شكر أو مدح فالتصنيف "شكر" والشعور "إيجابي" والاستعجال 1.
- لا تصنفها "شكوى" إلا إذا العميل يعبر عن مشكلة أو استياء.

أمثلة:
الرسالة: ما قدرت أدخل حسابي من أمس وأحتاج حل بسرعة
النتيجة: {{"sentiment": "سلبي", "topic": "مشكلة في تسجيل الدخول إلى الحساب", "category": "شكوى", "urgency": 4, "urgent_request": "استعادة الوصول إلى الحساب"}}

الرسالة: ممتاز، تم حل مشكلتي بسرعة، يعطيكم العافية
النتيجة: {{"sentiment": "إيجابي", "topic": "شكر على سرعة حل المشكلة", "category": "شكر", "urgency": 1, "urgent_request": null}}

الرسالة: كم مدة توصيل الطلب إلى الرياض؟
النتيجة: {{"sentiment": "محايد", "topic": "استفسار عن مدة التوصيل", "category": "استفسار", "urgency": 2, "urgent_request": null}}

الرسالة: {message}
"""


def analyze_message(message: str) -> dict:
    try:
        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": PROMPT.format(message=message)}],
            format="json",
            options={"temperature": 0},
        )
        return json.loads(response["message"]["content"])
    except json.JSONDecodeError:
        return {"error": "النموذج رجّع رد غير صالح، جرّب مرة ثانية."}
    except Exception as e:
        return {"error": f"تأكد أن Ollama شغال وأن الموديل {MODEL} محمّل. التفاصيل: {e}"}


def main():
    print("وكيل تحليل الرسائل (اكتب 'خروج' للإنهاء)")
    while True:
        message = input("\nالرسالة: ").strip()
        if message in ("خروج", "exit", "quit"):
            break
        if not message:
            continue
        result = analyze_message(message)
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
