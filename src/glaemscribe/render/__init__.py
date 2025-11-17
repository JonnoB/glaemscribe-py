"""
Font rendering module for Glaemscribe.

This module provides functionality to render Tengwar Unicode characters
as images, solving the "tofu" problem where users see boxes (□) instead
of Tengwar characters when they don't have appropriate fonts installed.

Planned features:
- PIL-based image rendering
- SVG output for web usage
- Base64 encoding for embedding
- Font management and fallback handling
"""

from .renderer import TengwarRenderer

__all__ = ['TengwarRenderer']
