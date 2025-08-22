import streamlit as st
import asyncio

from AiAgent import AiAgent

# กำหนดค่า Agent
llm = "google-gla:gemini-2.5-flash"
system_prompt = open("system_prompt_basic.md", "r", encoding="utf-8").read()
agent = AiAgent(llm=llm, system_prompt=system_prompt, output_type=str)

st.title("Agent Chatbot Basic")


# กำหนดค่าเริ่มต้นให้ session state สำหรับประวัติการสนทนา
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "ถามมาได้เลย.."}]

# แสดงประวัติการสนทนา
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# กำหนดค่าเริ่มต้นให้ message_history สำหรับ agent
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []


if user_input := st.chat_input("Enter your question:"):
    # เพิ่มข้อความของผู้ใช้ลงในประวัติการสนทนา
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)

    # รอรับคำตอบจาก AI
    with st.spinner("Thinking..."):
        message_history = st.session_state["message_history"]
        result = asyncio.run(agent.chat(user_input, message_history))
        new_message_history = result.all_messages()
        st.session_state["message_history"] = new_message_history

        st.session_state["messages"].append(
            {"role": "assistant", "content": result.output}
        )
        st.chat_message("assistant").markdown(result.output)
