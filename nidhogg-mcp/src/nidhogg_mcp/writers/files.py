"""
JSON and JSONL file writers for meta.json and chunks.jsonl.
"""

import json
from pathlib import Path
from typing import Dict, List

from ..models.meta import ConversationMeta
from .base import FileWriter


class JSONWriter(FileWriter):
    """Leaf writer for meta.json files."""

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

        # Serialize metadata with JSON-compatible datetime format
        path = conversation_dir / "meta.json"
        data = meta.model_dump(mode="json")

        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


class JSONLWriter(FileWriter):
    """Leaf writer for chunks.jsonl files (empty in Phase 0)."""

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

        # Create empty chunks file for Phase 0
        path = conversation_dir / "chunks.jsonl"
        path.write_text("", encoding="utf-8")