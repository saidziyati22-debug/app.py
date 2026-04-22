
import streamlit as st
import google.generativeai as genai

# 1. أحسن حاجة تجبد الـ Key من Secrets
# إيلا بغيتي تجرب غير ف الجهاز ديالك، خلي الكي ديالك بلاصة st.secrets
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    API_KEY = "AIzaSyAUYVOf6x09hpNaHQvJ-Yqo4GjTtq2ac8o" # الكي ديالك

genai.configure(api_key=API_KEY)

st.title("My AI Assistant 🤖")
st.write("مرحباً! أنا ذكاء اصطناعي خاص بسعد الزياتي..")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. استعمل موديل أحدث (1.5-flash)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    try:
        # صيفط الـ prompt
        response = model.generate_content(prompt)
        
        with st.chat_message("assistant"):
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("السموحة، ماقدرتش نجاوب على هاد السؤال.")
                
    except Exception as e:
        st.error(f"وقع مشكل تقني: {e}")
