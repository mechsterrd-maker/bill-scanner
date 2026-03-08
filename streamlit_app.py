import streamlit as st
from openai import OpenAI
import base64
import pandas as pd

# 1. Setup OpenAI Client
# We will set the API key securely in the next step
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

st.set_page_config(page_title="AI Bill Scanner", layout="centered")
st.title("📸 Bill & PDF Scanner")

# 2. The Mobile Camera Trigger
# On a phone, this button opens the camera or gallery
uploaded_file = st.file_uploader("Upload Bill or Take Photo", type=['png', 'jpg', 'jpeg', 'pdf'])

if uploaded_file:
    st.image(uploaded_file, caption="Processing...", use_container_width=True)
    
    with st.spinner("AI is reading the bill..."):
        base64_image = encode_image(uploaded_file)
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract: merchant, date, total, currency. Return valid JSON only."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }
            ],
            response_format={"type": "json_object"}
        )
        
        # 3. Output Data
        data = response.choices[0].message.content
        st.success("Data Extracted!")
        st.json(data)
