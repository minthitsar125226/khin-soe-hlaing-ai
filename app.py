import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Model Scanner", layout="centered")

st.title("🔍 Gemini Model Scanner")

# ၁။ Secrets ထဲက API Key ကို စစ်ဆေးခြင်း
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    st.success("✅ API Key ကို Secrets ထဲမှာ တွေ့ရှိပါတယ်။")
else:
    st.error("❌ GEMINI_API_KEY ကို Secrets ထဲမှာ မတွေ့ရပါဘူး။ Advanced Settings မှာ သွားထည့်ပေးပါ ကိုကို။")
    st.stop()

# ၂။ ရရှိနိုင်သော Model များအားလုံးကို ခေါ်ယူခြင်း
st.subheader("ကိုကို့ API နဲ့ သုံးလို့ရတဲ့ Model များစာရင်း")

try:
    model_list = []
    # Gemini ရဲ့ list_models() function ကို သုံးပြီး စစ်ဆေးမယ်
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            model_list.append(m.name)
    
    if model_list:
        for model_name in model_list:
            st.code(model_name, language="text")
        st.info(f"စုစုပေါင်း Model ({len(model_list)}) ခု တွေ့ရှိပါတယ်ရှင်။")
    else:
        st.warning("⚠️ စကားပြောလို့ရတဲ့ Model တစ်ခုမှ ရှာမတွေ့ပါဘူး။")

except Exception as e:
    st.error(f"❌ Model List ခေါ်ယူရာမှာ Error တက်သွားပါတယ်: {e}")
    st.info("အကြံပြုချက်: API Key က မှားနေတာ (သို့မဟုတ်) Google Cloud မှာ Gemini API ကို Enable မလုပ်ရသေးတာ ဖြစ်နိုင်ပါတယ်ရှင်။")

st.markdown("---")
st.write("ဒီစာရင်းထဲမှာ ပေါ်လာတဲ့ နာမည်ကိုမှ ခင်တို့ AI အတွက် ပြန်သုံးရမှာပါ ကိုကို။")
