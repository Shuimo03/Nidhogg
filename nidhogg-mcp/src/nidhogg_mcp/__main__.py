"""Main entry point for the Nidhogg MCP server."""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ in (None, ""):
    package_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(package_root))
    __package__ = "nidhogg_mcp"

from .server import main


if __name__ == "__main__":
    main()
