"""
Base classes and interfaces for file writers.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import  Dict, List, Protocol

from ..models.meta import ConversationMeta


class FileWriter(ABC):
    """Abstract base class for file writers using Strategy pattern."""

    @abstractmethod
    async def write(
        self,
        base_dir: Path,
        conversation_id: str,
        messages: list[dict[str, str]],
        meta: ConversationMeta,
    ) -> None:
        """
        Write part or all of a conversation to storage.

        Implementations may write one file (Leaf) or
        coordinate multiple writers (Composite).
        """
        ...


class ConversationWriter(Protocol):
    """Protocol for writing complete conversation data to three-file system."""

    async def write_conversation(
        self,
        base_dir: Path,
        conversation_id: str,
        messages: List[Dict[str, str]],
        meta: ConversationMeta
    ) -> Path:
        """
        Write complete conversation to three-file system.
        Returns the conversation directory path.
        """
        ...