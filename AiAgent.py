from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from dotenv import load_dotenv
from typing import Optional,Any
load_dotenv()



class AiAgent:
    def __init__(self,llm,system_prompt,tools=[],output_type:Optional[Any]=None):
        self.agent = Agent(
            model=llm,
            system_prompt=system_prompt,
            toolsets=tools,
            output_type=output_type,
        )

    async def chat(self, user_input, message_history=[]):
        async with self.agent:
            result = await self.agent.run(user_input, message_history=message_history)
        return result
