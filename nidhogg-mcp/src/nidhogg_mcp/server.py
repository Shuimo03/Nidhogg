"""
Nidhogg MCP Server for conversation storage and vectorization.

This server implements the Model Context Protocol (MCP) to provide
conversation storage capabilities to Claude Code and other MCP clients.
"""

import asyncio
import sys
from pathlib import Path

if __package__ in (None, ""):
    package_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(package_root))
    __package__ = "nidhogg_mcp"

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolResult,
    ServerCapabilities,
    TextContent,
    Tool,
    ToolsCapability, CallToolRequest,
)

# Import our data models and business logic
from .commands.save_conversation import SaveConversationCommand


class NidhoggMCPServer:
    """Main MCP Server class for Nidhogg conversation storage."""

    def __init__(self):
        self.server = Server("nidhogg-mcp")
        self.save_command = SaveConversationCommand()
        self._setup_handlers()

    async def _handle_call_tool(self, name: str, arguments: dict) -> CallToolResult:
        """Handle tool calls from MCP clients."""
        if name == "save_conversation":
            try:
                result = await self.save_command.execute(arguments)
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text=f"Successfully saved conversation to: {result['conversation_path']}"
                        )
                    ]
                )
            except Exception as e:
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text=f"Error saving conversation: {str(e)}"
                        )
                    ],
                    isError=True
                )
        else:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Unknown tool: {name}"
                    )
                ],
                isError=True
            )

    def _setup_handlers(self):
        """Set up MCP request handlers."""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List all available tools in the Nidhogg MCP server."""
            return [
                Tool(
                    name="save_conversation",
                    description="Save a conversation to the three-file system (conversation.md, meta.json, chunks.jsonl)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Title/topic of the conversation"
                            },
                            "messages": {
                                "type": "array",
                                "description": "Array of conversation messages",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "role": {"type": "string", "description": "Message role (user, assistant, system)"},
                                        "content": {"type": "string", "description": "Message content"}
                                    },
                                    "required": ["role", "content"]
                                }
                            },
                            "out_dir": {
                                "type": "string",
                                "description": "Output directory for conversations",
                                "default": "./conversations"
                            },
                            "summary": {
                                "type": "string",
                                "description": "Optional summary of the conversation"
                            },
                            "tags": {
                                "type": "array",
                                "description": "Optional tags for categorization",
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["title", "messages"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> CallToolResult:
            """Handle tool calls from MCP clients."""
            return await self._handle_call_tool(name, arguments)

    async def run(self):
        """Run the MCP server with stdio transport."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="nidhogg-mcp",
                    server_version="0.1.0",
                    capabilities=ServerCapabilities(
                        tools=ToolsCapability()
                    )
                )
            )


def main():
    """Entry point for the Nidhogg MCP server."""
    try:
        # Create and run the server
        server = NidhoggMCPServer()
        asyncio.run(server.run())
    except KeyboardInterrupt:
        print("\nShutting down Nidhogg MCP server...", file=sys.stderr)
    except Exception as e:
        print(f"Error running server: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
