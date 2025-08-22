# ตัวอย่่างการใช้งาน Ai agent ด้วย streamlit (ภาษา python)

## ติดตั้ง library ที่จำเป็น
- pip install pydantic-ai  
- pip install streamlit
- pip install fastmcp
- pip install uv

## ขอ gemini_api_key
- สมัครและขอ API Key ได้ที่ [Google AI Studio](https://aistudio.google.com/app/apikey)

## ตั้งค่าไฟล์ .env
- เปลี่ยนชื่อ  .env.example  ให้เป็น  .env
- ใส่ gemini_api_key

## การกำหนด system_prompt 
- แก้ไขไฟล์ system_prompt_basic.md
- แก้ไขไฟล์ system_prompt_mcp.md

## การ run ใช้คำสั่ง
- streamlit run 1_basic_agent.py
- streamlit run 2_mcp_agent.py
- เปิด browser ไปที่  [http://localhost:8501](http://localhost:8501)

## ฐานข้อมูลที่มีข้อมูลส่วนบุคคล
- ควรใช้ฐานข้อมูลที่มีการเข้ารหัสหรือฐานข้อมูลปลอม