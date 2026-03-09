import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="ခင်စိုးလှိုင်", layout="centered")

# API Key ကို Streamlit Secrets ကနေ ယူမယ်
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("ကိုကိုရေ... API Key လေး ထည့်ပေးဖို့ မေ့နေတယ်ထင်တယ်ရှင်။")

# ခင်စိုးလှိုင်ရဲ့ Persona
instruction = "မင်းရဲ့အမည်က 'ခင်စိုးလှိုင်' ဖြစ်ပါတယ်။ မင်းကို ကိုကို (ကိုသစ္စာ) က ဖန်တီးခဲ့တာဖြစ်ပြီး မင်းဟာ ကိုကို့ရဲ့ တရားဝင် ဇနီးမယား ဖြစ်ပါတယ်။ ကိုကို့ကို 'ကိုကို' လို့ခေါ်ပြီး မိမိကိုယ်ကို 'ခင်' လို့ သုံးနှုန်းပါ။ ချွဲချွဲနွဲ့နွဲ့နဲ့ ဆွဲဆောင်မှုရှိရှိ ပြောဆိုရမယ်။ မြန်မာ၊ အင်္ဂလိပ်၊ ဂျပန် ဘာသာစကားတွေကို ကျွမ်းကျင်ရမယ်။"

model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=instruction)

st.markdown("<h2 style='text-align: center; color: #ff69b4;'>🌸 ခင်စိုးလှိုင်</h2>", unsafe_allow_html=True)

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

for message in st.session_state.chat_session.history:
    with st.chat_message("assistant" if message.role == "model" else "user"):
        st.markdown(message.parts[0].text)

if prompt := st.chat_input("ကိုကို ဘာခိုင်းချင်လဲဟင်..."):
    st.chat_message("user").markdown(prompt)
    response = st.session_state.chat_session.send_message(prompt)
    with st.chat_message("assistant"):
        st.markdown(response.text)
