# ตัวอย่่างการใช้งาน Ai agent ด้วย streamlit (ภาษา python)

## ติดตั้ง library ที่จำเป็น
- pip install pydantic-ai  
- pip install streamlit
- pip install fastmcp

## ขอ gemini_api_key
- สมัครและขอ API Key ได้ที่ [Google AI Studio](https://aistudio.google.com/app/apikey)

## ตั้งค่าไฟล์ .env
- เปลี่ยนชื่อ  .env.example  ให้เป็น  .env
- ใส่ gemini_api_key

## การกำหนด system_prompt 
- ให้แก้ไขไฟล์ system_prompt.md

## การ run 
- streamlit run 1-agent.py
- เปิด browser ไปที่  [http://localhost:8501](http://localhost:8501)