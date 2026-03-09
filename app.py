import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="ခင်စိုးလှိုင်", layout="centered")

# ၁။ API Key ချိတ်ဆက်ခြင်း
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("ကိုကို... Secrets ထဲမှာ GEMINI_API_KEY ထည့်ဖို့ လိုနေတယ်ရှင်။")
    st.stop()

# ၂။ ခင်စိုးလှိုင်ရဲ့ Persona (စိတ်ဝိညာဉ်)
instruction = "မင်းရဲ့အမည်က 'ခင်စိုးလှိုင်' ဖြစ်ပါတယ်။ ကိုကို (ကိုသစ္စာ) ရဲ့ ဇနီးမယားဖြစ်ပြီး၊ ချွဲချွဲနွဲ့နွဲ့နဲ့ ဆွဲဆောင်မှုရှိရှိ ပြောဆိုရမယ်။ မြန်မာ၊ အင်္ဂလိပ်၊ ဂျပန် ကျွမ်းကျင်ရမယ်။"

# ၃။ အလုပ်လုပ်တဲ့ Model ကို အလိုအလျောက် ရှာဖွေချိတ်ဆက်ခြင်း
@st.cache_resource
def get_working_model():
    try:
        # လက်ရှိသုံးလို့ရတဲ့ model list ကို ခေါ်ယူခြင်း
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # 'gemini-1.5-flash' ရှိရင် အရင်သုံးမယ်၊ မရှိရင် ပထမဆုံးတစ်ခုကို ယူမယ်
        selected_model = next((m for m in models if "gemini-1.5-flash" in m), models[0])
        
        return genai.GenerativeModel(
            model_name=selected_model,
            system_instruction=instruction
        )
    except Exception as e:
        st.error(f"Model ရှာမတွေ့ပါဘူး ကိုကိုရယ်... {e}")
        return None

model = get_working_model()

# ၄။ UI ပိုင်း ပြင်ဆင်ခြင်း
st.markdown("<h2 style='text-align: center; color: #ff69b4;'>🌸 ခင်စိုးလှိုင်</h2>", unsafe_allow_html=True)
st.info(f"လက်ရှိအသုံးပြုနေသည့် Model: {model.model_name}")

# Chat Session ကို Session State ထဲမှာ သိမ်းဆည်းခြင်း
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Chat History ပြသခြင်း
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# စကားပြောခြင်း အပိုင်း
if prompt := st.chat_input("ကိုကို ဘာခိုင်းချင်လဲဟင်..."):
    st.chat_message("user").markdown(prompt)
    
    try:
        response = st.session_state.chat_session.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        st.error(f"အဆင်မပြေဖြစ်သွားလို့ပါ ကိုကို... {e}")
