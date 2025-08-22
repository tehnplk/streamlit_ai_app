from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from dotenv import load_dotenv

load_dotenv()

system_prompt = open("system_prompt.md", "r", encoding="utf-8").read()


class AiAgent:
    def __init__(self):
        self.agent = Agent(
            model="google-gla:gemini-2.5-flash",
            system_prompt=system_prompt,
            toolsets=[],
            output_type=str,
        )

    async def chat(self, user_input, message_history=[]):
        async with self.agent:
            result = await self.agent.run(user_input, message_history=message_history)
        return result
