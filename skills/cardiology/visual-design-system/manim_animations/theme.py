"""
Shared Manim theme utilities for cardiology animations.
"""

from __future__ import annotations

from pathlib import Path
import sys

VISUAL_SYSTEM_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(VISUAL_SYSTEM_ROOT))

from tokens.index import get_tokens, get_color, get_accessible_pair


def _first_font_name(font_family: str, fallback: str) -> str:
    primary = font_family.split(",")[0].strip()
    return primary or fallback


PRIMARY_FONT = _first_font_name(get_tokens().get_font_family("primary"), "Arial")
MONO_FONT = _first_font_name(get_tokens().get_font_family("monospace"), "Courier")

COLORS = {
    "navy": get_color("primary.navy"),
    "blue": get_color("primary.blue"),
    "teal": get_color("primary.teal"),
    "success": get_color("semantic.success"),
    "warning": get_color("semantic.warning"),
    "danger": get_color("semantic.danger"),
    "neutral": get_color("semantic.neutral"),
    "text": get_color("text.primary"),
    "muted": get_color("text.muted"),
    "background": get_color("backgrounds.white"),
    "panel": get_color("backgrounds.light_gray"),
}

ACCESSIBLE_PAIR = get_accessible_pair("treatment_control")

FONT_SIZES = {
    "title": 44,
    "subtitle": 34,
    "label": 26,
    "small": 22,
}


def apply_theme(config, resolution: str = "1080p") -> None:
    """
    Apply a publication-style Manim config.

    Args:
        config: manim config object
        resolution: "1080p" or "4k"
    """
    config.background_color = COLORS["background"]
    config.frame_rate = 30

    if resolution == "4k":
        config.pixel_width = 3840
        config.pixel_height = 2160
    else:
        config.pixel_width = 1920
        config.pixel_height = 1080
