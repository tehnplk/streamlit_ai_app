import streamlit as st
import asyncio

from AiAgent import AiAgent

agent = AiAgent()

# st.set_page_config(layout="wide")


# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "ถามมาได้เลย.."}]

# Display conversation history
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# Initialize message history for pydantic_ai
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []


if user_input := st.chat_input("Enter your question:"):
    # Add user message to chat history
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Get AI response
    with st.spinner("Thinking..."):
        message_history = st.session_state["message_history"]
        result = asyncio.run(agent.chat(user_input, message_history))
        new_message_history = result.all_messages()
        st.session_state["message_history"] = new_message_history

        st.session_state["messages"].append(
            {"role": "assistant", "content": result.output}
        )
        st.chat_message("assistant").write(result.output)
