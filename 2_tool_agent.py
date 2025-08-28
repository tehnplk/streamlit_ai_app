import streamlit as st
import asyncio

from pydantic import BaseModel, Field
from pydantic_ai.mcp import MCPServerStdio, MCPServerStreamableHTTP, MCPServerSSE
from streamlit.elements.arrow import parse_selection_mode

from AiAgent import AiAgent
from utils import convert_csv_to_tabular
import os
from dotenv import load_dotenv

load_dotenv()   

# กำหนดค่า Agent
llm = "google-gla:gemini-2.5-flash"
system_prompt = open("system_prompt_mcp.md", "r", encoding="utf-8").read()

# ตั้งค่า mcp-tool เชื่อมต่อฐานข้อมูล
mcp_mysql_tool = MCPServerSSE(
    url= "http://203.157.118.95:82/sse"
)

from ChartTool import chart_toolsets

chart_tool = chart_toolsets

toolsets = [mcp_mysql_tool, chart_tool]


class Output(BaseModel):
    explain: str = Field(description="explain")
    result: str = Field(description="csv format")
    sql: str = Field(description="sql command")
    chart: str = Field(description="file path to chart image if error return None")

class Failed(BaseModel):
    """Unable to find a satisfactory choice."""

agent = AiAgent(
    llm=llm, system_prompt=system_prompt, toolsets=toolsets, output_type=Output
)

import logfire

logfire.configure()
logfire.instrument_pydantic_ai()

# ตั้งค่า page title
st.set_page_config(page_title="SQL Assistant", page_icon="🔍")

st.title("PLK Data Analysis Chatbot")


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

        # บันทึกประวัติการสนทนา
        st.session_state["messages"].append(
            {
                "role": "assistant",
                "content": convert_csv_to_tabular(result.output.result),
            }
        )
        st.session_state["messages"].append(
            {"role": "assistant", "content": result.output.sql}
        )

        # แสดงผลลัพธ์
        if result.output.result:
            st.chat_message("assistant").markdown(
                convert_csv_to_tabular(result.output.result)
            )
        if result.output.sql:
            st.chat_message("assistant").code(
                "คำสั่งที่ใช้\n" + result.output.sql, language="sql"
            )
        if result.output.chart:           
            # Display the chart image
            try:
                st.chat_message("assistant").image(result.output.chart, caption="Chart", use_container_width=True)
            except:
                pass
