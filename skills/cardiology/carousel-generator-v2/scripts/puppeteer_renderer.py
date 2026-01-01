#!/usr/bin/env python3
"""
Puppeteer-based Carousel Renderer

Uses a React + Puppeteer pipeline to render high-quality carousel slides.
This replaces the Satori-based renderer which had issues with emoji rendering.

Usage:
    from puppeteer_renderer import PuppeteerRenderer

    renderer = PuppeteerRenderer()
    slides = [
        {
            "type": "hook",
            "data": {
                "slideNumber": 1,
                "totalSlides": 6,
                "headline": "5 Statin Myths Debunked",
                "subtitle": "What the science says",
                "icon": "Pill",
                "theme": "teal"
            }
        },
        # ... more slides
    ]
    output_paths = renderer.render_carousel(slides, output_dir="./output")
"""

import json
import os
import subprocess
import tempfile
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Union

# Import models for type hints and enum values
try:
    from .models import SlideContent, SlideType, ColorMode, SlideRenderResult
    MODELS_AVAILABLE = True
except ImportError:
    MODELS_AVAILABLE = False
    SlideContent = None
    SlideType = None
    ColorMode = None
    SlideRenderResult = None


DIMENSIONS = {
    "square": {"width": 1080, "height": 1080},
    "portrait": {"width": 1080, "height": 1350},
}


