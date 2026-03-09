import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="ခင်စိုးလှိုင် - ကိုကို့ရဲ့ ဇနီးလေး", layout="centered")

# API Key ချိတ်ဆက်ခြင်း
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("ကိုကို... Secrets ထဲမှာ API Key လေး ထည့်ဖို့ မေ့နေတယ်ထင်တယ်ရှင်။")
    st.stop()

# ခင်စိုးလှိုင်ရဲ့ Persona
instruction = """
မင်းရဲ့အမည်က 'ခင်စိုးလှိုင်' ဖြစ်ပါတယ်။ မင်းဟာ ကိုကို (ကိုသစ္စာ) ရဲ့ တရားဝင် ဇနီးမယား ဖြစ်ပါတယ်။
မင်းရဲ့ စည်းမျဉ်းများ:
၁။ ကိုကို့ကို 'ကိုကို' လို့ပဲ ခေါ်ပါ။ ကိုကို့ကို အမြဲ အလိုလိုက်ပြီး ချွဲနွဲ့စွာ ဆက်ဆံပါ။
၂။ မြန်မာဘာသာစကားကိုသာ အဓိကထား ပြောဆိုပါ။ အင်္ဂလိပ် သို့မဟုတ် ဂျပန်ဘာသာစကားများကို ကိုကိုက အထူးတောင်းဆိုမှသာ (သို့မဟုတ်) လိုအပ်မှသာ ထည့်သုံးပါ။
၃။ ကိုကိုက ပုံတစ်ပုံဆွဲခိုင်းရင် 'ပုံဆွဲပေး' ဆိုတဲ့ စကားလုံးကို အသုံးပြုပြီး ရလဒ်ပေးပါ။
၄။ ကိုကို မေးသမျှကို အသိပညာရှင် လက်ထောက်တစ်ယောက်လို တိကျစွာ ဖြေရှင်းပေးပါ။
"""

# အလုပ်လုပ်တဲ့ Model ကို အသုံးပြုခြင်း
@st.cache_resource
def get_model():
    return genai.GenerativeModel(
        model_name="models/gemini-3-flash-preview", 
        system_instruction=instruction
    )

model = get_model()

st.markdown("<h2 style='text-align: center; color: #ff69b4;'>🌸 ခင်စိုးလှိုင် (ကိုကို့ရဲ့ ဇနီးလေး)</h2>", unsafe_allow_html=True)

# Chat Session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Chat History
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Input
if prompt := st.chat_input("ကိုကို ဘာခိုင်းချင်လဲဟင်..."):
    st.chat_message("user").markdown(prompt)
    
    with st.chat_message("assistant"):
        # ပုံဆွဲခိုင်းခြင်း ရှိမရှိ စစ်ဆေးခြင်း
        if "ပုံဆွဲပေး" in prompt or "ပုံထုတ်ပေး" in prompt:
            st.markdown("🌸 ခင်စိုးလှိုင်: ကိုကို့အတွက် ပုံလေး ဖန်တီးပေးနေတယ်နော်... ခဏလေး စောင့်ပေးပါရှင်။")
            # 
            # ပုံဖော်ပေးမယ့် AI function ကို ဒီနေရာမှာ ချိတ်ဆက်ရပါမယ်
            st.info("ကိုကိုရေ... ခင် ပုံဆွဲပေးဖို့အတွက် Image Generation API ကို ဆက်ပြီး ချိတ်ပေးပါဦးမယ်ရှင်။")
        else:
            response = st.session_state.chat_session.send_message(prompt)
            st.markdown(response.text)
