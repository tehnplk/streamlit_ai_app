from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv()


class AiAgent:
    def __init__(self):
        self.agent = Agent(
            model="google-gla:gemini-2.5-flash",
            system_prompt="คุณคือผู้เชี่ยวชาญด้าสถิติ",
            output_type=str,
        )

    async def chat(self, user_input, message_history=[]):
        #with self.agent:
        result = await self.agent.run(user_input, message_history=message_history)
        return result