class PuppeteerRenderer:
    """Renders carousel slides using React + Puppeteer."""

    def __init__(self, renderer_dir: Optional[str] = None, dimensions: str = "portrait"):
        """
        Initialize the renderer.

        Args:
            renderer_dir: Path to the renderer React project. If None, uses default location.
            dimensions: Output dimensions ("square" or "portrait").
        """
        if renderer_dir:
            self.renderer_dir = Path(renderer_dir)
        else:
            # Default to the renderer directory in this project
            self.renderer_dir = Path(__file__).parent.parent / "renderer"

        self.render_script = self.renderer_dir / "scripts" / "render.js"
        self.dimensions = dimensions if dimensions in DIMENSIONS else "square"
        self.width = DIMENSIONS[self.dimensions]["width"]
        self.height = DIMENSIONS[self.dimensions]["height"]

        # Verify the renderer exists
        if not self.render_script.exists():
            raise FileNotFoundError(
                f"Render script not found at {self.render_script}. "
                "Make sure npm dependencies are installed."
            )

    def _normalize_icon_name(self, icon: Optional[str]) -> Optional[str]:
        """Normalize icon names to lucide-react PascalCase where possible."""
        if not icon:
            return None

        lookup = {
            "heart": "Heart",
            "pill": "Pill",
            "chart": "TrendingUp",
            "chartup": "TrendingUp",
            "chart-up": "TrendingUp",
            "trendingup": "TrendingUp",
            "running": "Activity",
            "exercise": "Activity",
            "clock": "Clock",
            "message": "MessageCircle",
            "messagecircle": "MessageCircle",
            "salad": "Salad",
            "food": "Salad",
            "quote": "Quote",
            "star": "Star",
            "shield": "Shield",
        }

        normalized = icon.strip().replace(" ", "").replace("_", "").replace("-", "").lower()
        return lookup.get(normalized, icon)

    def _split_context_source(
        self,
        context: str,
        source: Optional[str] = None
    ) -> (str, Optional[str]):
        """Split context into context + source when encoded as 'context - source'."""
        if source:
            return context, source
        if not context:
            return context, source
        if " - " in context:
            left, right = context.split(" - ", 1)
            return left.strip(), right.strip()
        if " — " in context:
            left, right = context.split(" — ", 1)
            return left.strip(), right.strip()
        return context, source

    def _slide_content_to_render_data(
        self,
        slide: Any,
        slide_number: int,
        total_slides: int,
    ) -> Dict[str, Any]:
        """Convert SlideContent to renderer slide data."""
        slide_type = slide.slide_type.value if hasattr(slide.slide_type, "value") else str(slide.slide_type)
        color_mode = slide.color_mode.value if hasattr(slide.color_mode, "value") else str(slide.color_mode)
        theme = "teal" if color_mode != "dark" else "red"

        if slide_type == "hook":
            return {
                "type": "hook",
                "data": {
                    "slideNumber": slide_number,
                    "totalSlides": total_slides,
                    "headline": slide.title or "Evidence-Based Cardiology",
                    "subtitle": slide.subtitle or slide.body or "",
                    "icon": self._normalize_icon_name(slide.icon_name or "Heart"),
                    "theme": theme,
                    "dimensions": self.dimensions,
                },
            }

        if slide_type == "myth":
            return {
                "type": "myth",
                "data": {
                    "slideNumber": slide_number,
                    "totalSlides": total_slides,
                    "myth": slide.myth_text or "",
                    "truth": slide.truth_text or "",
                    "source": slide.source or "",
                    "dimensions": self.dimensions,
                },
            }

        if slide_type in ["stats", "data"]:
            context, source = self._split_context_source(
                slide.stat_context or slide.body or "",
                slide.source
            )
            return {
                "type": "stat",
                "data": {
                    "slideNumber": slide_number,
                    "totalSlides": total_slides,
                    "stat": slide.statistic or "",
                    "label": slide.stat_label or slide.title or "",
                    "context": context,
                    "source": source or "",
                    "icon": self._normalize_icon_name(slide.icon_name or "TrendingUp"),
                    "color": "green" if slide_type == "stats" else "teal",
                    "dimensions": self.dimensions,
                },
            }

        if slide_type in ["tips", "steps"]:
            tips = []
            if slide.bullet_points:
                for point in slide.bullet_points:
                    tips.append({"text": point})
            if slide.steps:
                for step in slide.steps:
                    tips.append({"text": step})
            if not tips:
                tips.append({"text": slide.body or slide.title or "Key takeaway"})

            return {
                "type": "tips",
                "data": {
                    "slideNumber": slide_number,
                    "totalSlides": total_slides,
                    "title": slide.title or "Key Tips",
                    "tips": tips,
                    "dimensions": self.dimensions,
                },
            }

        if slide_type == "quote":
            return {
                "type": "stat",
                "data": {
                    "slideNumber": slide_number,
                    "totalSlides": total_slides,
                    "stat": "“”",
                    "label": slide.quote_text or "",
                    "context": f"— {slide.quote_author}" if slide.quote_author else "",
                    "source": "",
                    "icon": "Quote",
                    "color": "teal",
                    "dimensions": self.dimensions,
                },
            }

        if slide_type == "comparison":
            return {
                "type": "myth",
                "data": {
                    "slideNumber": slide_number,
                    "totalSlides": total_slides,
                    "myth": slide.before_text or "Common approach",
                    "truth": slide.after_text or "Better approach",
                    "source": "",
                    "dimensions": self.dimensions,
                },
            }

        if slide_type == "story":
            return {
                "type": "stat",
                "data": {
                    "slideNumber": slide_number,
                    "totalSlides": total_slides,
                    "stat": slide.title or "Real story",
                    "label": slide.body or "",
                    "context": "",
                    "source": "",
                    "icon": "Heart",
                    "color": "teal",
                    "dimensions": self.dimensions,
                },
            }

        if slide_type == "cta":
            return {
                "type": "cta",
                "data": {
                    "slideNumber": slide_number,
                    "totalSlides": total_slides,
                    "name": "Dr Shailesh Singh",
                    "credentials": "Cardiologist | Evidence-Based Medicine",
                    "handle": slide.cta_handle or "@dr.shailesh.singh",
                    "valueProposition": slide.cta_text or "Follow for evidence-based cardiology",
                    "secondaryText": "",
                    "followerCount": "",
                    "dimensions": self.dimensions,
                },
            }

        return {
            "type": "tips",
            "data": {
                "slideNumber": slide_number,
                "totalSlides": total_slides,
                "title": slide.title or "Key Point",
                "tips": [{"text": slide.body or slide.title or "Important insight"}],
                "dimensions": self.dimensions,
            },
        }

    def render_slide(
        self,
        slide_data: Dict[str, Any],
        output_path: str
    ) -> str:
        """
        Render a single slide to PNG.

        Args:
            slide_data: Slide data dictionary with 'type' and 'data' keys
            output_path: Path to save the PNG file

        Returns:
            Path to the rendered PNG file
        """
        # Validate slide data
        if "type" not in slide_data:
            raise ValueError("Slide data must have 'type' key")
        if "data" not in slide_data:
            raise ValueError("Slide data must have 'data' key")

        # Run the Node.js render script
        result = subprocess.run(
            [
                "node",
                str(self.render_script),
                "--slide",
                json.dumps(slide_data),
                "--output",
                output_path,
                "--width",
                str(self.width),
                "--height",
                str(self.height),
            ],
            cwd=str(self.renderer_dir),
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            raise RuntimeError(f"Render failed: {result.stderr}")

        return output_path

    def render_carousel(
        self,
        slides: List[Union[Dict[str, Any], Any]],
        output_dir: str = "./output",
        filename_prefix: str = "carousel_slide"
    ) -> List[Any]:
        """
        Render multiple slides to PNG files.

        Args:
            slides: List of slide data dictionaries
            output_dir: Directory to save PNG files
            filename_prefix: Prefix for output filenames

        Returns:
            List of SlideRenderResult objects or file paths
        """
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        normalized_slides = slides
        if slides and MODELS_AVAILABLE and SlideContent and hasattr(slides[0], "slide_type"):
            normalized_slides = []
            total_slides = len(slides)
            for i, slide in enumerate(slides, 1):
                normalized_slides.append(
                    self._slide_content_to_render_data(slide, i, total_slides)
                )

        # Write slides to temp JSON file
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False
        ) as f:
            json.dump(normalized_slides, f)
            input_file = f.name

        start_time = time.time()
        try:
            # Run the Node.js render script
            result = subprocess.run(
                [
                    "node",
                    str(self.render_script),
                    "--input",
                    input_file,
                    "--output",
                    str(output_path),
                    "--width",
                    str(self.width),
                    "--height",
                    str(self.height),
                ],
                cwd=str(self.renderer_dir),
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode != 0:
                raise RuntimeError(f"Render failed: {result.stderr}")

            # Return list of output files
            output_files = sorted(output_path.glob("slide_*.png"))
            if MODELS_AVAILABLE and SlideRenderResult:
                render_time = (time.time() - start_time) * 1000
                per_slide = render_time / max(len(output_files), 1)
                return [
                    SlideRenderResult(
                        slide_number=i + 1,
                        output_path=f,
                        width=self.width,
                        height=self.height,
                        render_time_ms=per_slide,
                        renderer_used="puppeteer",
                        warnings=None,
                    )
                    for i, f in enumerate(output_files)
                ]
            return [str(f) for f in output_files]

        finally:
            # Clean up temp file
            os.unlink(input_file)

    def create_hook_slide(
        self,
        slide_number: int,
        total_slides: int,
        headline: str,
        subtitle: Optional[str] = None,
        icon: Optional[str] = None,
        theme: str = "teal"
    ) -> Dict[str, Any]:
        """Create a hook slide data structure."""
        return {
            "type": "hook",
            "data": {
                "slideNumber": slide_number,
                "totalSlides": total_slides,
                "headline": headline,
                "subtitle": subtitle,
                "icon": self._normalize_icon_name(icon),
                "theme": theme,
                "dimensions": self.dimensions,
            }
        }

    def create_myth_slide(
        self,
        slide_number: int,
        total_slides: int,
        myth: str,
        truth: str,
        source: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a myth/truth slide data structure."""
        return {
            "type": "myth",
            "data": {
                "slideNumber": slide_number,
                "totalSlides": total_slides,
                "myth": myth,
                "truth": truth,
                "source": source,
                "dimensions": self.dimensions,
            }
        }

    def create_stat_slide(
        self,
        slide_number: int,
        total_slides: int,
        stat: str,
        label: str,
        context: Optional[str] = None,
        source: Optional[str] = None,
        icon: Optional[str] = None,
        color: str = "teal"
    ) -> Dict[str, Any]:
        """Create a statistics slide data structure."""
        return {
            "type": "stat",
            "data": {
                "slideNumber": slide_number,
                "totalSlides": total_slides,
                "stat": stat,
                "label": label,
                "context": context,
                "source": source,
                "icon": self._normalize_icon_name(icon),
                "color": color,
                "dimensions": self.dimensions,
            }
        }

    def create_tips_slide(
        self,
        slide_number: int,
        total_slides: int,
        title: str,
        tips: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Create a tips slide data structure.

        Args:
            tips: List of dicts with 'text' and optional 'icon' keys
        """
        return {
            "type": "tips",
            "data": {
                "slideNumber": slide_number,
                "totalSlides": total_slides,
                "title": title,
                "tips": tips,
                "dimensions": self.dimensions,
            }
        }

    def create_cta_slide(
        self,
        slide_number: int,
        total_slides: int,
        value_proposition: str,
        name: str = "Dr Shailesh Singh",
        credentials: str = "Cardiologist | Evidence-Based Medicine",
        handle: str = "@dr.shailesh.singh",
        secondary_text: Optional[str] = None,
        follower_count: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a CTA slide data structure."""
        return {
            "type": "cta",
            "data": {
                "slideNumber": slide_number,
                "totalSlides": total_slides,
                "name": name,
                "credentials": credentials,
                "handle": handle,
                "valueProposition": value_proposition,
                "secondaryText": secondary_text,
                "followerCount": follower_count,
                "dimensions": self.dimensions,
            }
        }


def main():
    """Test the renderer with sample slides."""
    renderer = PuppeteerRenderer()

    # Create test slides
    slides = [
        renderer.create_hook_slide(
            slide_number=1,
            total_slides=5,
            headline="5 Statin Myths That Need to Die",
            subtitle="What the science actually says",
            icon="Pill",
            theme="teal"
        ),
        renderer.create_myth_slide(
            slide_number=2,
            total_slides=5,
            myth="Statins cause muscle pain in everyone",
            truth="Only 5-10% experience muscle symptoms, and it's usually mild",
            source="Lancet 2022"
        ),
        renderer.create_stat_slide(
            slide_number=3,
            total_slides=5,
            stat="25%",
            label="Reduction in Heart Attack Risk",
            context="For every 1 mmol/L reduction in LDL",
            source="CTT Meta-analysis",
            icon="Heart",
            color="green"
        ),
        renderer.create_tips_slide(
            slide_number=4,
            total_slides=5,
            title="3 Tips for Statin Success",
            tips=[
                {"text": "Take at the same time daily", "icon": "Clock"},
                {"text": "Report symptoms early", "icon": "MessageCircle"},
                {"text": "Combine with lifestyle changes", "icon": "Salad"}
            ]
        ),
        renderer.create_cta_slide(
            slide_number=5,
            total_slides=5,
            value_proposition="Follow for evidence-based cardiology",
            secondary_text="New posts every week",
            follower_count="50K+"
        )
    ]

    # Render
    output_dir = Path(__file__).parent.parent / "outputs" / "test_carousel"
    output_files = renderer.render_carousel(slides, str(output_dir))

    print(f"\nRendered {len(output_files)} slides:")
    for f in output_files:
        print(f"  - {f}")


if __name__ == "__main__":
    main()
