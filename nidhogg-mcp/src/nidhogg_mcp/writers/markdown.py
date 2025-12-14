"""
Markdown file writer for conversation.md generation.
"""

from pathlib import Path
from ..models.meta import ConversationMeta
from .base import FileWriter


def _generate_markdown(
        messages: list[dict[str, str]], meta: ConversationMeta
) -> str:
    """Generate the complete markdown content for a conversation."""
    markdown_context: list[str] = [
        f"# {meta.topic}",
        "",
        f"**Created:** {meta.created_at.isoformat()}",
        f"**Status:** {meta.status.value}",
        f"**Summary:** {meta.summary or 'No summary available'}",
        "",
        "---",
        "",
    ]

    for message in messages:
        role = message.get("role", "unknown")
        content = message.get("content", "")

        markdown_context.append(f"## {role.title()}")
        markdown_context.append("")
        markdown_context.append(content)
        markdown_context.append("")

    return "\n".join(markdown_context)


class MarkdownWriter(FileWriter):
    """Leaf writer for conversation.md files."""

    async def write(
        self,
        base_dir: Path,
        conversation_id: str,
        messages: list[dict[str, str]],
        meta: ConversationMeta,
    ) -> None:
        # Create conversation directory
        conversation_dir = base_dir / conversation_id
        conversation_dir.mkdir(parents=True, exist_ok=True)

        # Generate markdown
        path = conversation_dir / "conversation.md"
        markdown_content = _generate_markdown(messages, meta)
        path.write_text(markdown_content, encoding="utf-8")

