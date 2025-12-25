"""
SaveConversationCommand implementation for the Nidhogg MCP server.

This command handles the core business logic for saving conversations
to the three-file system as defined in the PRD.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from ..models.meta import ConversationMeta, ConversationStatus
from ..writers import ThreeFileWriter


def _generate_conversation_id(title: str) -> str:
    """
    Generate a stable conversation ID from title and timestamp.

    Uses a combination of sanitized title and timestamp to create
    human-readable but unique directory names.
    """
    # Sanitize title for filesystem
    sanitized = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
    sanitized = sanitized.replace(' ', '-').lower()

    # Truncate if too long
    if len(sanitized) > 50:
        sanitized = sanitized[:50].rstrip('-')

    # Add timestamp for uniqueness
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    return f"{sanitized}-{timestamp}" if sanitized else f"conversation-{timestamp}"


class SaveConversationCommand:
    """
    Command to save conversations to the three-file system.

    This is the main business logic implementation that:
    1. Validates input parameters
    2. Creates conversation metadata
    3. Delegates to ThreeFileWriter for actual file operations
    """

    def __init__(self):
        self.writer = ThreeFileWriter()

    async def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the save_conversation command.

        Args:
            arguments: MCP tool arguments containing:
                - title: string - conversation title/topic
                - messages: list - conversation messages
                - out_dir: string - output directory (default: "./conversations")
                - summary: string - optional summary
                - tags: list - optional tags

        Returns:
            Dict with conversation_path and metadata

        Raises:
            ValueError: If required arguments are missing or invalid
            Exception: If file operations fail
        """
        # Validate required arguments
        if "title" not in arguments:
            raise ValueError("Missing required argument: title")

        if "messages" not in arguments:
            raise ValueError("Missing required argument: messages")

        if not arguments["messages"]:
            raise ValueError("Messages array cannot be empty")

        # Extract and validate arguments
        title = str(arguments["title"]).strip()
        if not title:
            raise ValueError("Title cannot be empty")

        messages = arguments["messages"]
        if not isinstance(messages, list):
            raise ValueError("Messages must be an array")

        # Validate message format
        for i, message in enumerate(messages):
            if not isinstance(message, dict):
                raise ValueError(f"Message {i} must be an object")
            if "role" not in message or "content" not in message:
                raise ValueError(f"Message {i} missing required fields: role, content")

        # Extract optional arguments
        out_dir_arg = arguments.get("out_dir")
        out_dir = Path(out_dir_arg) if out_dir_arg else Path.cwd().parent
        summary = arguments.get("summary", "")
        tags = arguments.get("tags", [])

        # Generate unique conversation ID
        conversation_id = _generate_conversation_id(title)

        # Create conversation metadata
        meta = ConversationMeta(
            conversation_id=conversation_id,
            topic=title,
            summary=summary,
            tags=tags,
            status=ConversationStatus.ACTIVE,
            version="1.0.0"
        )

        # Execute the write operation
        conversation_path = await self.writer.write(
            base_dir=out_dir,
            conversation_id=conversation_id,
            messages=messages,
            meta=meta
        )

        return {
            "conversation_path": str(conversation_path),
            "conversation_id": conversation_id,
            "meta": meta.model_dump(mode='json')
        }
