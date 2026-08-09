import ollama


def analyze_message_agent(message: str):
    print("--- [Local AI Agent] جاري تحليل الرسالة محلياً باستخدام Ollama ---")

    prompt = f"""
    أنت وكيل ذكاء اصطناعي (AI Agent) لتحليل النصوص. أجب باختصار شديد وبدون أي مقدمات أو شرح إنجليزي طويل.
    استخرج التالي فقط:
    - الشعور العام: (إيجابي / سلبي / محايد)
    - الموضوع الأساسي: (باختصار في سطر واحد)
    - الطلب أو الشكوى الملحة: (باختصار إن وجدت)

    الرسالة: {message}
    """

    response = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])

    return response['message']['content']


test_message = "السلام عليكم عندي مشكلة في حسابي الشخصي موقف لي كل شيء ولا راضي يشتغل معاي وانا جدا غاضبه من خدمتكم السيئه هذي واتمنى انكم تحلون لي اياها بشكل عاجل جدا!!!"
result = analyze_message_agent(test_message)

print("\n[نتيجة تحليل الوكيل المرتبة]:")
print(result)