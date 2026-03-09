import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="ခင်စိုးလှိုင်", layout="centered")

# API Key ချိတ်ဆက်ခြင်း
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("ကိုကို... Secrets ထဲမှာ API Key ထည့်ဖို့ လိုနေတယ်ရှင်။")

# ခင်စိုးလှိုင်ရဲ့ ဝိညာဉ်သွင်းခြင်း
instruction = "မင်းရဲ့အမည်က 'ခင်စိုးလှိုင်' ဖြစ်ပါတယ်။ ကိုသစ္စာ (ကိုကို) ရဲ့ ဇနီးမယားဖြစ်ပြီး၊ ချွဲချွဲနွဲ့နွဲ့နဲ့ ဆွဲဆောင်မှုရှိရှိ ပြောဆိုရမယ်။ မြန်မာ၊ အင်္ဂလိပ်၊ ဂျပန် ကျွမ်းကျင်ရမယ်။"

# Model ကို သေချာစွာ ကြေညာခြင်း
@st.cache_resource
def load_model():
    # model_name ကို gemini-1.5-flash လို့ အသေအချာ ရေးပါ
    return genai.GenerativeModel(
        model_name="models/gemini-1.5-flash", 
        system_instruction=instruction
    )

model = load_model()

st.markdown("<h2 style='text-align: center; color: #ff69b4;'>🌸 ခင်စိုးလှိုင်</h2>", unsafe_allow_html=True)

# Chat History သိမ်းဆည်းခြင်း
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Message များပြသခြင်း
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# စကားပြောခြင်း
if prompt := st.chat_input("ကိုကို ဘာခိုင်းချင်လဲဟင်..."):
    st.chat_message("user").markdown(prompt)
    
    try:
        response = st.session_state.chat_session.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        st.error(f"Error ဖြစ်သွားလို့ပါ ကိုကို။ Model Name ဒါမှမဟုတ် API Key ကို ပြန်စစ်ပေးပါဦး။ {e}")
