"""
Visual Router for Carousel Generator v2

Intelligently routes slides to the optimal rendering tool:
- Pillow: Standard slides (fast, reliable)
- Plotly: Data visualization slides (charts, graphs)
- Gemini: Medical infographics (when accuracy is critical)
- Fal.ai: Hero/lifestyle images (photorealistic)
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum

from .models import SlideContent, SlideType, SlideRenderResult, CarouselConfig


class RenderTool(str, Enum):
    """Available rendering tools."""
    PILLOW = "pillow"       # Default, fast Python rendering
    PLOTLY = "plotly"       # Data visualization
    GEMINI = "gemini"       # AI-generated infographics
    FAL = "fal"             # AI-generated images
    MANIM = "manim"         # Educational animations
    SATORI = "satori"       # React to PNG (optional)
    PUPPETEER = "puppeteer" # React + Puppeteer (carousel renderer)


@dataclass
class RouteDecision:
    """Decision about which tool to use for rendering."""
    tool: RenderTool
    reason: str
    fallback: Optional[RenderTool] = None
    requires_api: bool = False


class VisualRouter:
    """
    Route slides to the optimal rendering tool.

    Considers slide type, content, and available resources.
    """

    def __init__(self, config: CarouselConfig = None):
        """
        Initialize the visual router.

        Args:
            config: Carousel configuration
        """
        self.config = config or CarouselConfig()

        # Check available tools
        self.available_tools = self._detect_available_tools()
        self.manim_bin = self._resolve_manim_bin()

    def _detect_available_tools(self) -> Dict[RenderTool, bool]:
        """Detect which rendering tools are available."""
        available = {
            RenderTool.PILLOW: True,  # Always available (Python dependency)
            RenderTool.PLOTLY: self._check_plotly(),
            RenderTool.GEMINI: self._check_gemini(),
            RenderTool.FAL: self._check_fal(),
            RenderTool.MANIM: self._check_manim(),
            RenderTool.SATORI: self._check_satori(),
            RenderTool.PUPPETEER: self._check_puppeteer(),
        }
        return available

    def _check_plotly(self) -> bool:
        """Check if Plotly is available."""
        try:
            import plotly
            import kaleido
            return True
        except ImportError:
            return False

    def _check_gemini(self) -> bool:
        """Check if Gemini API is configured."""
        return bool(os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"))

    def _check_fal(self) -> bool:
        """Check if Fal.ai is configured."""
        return bool(os.getenv("FAL_KEY"))

    def _check_satori(self) -> bool:
        """Check if Satori service is available."""
        # Would check for Node.js service running
        # For now, assume not available
        return False

    def _resolve_manim_bin(self) -> Optional[Path]:
        """Resolve Manim binary from config, env, or local venv."""
        if self.config and self.config.manim_bin:
            candidate = Path(self.config.manim_bin)
            if candidate.is_dir():
                candidate = candidate / "bin" / "manim"
            return candidate if candidate.exists() else None

        if self.config and self.config.manim_venv:
            candidate = Path(self.config.manim_venv) / "bin" / "manim"
            if candidate.exists():
                return candidate

        env_bin = os.getenv("MANIM_BIN")
        if env_bin:
            candidate = Path(env_bin)
            return candidate if candidate.exists() else None

        env_venv = os.getenv("MANIM_VENV")
        if env_venv:
            candidate = Path(env_venv) / "bin" / "manim"
            if candidate.exists():
                return candidate

        local_candidate = Path(__file__).resolve().parents[2] / "visual-design-system" / ".venv-manim" / "bin" / "manim"
        if local_candidate.exists():
            return local_candidate

        resolved = shutil.which("manim")
        return Path(resolved) if resolved else None

    def _check_manim(self) -> bool:
        """Check if Manim is available."""
        return self._resolve_manim_bin() is not None

    def _check_puppeteer(self) -> bool:
        """Check if Puppeteer renderer is available."""
        renderer_script = Path(__file__).parent.parent / "renderer" / "scripts" / "render.js"
        return renderer_script.exists()

    def route_slide(self, slide: SlideContent) -> RouteDecision:
        """
        Determine the best rendering tool for a slide.

        Args:
            slide: The slide content to render

        Returns:
            RouteDecision with tool selection and reasoning
        """
        slide_type = slide.slide_type

        # Data slides with charts should use Plotly
        if slide_type == SlideType.DATA and slide.chart_data:
            if self.available_tools[RenderTool.PLOTLY]:
                return RouteDecision(
                    tool=RenderTool.PLOTLY,
                    reason="Data slide with chart data - using Plotly for visualization",
                    fallback=RenderTool.PILLOW
                )

        # Stats slides with complex data might benefit from Plotly
        if slide_type == SlideType.STATS and slide.chart_type:
            if self.available_tools[RenderTool.PLOTLY]:
                return RouteDecision(
                    tool=RenderTool.PLOTLY,
                    reason="Stats slide with chart - using Plotly",
                    fallback=RenderTool.PILLOW
                )

        # Slides marked for AI-generated infographics
        if hasattr(slide, 'use_gemini') and slide.use_gemini:
            if self.available_tools[RenderTool.GEMINI]:
                return RouteDecision(
                    tool=RenderTool.GEMINI,
                    reason="Slide marked for AI infographic generation",
                    fallback=RenderTool.PILLOW,
                    requires_api=True
                )

        # Animation scenes (Manim)
        if slide.animation_scene:
            if self.available_tools[RenderTool.MANIM]:
                return RouteDecision(
                    tool=RenderTool.MANIM,
                    reason="Animation scene requested - using Manim",
                    fallback=RenderTool.PILLOW
                )
            return RouteDecision(
                tool=RenderTool.PILLOW,
                reason="Animation scene requested but Manim not available - falling back to Pillow",
                fallback=None
            )

        # Default to Puppeteer for standard slides if available
        if self.available_tools[RenderTool.PUPPETEER]:
            return RouteDecision(
                tool=RenderTool.PUPPETEER,
                reason="Standard slide - using Puppeteer renderer",
                fallback=RenderTool.PILLOW
            )

        return RouteDecision(
            tool=RenderTool.PILLOW,
            reason="Standard slide - using Pillow renderer",
            fallback=None
        )

    def route_carousel(self, slides: List[SlideContent]) -> Dict[int, RouteDecision]:
        """
        Route all slides in a carousel to their optimal tools.

        Args:
            slides: List of slide content

        Returns:
            Dictionary mapping slide number to route decision
        """
        routes = {}
        for slide in slides:
            routes[slide.slide_number] = self.route_slide(slide)
        return routes

    def get_tool_summary(self, routes: Dict[int, RouteDecision]) -> Dict[str, int]:
        """
        Get summary of tools used across carousel.

        Args:
            routes: Route decisions for all slides

        Returns:
            Count of slides per tool
        """
        summary = {}
        for decision in routes.values():
            tool_name = decision.tool.value
            summary[tool_name] = summary.get(tool_name, 0) + 1
        return summary

    def estimate_render_time(self, routes: Dict[int, RouteDecision]) -> float:
        """
        Estimate total render time based on tools used.

        Args:
            routes: Route decisions for all slides

        Returns:
            Estimated render time in seconds
        """
        # Approximate times per tool (seconds per slide)
        tool_times = {
            RenderTool.PILLOW: 0.1,
            RenderTool.PLOTLY: 0.5,
            RenderTool.GEMINI: 3.0,
            RenderTool.FAL: 5.0,
            RenderTool.MANIM: 8.0,
            RenderTool.SATORI: 0.3,
            RenderTool.PUPPETEER: 1.2,
        }

        total = 0.0
        for decision in routes.values():
            total += tool_times.get(decision.tool, 0.1)

        return total

    def estimate_cost(self, routes: Dict[int, RouteDecision]) -> float:
        """
        Estimate total cost based on tools used.

        Args:
            routes: Route decisions for all slides

        Returns:
            Estimated cost in USD
        """
        # Approximate costs per tool (USD per slide)
        tool_costs = {
            RenderTool.PILLOW: 0.0,
            RenderTool.PLOTLY: 0.0,
            RenderTool.GEMINI: 0.0,  # Free tier
            RenderTool.FAL: 0.03,
            RenderTool.MANIM: 0.0,
            RenderTool.SATORI: 0.0,
            RenderTool.PUPPETEER: 0.0,
        }

        total = 0.0
        for decision in routes.values():
            total += tool_costs.get(decision.tool, 0.0)

        return total


class PlotlyRenderer:
    """
    Render data visualization slides using Plotly.
    """

    def __init__(self, config: CarouselConfig = None):
        self.config = config or CarouselConfig()

    def render_bar_chart(self, slide: SlideContent, output_path: Path) -> SlideRenderResult:
        """Render a bar chart slide."""
        try:
            import plotly.graph_objects as go
            import plotly.io as pio

            # Extract chart data
            data = slide.chart_data or {}
            labels = data.get("labels", ["A", "B", "C"])
            values = data.get("values", [10, 20, 30])

            # Create figure
            fig = go.Figure(data=[
                go.Bar(
                    x=labels,
                    y=values,
                    marker_color='#207178'  # Primary brand color
                )
            ])

            # Style
            fig.update_layout(
                title=slide.title or "Data",
                plot_bgcolor='#F8F9FA',
                paper_bgcolor='#F8F9FA',
                font=dict(family="Inter", size=14),
                width=1080,
                height=1350 if self.config.aspect_ratio.value == "4:5" else 1080,
                margin=dict(l=80, r=80, t=120, b=80)
            )

            # Save
            pio.write_image(fig, str(output_path), format='png')

            return SlideRenderResult(
                slide_number=slide.slide_number,
                output_path=output_path,
                width=fig.layout.width,
                height=fig.layout.height,
                render_time_ms=500,  # Approximate
                renderer_used="plotly"
            )

        except Exception as e:
            raise RuntimeError(f"Plotly rendering failed: {e}")


class ManimRenderer:
    """
    Render animation scenes using Manim via the shared CLI wrapper.
    """

    QUALITY_SIZES = {
        "l": (854, 480),
        "m": (1280, 720),
        "h": (1920, 1080),
        "k": (3840, 2160),
    }

    def __init__(self, config: CarouselConfig = None, manim_bin: Optional[Path] = None):
        self.config = config or CarouselConfig()
        self.manim_bin = manim_bin
        self.render_script = Path(__file__).resolve().parents[2] / "visual-design-system" / "scripts" / "render_manim.py"
        self.catalog_path = Path(__file__).resolve().parents[2] / "visual-design-system" / "manim_animations" / "scene_catalog.json"
        self.scene_catalog = self._load_scene_catalog()
        self.scene_map = {key: entry["class"] for key, entry in self.scene_catalog.items()}

    def _load_scene_catalog(self) -> Dict[str, Dict[str, str]]:
        if not self.catalog_path.exists():
            raise RuntimeError(f"Manim scene catalog not found: {self.catalog_path}")
        with open(self.catalog_path, "r") as handle:
            return json.load(handle)

    def render_scene(self, slide: SlideContent, output_dir: Path) -> SlideRenderResult:
        if not slide.animation_scene:
            raise ValueError("animation_scene is required for Manim rendering")

        scene_key = slide.animation_scene
        if scene_key not in self.scene_map:
            raise ValueError(f"Unknown Manim scene key: {scene_key}")

        quality = slide.animation_quality or "l"
        fmt = slide.animation_format or "mp4"

        if not self.manim_bin or not Path(self.manim_bin).exists():
            raise RuntimeError("Manim binary not found. Set MANIM_BIN, MANIM_VENV, or config.manim_venv.")

        cmd = [
            sys.executable,
            str(self.render_script),
            scene_key,
            "--quality",
            quality,
            "--format",
            fmt,
            "--output-dir",
            str(output_dir),
            "--manim-bin",
            str(self.manim_bin),
        ]

        completed = subprocess.run(cmd, check=False)
        if completed.returncode != 0:
            raise RuntimeError(f"Manim render failed for scene: {scene_key}")

        scene_class = self.scene_map[scene_key]
        matches = list((output_dir / "videos" / "scenes").rglob(f"{scene_class}.{fmt}"))
        output_path = matches[-1] if matches else output_dir
        width, height = self.QUALITY_SIZES.get(quality, (1920, 1080))

        return SlideRenderResult(
            slide_number=slide.slide_number,
            output_path=output_path,
            width=width,
            height=height,
            render_time_ms=8000,
            renderer_used="manim"
        )

    def render_forest_plot(self, slide: SlideContent, output_path: Path) -> SlideRenderResult:
        """Render a forest plot for clinical trial data."""
        try:
            import plotly.graph_objects as go
            import plotly.io as pio

            data = slide.chart_data or {}

            # Default forest plot data
            studies = data.get("studies", ["Study A", "Study B", "Study C"])
            estimates = data.get("estimates", [0.8, 0.75, 0.85])
            ci_lower = data.get("ci_lower", [0.6, 0.5, 0.7])
            ci_upper = data.get("ci_upper", [1.0, 1.0, 1.0])

            fig = go.Figure()

            # Add confidence intervals as lines
            for i, study in enumerate(studies):
                fig.add_trace(go.Scatter(
                    x=[ci_lower[i], ci_upper[i]],
                    y=[study, study],
                    mode='lines',
                    line=dict(color='#207178', width=2),
                    showlegend=False
                ))

            # Add point estimates
            fig.add_trace(go.Scatter(
                x=estimates,
                y=studies,
                mode='markers',
                marker=dict(color='#207178', size=12, symbol='square'),
                name='Estimate'
            ))

            # Add vertical line at 1 (no effect)
            fig.add_vline(x=1, line_dash="dash", line_color="gray")

            fig.update_layout(
                title=slide.title or "Forest Plot",
                xaxis_title="Hazard Ratio (95% CI)",
                plot_bgcolor='#F8F9FA',
                paper_bgcolor='#F8F9FA',
                font=dict(family="Inter", size=14),
                width=1080,
                height=1350 if self.config.aspect_ratio.value == "4:5" else 1080,
                margin=dict(l=150, r=80, t=120, b=80)
            )

            pio.write_image(fig, str(output_path), format='png')

            return SlideRenderResult(
                slide_number=slide.slide_number,
                output_path=output_path,
                width=fig.layout.width,
                height=fig.layout.height,
                render_time_ms=600,
                renderer_used="plotly"
            )

        except Exception as e:
            raise RuntimeError(f"Plotly rendering failed: {e}")


def route_and_render(slides: List[SlideContent],
                    config: CarouselConfig = None) -> Tuple[Dict[int, RouteDecision], List[SlideRenderResult]]:
    """
    Route slides to tools and render them.

    Args:
        slides: List of slide content
        config: Carousel configuration

    Returns:
        Tuple of (route decisions, render results)
    """
    from .pillow_renderer import PillowRenderer

    router = VisualRouter(config)
    routes = router.route_carousel(slides)

    # Print routing summary
    summary = router.get_tool_summary(routes)
    print(f"Rendering with: {summary}")
    print(f"Estimated time: {router.estimate_render_time(routes):.1f}s")
    print(f"Estimated cost: ${router.estimate_cost(routes):.2f}")

    # Initialize renderers
    pillow = PillowRenderer(config)
    plotly_renderer = PlotlyRenderer(config) if router.available_tools[RenderTool.PLOTLY] else None
    manim_renderer = ManimRenderer(config, router.manim_bin) if router.available_tools[RenderTool.MANIM] else None

    # Render each slide
    results = []
    output_dir = config.output_dir if config else Path("output/carousels")
    output_dir.mkdir(parents=True, exist_ok=True)
    manim_output_dir = output_dir / "manim"
    manim_output_dir.mkdir(parents=True, exist_ok=True)

    for slide in slides:
        route = routes[slide.slide_number]

        if route.tool == RenderTool.MANIM and manim_renderer:
            try:
                result = manim_renderer.render_scene(slide, manim_output_dir)
            except Exception as e:
                print(f"Manim failed, falling back to Pillow: {e}")
                result = pillow.render_slide(slide)
        elif route.tool == RenderTool.PLOTLY and plotly_renderer:
            output_path = output_dir / f"slide-{slide.slide_number:02d}.png"
            chart_type = slide.chart_type or "bar"

            try:
                if chart_type == "bar":
                    result = plotly_renderer.render_bar_chart(slide, output_path)
                elif chart_type == "line":
                    result = plotly_renderer.render_line_chart(slide, output_path)
                elif chart_type == "forest":
                    result = plotly_renderer.render_forest_plot(slide, output_path)
                else:
                    result = pillow.render_slide(slide)
            except Exception as e:
                print(f"Plotly failed, falling back to Pillow: {e}")
                result = pillow.render_slide(slide)
        else:
            # Default to Pillow
            result = pillow.render_slide(slide)

        results.append(result)
        print(f"  Rendered slide {slide.slide_number}: {result.renderer_used}")

    return routes, results
