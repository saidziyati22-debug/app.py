import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="سعد الزياتي AI", page_icon="🤖")

# الساروت (ضروري يكون ف Secrets)
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("زيد الساروت ف Secrets أولا!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# تحديد الشخصية (System Instruction)
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="أنت ذكاء اصطناعي خاص بسعد الزياتي. جاوب بذكاء وبالدارجة المغربية."
)

st.title("🤖 مساعد سعد الزياتي الذكي")

# ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الشات القديم
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# فين بنادم كايكتب سؤاله
if prompt := st.chat_input("بشنو نقدر نعاونك؟"):
    # سجل ميساج المستعمل
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # جواب البوت
    with st.chat_message("assistant"):
        try:
            # هنا البوت كايقرا السؤال وكايجاوب
            response = model.generate_content(prompt)
            st.markdown(response.text)
            # سجل جواب البوت ف الذاكرة
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("ach tama al5awa.")
