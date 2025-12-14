"""
Meta.json data models for Nidhogg conversation storage.

This module defines the schema for meta.json files in the three-file system.
According to the PRD, meta.json contains structured metadata including:
- topic, summary, decisions, tags, status
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
import uuid

# 这里状态是可以后期通过修改 meta.json 去修改，后期加入自动修改
class ConversationStatus(Enum):
    """Status of a conversation in the knowledge base."""
    ACTIVE = "active" # 处于对话阶段
    FROZEN = "frozen" # 当前对话完成设计
    DEPRECATED = "deprecated" #修改上一轮对话设计，继续对话


class Decision(BaseModel):
    """
    A stable decision extracted from a conversation.

    Phase 0 design principles:
    - Human-readable
    - Referencable
    - Minimal but sufficient
    """

    id: str = Field(
        ...,
        description="Stable identifier within a conversation, e.g. D1, D2"
    )

    text: str = Field(
        ...,
        description="The decision statement itself"
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(datetime.UTC),
        description="When this decision was recorded"
    )

    note: Optional[str] = Field(
        default=None,
        description="Optional human note or clarification"
    )


class ConversationMeta(BaseModel):
    """
    Main metadata model for conversation.md files.

    This represents the complete schema for meta.json v0.
    All database/vector content must be rebuildable from this + conversation.md.
    """
    # TODO(human): Fix the field definitions below
    # Current issues:
    # 1. Add Field() definitions for all fields
    # 2. Add conversation_id field (missing)
    # 3. Fix field names: created->created_at, updated->updated_at
    # 4. Add proper default values and descriptions
    # 5. Consider which fields should be optional vs required

    conversation_id: str = Field(
        ...,
        description="Stable identifier for this conversation (directory name)"
    )

    topic: str = Field(
        ...,
        description="Primary topic or theme of the conversation"
    )

    summary: str = Field(
        "",
        description="Human-readable summary of the conversation"
    )

    decisions: List[Decision] = Field(
        default_factory=list,
        description="Key decisions extracted from the conversation"
    )

    tags: List[str] = Field(
        default_factory=list,
        description="Free-form tags for classification and search"
    )

    status: ConversationStatus = Field(
        default=ConversationStatus.ACTIVE,
        description="Lifecycle status of the conversation"
    )

    version: str = Field(
        "v0",
        description="Schema version for meta.json"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When this conversation metadata was first created"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When this conversation metadata was last updated"
    )