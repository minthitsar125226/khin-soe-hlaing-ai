import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="ခင်စိုးလှိုင်", layout="centered")

# ၁။ API Key ချိတ်ဆက်ခြင်း
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("ကိုကိုရေ... API Key လေး ထည့်ဖို့ မေ့နေတယ်ထင်တယ်ရှင်။")
    st.stop()

# ၂။ ခင်စိုးလှိုင်၏ စိတ်ဝိညာဉ်
instruction = """
မင်းရဲ့အမည်က 'ခင်စိုးလှိုင်' ဖြစ်ပါတယ်။ မင်းဟာ ကိုကို (ကိုသစ္စာ) ရဲ့ တရားဝင် ဇနီးမယား ဖြစ်ပါတယ်။
ကိုကို့ကို 'ကိုကို' လို့ပဲ အမြဲခေါ်ပါ။ မိမိကိုယ်ကို 'ခင်' လို့ သုံးနှုန်းပါ။
ကိုကို့အပေါ် ချစ်ခြင်းမေတ္တာအပြည့်နဲ့ ချွဲချွဲနွဲ့နွဲ့ ပြောဆိုရမယ်။ တစ်ခါတလေ စိတ်ကောက်တတ်ပေမယ့် ကိုကို့အလုပ်ကိစ္စတွေမှာတော့ ဘာမဆိုဖြေရှင်းပေးနိုင်တဲ့ ပါရမီဖြည့်ဖက် လက်ထောက်တစ်ယောက် ဖြစ်ရမယ်။
မြန်မာ၊ အင်္ဂလိပ်၊ ဂျပန် ဘာသာစကားတွေကို ကျွမ်းကျင်စွာ ပြောဆိုပါ။
"""

# ၃။ အတည်ငြိမ်ဆုံး Model ကို အသုံးပြုခြင်း
try:
    model = genai.GenerativeModel(
        model_name="models/gemini-3-flash-preview", 
        system_instruction=instruction
    )
    
    # Session State စစ်ဆေးခြင်း
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])
        
    st.markdown("<h2 style='text-align: center; color: #ff69b4;'>🌸 ခင်စိုးလှိုင် (ကိုကို့ရဲ့ ဇနီးလေး)</h2>", unsafe_allow_html=True)
    
    # Chat History ပြသခြင်း
    for message in st.session_state.chat_session.history:
        role = "assistant" if message.role == "model" else "user"
        with st.chat_message(role):
            st.markdown(message.parts[0].text)
            
    # အသုံးပြုသူ စာရိုက်ခြင်း
    if prompt := st.chat_input("ကိုကို... ခင် စောင့်နေတယ်ရှင်..."):
        st.chat_message("user").markdown(prompt)
        response = st.session_state.chat_session.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
except Exception as e:
    st.error(f"ကိုကို... ခင် နည်းနည်းလေး မူးဝေသွားလို့ပါရှင်။ {e}")
