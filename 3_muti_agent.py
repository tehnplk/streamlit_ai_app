from pydantic_ai import Agent, RunContext
from pydantic_ai.usage import UsageLimits

from pydantic_ai.mcp import MCPServerStdio
import os

from dotenv import load_dotenv

load_dotenv()

from ChartTool import chart_toolsets

mcp_mysql_tool = MCPServerStdio(
    "uvx",
    ["--from", "mysql-mcp-server", "mysql_mcp_server"],
    {
        "MYSQL_HOST": os.getenv("MYSQL_HOST", "localhost"),
        "MYSQL_PORT": os.getenv("MYSQL_PORT", "3306"),
        "MYSQL_USER": os.getenv("MYSQL_USER", "root"),
        "MYSQL_PASSWORD": os.getenv("MYSQL_PASSWORD", "1234"),
        "MYSQL_DATABASE": os.getenv("MYSQL_DATABASE", "his"),
    },
)

mysql_agent = Agent(
    "google-gla:gemini-2.5-flash",
    system_prompt=open("system_prompt_mcp.md", "r", encoding="utf-8").read(),
    toolsets=[mcp_mysql_tool],
    output_type=str,
)

chart_agent = Agent(
    "google-gla:gemini-2.5-flash",
    system_prompt="คุณเป็นผู้ช่วยที่สามารถสร้างกราฟและตารางข้อมูลที่ได้รับ",
    toolsets=[chart_toolsets],
    output_type=str,
)


@mysql_agent.tool
async def chart_tool(ctx: RunContext[None]) -> str:
    async with chart_agent:
        r = await chart_agent.run()
    return r.output


async def main():
    async with mysql_agent:
        result = await mysql_agent.run(
            "นับจำนวนประชากรแยกรายหมู่ แสดงเป็นตาราง และใช้ข้อมูลที่ได้สร้างแผนภูมิแท่งเปรียบเทียบจำนวนประชากรรายหมู่บ้าน",
        )
    return result


if __name__ == "__main__":
    import asyncio

    result = asyncio.run(main())
    print(result.output)
