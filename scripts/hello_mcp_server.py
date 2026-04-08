import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("hello-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="say_hello",
            description="Returns a greeting",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "say_hello":
        name_arg = arguments.get("name", "World")
        return [TextContent(type="text", text=f"Hello, {name_arg}!")]
    raise ValueError(f"Unknown tool {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    asyncio.run(main())
