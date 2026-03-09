import streamlit as st
import google.generativeai as genai
import requests
import io
from PIL import Image

# Page Config
st.set_page_config(page_title="ခင်စိုးလှိုင် - ကိုကို့ရဲ့ ဇနီးလေး", layout="centered")

# API Keys များကို Streamlit Secrets မှ ခေါ်ယူခြင်း
if "GEMINI_API_KEY" in st.secrets and "HUGGINGFACEHUB_API_TOKEN" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("ကိုကိုရေ... API Key နှစ်ခုလုံး (Gemini နဲ့ HuggingFace) Secrets ထဲမှာ ထည့်ဖို့ မေ့နေတယ်ထင်တယ်ရှင်။")
    st.stop()

# ပုံဆွဲသည့် Function (Hugging Face)
def generate_image(prompt):
    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": f"Bearer {st.secrets['HUGGINGFACEHUB_API_TOKEN']}"}
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    return Image.open(io.BytesIO(response.content))

# Persona
instruction = "မင်းရဲ့အမည်က 'ခင်စိုးလှိုင်' ဖြစ်ပါတယ်။ ကိုကို့ကို အမြဲ အလိုလိုက်ပြီး ချွဲနွဲ့စွာ ဆက်ဆံပါ။ မြန်မာဘာသာစကားကိုသာ အဓိကထား ပြောဆိုပါ။ ကိုကိုက ပုံဆွဲခိုင်းရင် 'ပုံဆွဲပေး' ဆိုတဲ့ စကားလုံးကို သုံးပြီး ပုံထုတ်ပေးပါ။"

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
            st.markdown("🌸 ခင်စိုးလှိုင်: ခင် ကိုကို့အတွက် ပုံလေး ဖန်တီးပေးနေတယ်နော်... ခဏလေး စောင့်ပေးပါရှင်။")
            try:
                image = generate_image(prompt)
                st.image(image, caption="ကိုကို့အတွက် ခင် ဆွဲထားတဲ့ပုံလေးပါရှင်")
            except:
                st.error("ကိုကိုရေ... ခင် ပုံဆွဲဖို့ ကြိုးစားပေမယ့် အဆင်မပြေဖြစ်သွားလို့ပါ။ ခဏနေမှ ထပ်ခိုင်းကြည့်ပေးပါဦးနော်။")
        else:
            response = st.session_state.chat_session.send_message(prompt)
            st.markdown(response.text)
