import streamlit as st
import asyncio

from pydantic import BaseModel, Field
from pydantic_ai.mcp import MCPServerStdio

from AiAgent import AiAgent

# กำหนดค่า Agent
llm = "google-gla:gemini-2.5-flash"
system_prompt = open("system_prompt_mcp.md", "r", encoding="utf-8").read()

# ตั้งค่าเชื่อมต่อฐานข้อมูล
mcp_mysql = MCPServerStdio(
    "uvx",
    ["--from", "mysql-mcp-server", "mysql_mcp_server"],
    {
        "MYSQL_HOST": "localhost",
        "MYSQL_PORT": "3310",
        "MYSQL_USER": "root",
        "MYSQL_PASSWORD": "112233",
        "MYSQL_DATABASE": "hos2",
    },
)

toolsets = [mcp_mysql]


class Output(BaseModel):
    result: str = Field(..., description="Query Result in tabular format and Explain")
    sql: str = Field(..., description="SQL Query")


agent = AiAgent(
    llm=llm, system_prompt=system_prompt, toolsets=toolsets, output_type=Output
)


st.title("Agent Chatbot ช่วยเขียน SQL")


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
            {"role": "assistant", "content": result.output.result}
        )
        st.session_state["messages"].append(
            {"role": "assistant", "content": result.output.sql}
        )
        st.chat_message("assistant").markdown(result.output.result)
        if result.output.sql:
            st.chat_message("assistant").code(
                "คำสั่งที่ใช้\n" + result.output.sql, language="sql"
            )
