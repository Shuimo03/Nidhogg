"""Main entry point for the Nidhogg MCP server."""

from __future__ import annotations

import os
import sys
from pathlib import Path

if __package__ in (None, ""):
    package_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(package_root))
    __package__ = "nidhogg_mcp"

# Automatically change to project root directory (where pyproject.toml is located)
# This ensures the server works regardless of where it's launched from
_project_root = Path(__file__).resolve().parent.parent.parent
if (_project_root / "pyproject.toml").exists():
    os.chdir(_project_root)

from .server import main


if __name__ == "__main__":
    main()
