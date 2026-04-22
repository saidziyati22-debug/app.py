import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة (العنوان والأيقونة)
st.set_page_config(page_title="Gemini AI Morocco", page_icon="🇲🇦")

# 2. جلب الـ API Key من Secrets وتأمين الاتصال
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("❌ الساروت (API Key) ناقص! زيد 'AIzaSyAUYVOf6x09hpNaHQvJ-Yqo4GjTtq2ac8o' في Secrets عاد كمل.")
    st.stop()

genai.configure(api_key=st.secrets["AIzaSyAUYVOf6x09hpNaHQvJ-Yqo4GjTtq2ac8o"])

# 3. تحديد شخصية البوت (هنا كتقرر كيفاش يجاوب الناس)
# تقدر تبدل هاد النص باش تردو كايجاوب كيف بغيتي
instruction = "أنت مساعد ذكاء اصطناعي سميتك 'Gemini المغرب'. كتحضر مع الناس بالدارجة المغربية، كتساعدهم في كاع المجالات، وكتكون ظريف ومؤدب."

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=instruction
)

# 4. إعداد ذاكرة المحادثة (باش ما ينساش شنو قلتي ليه)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. عرض الرسائل القديمة في الصفحة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. خانة الشات (فين كيكتب المستعمل)
if prompt := st.chat_input("بشنو نقدر نعاونك اليوم؟"):
    
    # أ- عرض وحفظ ميساج المستعمل
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # ب- توليد الجواب من عقل Gemini
    with st.chat_message("assistant"):
        try:
            # كنجمعو التاريخ ديال الهضرة باش البوت يفهم السياق
            # استعملنا طريقة بسيطة باش يجاوب على آخر سؤال مع فهم اللي فات
            response = model.generate_content(prompt)
            
            answer = response.text
            st.markdown(answer)
            
            # ج- حفظ جواب البوت في الذاكرة
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            st.error(f"وقع مشكل تقني: {e}")

# 7. زر في الجنب لمسح الشات (Sidebar)
with st.sidebar:
    st.title("الإعدادات")
    if st.button("مسح المحادثة 🗑️"):
        st.session_state.messages = []
        st.rerun()
