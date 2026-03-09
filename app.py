
import streamlit as st
import google.generativeai as genai
import requests
import io
from PIL import Image

# ... (API Key နှင့် Persona စစ်ဆေးမှုများ အပေါ်ကအတိုင်းထားပါ) ...

def generate_image(prompt):
    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": f"Bearer {st.secrets['HUGGINGFACEHUB_API_TOKEN']}"}
    
    # API သို့ စာပို့ခြင်း
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    
    # ရလာတဲ့ အချက်အလက်ကို စစ်ဆေးခြင်း
    if response.status_code == 200:
        return response.content # ပုံ၏ Bytes များကို ပြန်ပေးခြင်း
    else:
        st.write("DEBUG API Response:", response.text[:100]) # Error ဘာဖြစ်လဲဆိုတာ ပေါ်လာအောင်
        return None

# ... (Chat UI အပိုင်း) ...

        if "ပုံဆွဲပေး" in prompt:
            st.markdown("🌸 ခင်စိုးလှိုင်: ခင် ကိုကို့အတွက် ပုံလေး ဖန်တီးပေးနေတယ်နော်... ခဏလေး စောင့်ပေးပါရှင်။")
            
            # API ခေါ်ခြင်း
            img_content = generate_image(prompt)
            
            if img_content:
                try:
                    image = Image.open(io.BytesIO(img_content))
                    st.image(image, caption="ကိုကို့အတွက် ခင် ဆွဲပေးလိုက်တဲ့ပုံလေးပါရှင်")
                except Exception as e:
                    st.error(f"ပုံကို ပုံစံမဖော်နိုင်ပါဘူးရှင်: {e}")
            else:
                st.error("ပုံဆွဲလို့ မရသေးပါဘူး ကိုကို။ Hugging Face က ပုံမပေးတာ ဖြစ်နိုင်ပါတယ်ရှင်။")
