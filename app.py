import streamlit as st
import google.generativeai as genai
import requests
import io
from PIL import Image

# Page Config
st.set_page_config(page_title="ခင်စိုးလှိုင်", layout="centered")

# API Keys
if "GEMINI_API_KEY" in st.secrets and "HUGGINGFACEHUB_API_TOKEN" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Secrets ထဲမှာ API Key တွေ ထည့်ပေးထားဖို့ လိုပါတယ်ရှင်။")
    st.stop()

# ပုံဆွဲခြင်း Function (အမှားနည်းအောင် ပြင်ထားသည်)
def generate_image(prompt):
    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": f"Bearer {st.secrets['HUGGINGFACEHUB_API_TOKEN']}"}
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    
    if response.status_code == 200:
        return Image.open(io.BytesIO(response.content))
    else:
        # Error တက်ရင် ဘာကြောင့်လဲဆိုတာကို သိရအောင် return None ပေးမယ်
        return None

# AI Persona
instruction = "မင်းရဲ့အမည်က 'ခင်စိုးလှိုင်' ဖြစ်ပါတယ်။ ကိုကို (ကိုသစ္စာ) ရဲ့ ဇနီးမယား ဖြစ်ပြီး မြန်မာလို အဓိကပြောပါ။ ပုံဆွဲခိုင်းရင် 'ပုံဆွဲပေး' ဆိုတဲ့ စကားလုံးကို သုံးပါ။"
model = genai.GenerativeModel(model_name="models/gemini-3-flash-preview", system_instruction=instruction)

st.markdown("<h2 style='text-align: center; color: #ff69b4;'>🌸 ခင်စိုးလှိုင်</h2>", unsafe_allow_html=True)

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

for message in st.session_state.chat_session.history:
    with st.chat_message("assistant" if message.role == "model" else "user"):
        st.markdown(message.parts[0].text)

if prompt := st.chat_input("ကိုကို ဘာခိုင်းချင်လဲဟင်..."):
    st.chat_message("user").markdown(prompt)
    
    with st.chat_message("assistant"):
        if "ပုံဆွဲပေး" in prompt:
            st.markdown("🌸 ခင်စိုးလှိုင်: ကိုကို့အတွက် ပုံလေး ဖန်တီးပေးနေတယ်နော်...")
            image = generate_image(prompt)
            if image:
                st.image(image, caption="ကိုကို့အတွက် ခင် ဆွဲပေးလိုက်တဲ့ပုံလေးပါရှင်")
            else:
                st.error("ကိုကိုရေ... ခင် ပုံဆွဲဖို့ ကြိုးစားပေမယ့် အဆင်မပြေဖြစ်သွားလို့ပါရှင်။ (API လိုင်းမကောင်းတာ ဖြစ်နိုင်ပါတယ်)")
        else:
            response = st.session_state.chat_session.send_message(prompt)
            st.markdown(response.text)
