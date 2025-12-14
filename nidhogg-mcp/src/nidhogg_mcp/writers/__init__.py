"""
File writers for Nidhogg three-file system.

This module implements the Composite pattern for coordinating
multiple file format writers in the three-file system.
"""

from pathlib import Path

from ..models.meta import ConversationMeta
from .base import FileWriter, ConversationWriter
from .markdown import MarkdownWriter
from .files import JSONWriter, JSONLWriter


class ThreeFileWriter(FileWriter):
    """
    Composite writer that coordinates all three file writers.

    This is the main interface that client code should use.
    It coordinates writing to all three files in the Nidhogg system:
    - conversation.md (via MarkdownWriter)
    - meta.json (via JSONWriter)
    - chunks.jsonl (via JSONLWriter)
    """

    def __init__(self):
        self.writers = [
            MarkdownWriter(),
            JSONWriter(),
            JSONLWriter()
        ]

    async def write(
        self,
        base_dir: Path,
        conversation_id: str,
        messages: list[dict[str, str]],
        meta: ConversationMeta,
    ) -> Path:
        """Write all three files for the conversation."""
        # Validate conversation_id
        if not conversation_id or "/" in conversation_id or "\\" in conversation_id:
            raise ValueError(f"Invalid conversation_id: {conversation_id}")

        # Ensure base directory exists
        base_dir.mkdir(parents=True, exist_ok=True)

        # Execute all writers
        for writer in self.writers:
            await writer.write(base_dir, conversation_id, messages, meta)

        # Return the conversation directory path
        return base_dir / conversation_id


# Export the public interface
__all__ = [
    "ThreeFileWriter",
    "FileWriter",
    "ConversationWriter",
    "ConversationMeta"
]