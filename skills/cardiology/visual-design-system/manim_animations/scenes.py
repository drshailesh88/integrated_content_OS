"""
Manim scenes for cardiology education animations.
"""

from __future__ import annotations

from typing import List, Tuple

from manim import (
    Dot,
    FadeIn,
    Line,
    Scene,
    Text,
    VGroup,
    VMobject,
    config,
    Create,
    UP,
    DOWN,
    LEFT,
    RIGHT,
)

import theme
from primitives import heart_chambers
from templates import (
    AnatomyChambersScene,
    BarScene,
    ComparisonScene,
    FlowScene,
    ForestPlotScene,
    KaplanMeierBaseScene,
    LineScene,
    PanelGridScene,
    TimelineScene,
)

theme.apply_theme(config)


class MechanismOfActionScene(FlowScene):
    TITLE = "Mechanism of Action"
    STEPS = [
        ("Drug", theme.COLORS["blue"]),
        ("Receptor", theme.COLORS["teal"]),
        ("Signal", theme.COLORS["success"]),
        ("Outcome", theme.COLORS["navy"]),
    ]
    OUTCOME = "24% lower HF hospitalization"


class KaplanMeierScene(KaplanMeierBaseScene):
    TITLE = "Event-Free Survival"
    TREATMENT_POINTS = [(0, 1.0), (6, 0.94), (12, 0.88), (18, 0.83), (24, 0.78)]
    CONTROL_POINTS = [(0, 1.0), (6, 0.91), (12, 0.83), (18, 0.76), (24, 0.69)]
    HR_TEXT = "HR 0.76 (95% CI 0.64-0.90)"


class ECGWaveScene(Scene):
    def construct(self) -> None:
        title = Text(
            "ECG: Normal Sinus Rhythm",
            font=theme.PRIMARY_FONT,
            font_size=theme.FONT_SIZES["title"],
            color=theme.COLORS["navy"],
        ).to_edge(UP)

        baseline = Line(LEFT * 5.5, RIGHT * 5.5, color=theme.COLORS["muted"]).shift(DOWN * 0.5)

        points = [
            LEFT * 5.5 + DOWN * 0.5,
            LEFT * 4.7 + DOWN * 0.35,
            LEFT * 4.0 + DOWN * 0.5,
            LEFT * 3.4 + UP * 0.3,
            LEFT * 3.2 + DOWN * 0.85,
            LEFT * 2.7 + DOWN * 0.5,
            LEFT * 1.6 + DOWN * 0.4,
            LEFT * 0.3 + DOWN * 0.5,
            RIGHT * 0.7 + DOWN * 0.15,
            RIGHT * 1.8 + DOWN * 0.5,
            RIGHT * 5.5 + DOWN * 0.5,
        ]

        wave = _ecg_wave(points, theme.COLORS["blue"])

        labels = VGroup(
            Text("P", font=theme.PRIMARY_FONT, font_size=theme.FONT_SIZES["small"], color=theme.COLORS["text"]).next_to(LEFT * 4.3 + DOWN * 0.1, UP),
            Text("QRS", font=theme.PRIMARY_FONT, font_size=theme.FONT_SIZES["small"], color=theme.COLORS["text"]).next_to(LEFT * 3.2 + DOWN * 0.1, UP),
            Text("T", font=theme.PRIMARY_FONT, font_size=theme.FONT_SIZES["small"], color=theme.COLORS["text"]).next_to(RIGHT * 0.7 + DOWN * 0.1, UP),
        )

        self.play(FadeIn(title))
        self.play(Create(baseline))
        self.play(Create(wave))
        self.play(FadeIn(labels))
        self.wait(0.5)


class ECGAtrialFibrillationScene(Scene):
    def construct(self) -> None:
        title = Text(
            "ECG: Atrial Fibrillation",
            font=theme.PRIMARY_FONT,
            font_size=theme.FONT_SIZES["title"],
            color=theme.COLORS["navy"],
        ).to_edge(UP)

        baseline = Line(LEFT * 5.5, RIGHT * 5.5, color=theme.COLORS["muted"]).shift(DOWN * 0.5)

        points = [
            LEFT * 5.5 + DOWN * 0.4,
            LEFT * 4.6 + DOWN * 0.7,
            LEFT * 4.1 + DOWN * 0.2,
            LEFT * 3.6 + DOWN * 0.9,
            LEFT * 3.0 + UP * 0.4,
            LEFT * 2.8 + DOWN * 0.8,
            LEFT * 2.2 + DOWN * 0.3,
            LEFT * 1.5 + DOWN * 0.7,
            LEFT * 0.7 + UP * 0.2,
            RIGHT * 0.2 + DOWN * 0.6,
            RIGHT * 1.2 + DOWN * 0.1,
            RIGHT * 2.1 + DOWN * 0.8,
            RIGHT * 3.0 + DOWN * 0.3,
            RIGHT * 3.8 + DOWN * 0.7,
            RIGHT * 5.5 + DOWN * 0.5,
        ]

        wave = _ecg_wave(points, theme.COLORS["danger"])

        note = Text(
            "Irregularly irregular rhythm",
            font=theme.PRIMARY_FONT,
            font_size=theme.FONT_SIZES["small"],
            color=theme.COLORS["text"],
        ).next_to(baseline, DOWN, buff=0.5)

        self.play(FadeIn(title))
        self.play(Create(baseline))
        self.play(Create(wave))
        self.play(FadeIn(note))
        self.wait(0.5)


class SGLT2MechanismScene(FlowScene):
    TITLE = "SGLT2 Inhibitor Mechanism"
    STEPS = [
        ("SGLT2 block", theme.COLORS["blue"]),
        ("Natriuresis", theme.COLORS["teal"]),
        ("Lower preload", theme.COLORS["success"]),
        ("HF stability", theme.COLORS["navy"]),
    ]
    OUTCOME = "30% lower HF hospitalization"


class GLP1MechanismScene(FlowScene):
    TITLE = "GLP-1 Agonist Pathway"
    STEPS = [
        ("GLP-1 agonist", theme.COLORS["blue"]),
        ("Weight loss", theme.COLORS["teal"]),
        ("Lower inflammation", theme.COLORS["success"]),
        ("MACE reduction", theme.COLORS["navy"]),
    ]
    OUTCOME = "HR 0.86 for MACE"


class ARNIPathwayScene(FlowScene):
    TITLE = "ARNi Mechanism"
    STEPS = [
        ("ARNi", theme.COLORS["blue"]),
        ("Lower Ang II", theme.COLORS["teal"]),
        ("Raise natriuretic peptides", theme.COLORS["success"]),
        ("Reverse remodeling", theme.COLORS["navy"]),
    ]
    OUTCOME = "20% lower CV death"


class HFQuadTherapyScene(FlowScene):
    TITLE = "HFrEF Quad Therapy"
    STEPS = [
        ("ARNi/ACEi", theme.COLORS["blue"]),
        ("Beta-blocker", theme.COLORS["teal"]),
        ("MRA", theme.COLORS["success"]),
        ("SGLT2i", theme.COLORS["navy"]),
    ]
    OUTCOME = "4-pillar GDMT"


class LDLReductionScene(BarScene):
    TITLE = "LDL-C Reduction Ladder"
    BARS = [
        ("Baseline", 130, theme.COLORS["neutral"]),
        ("Statin", 80, theme.COLORS["blue"]),
        ("+Eze", 60, theme.COLORS["teal"]),
        ("PCSK9", 35, theme.COLORS["success"]),
    ]
    FOOTNOTE = "Lower is better"


class BloodPressureTargetsScene(BarScene):
    TITLE = "Blood Pressure Targets"
    BARS = [
        ("Baseline", 148, theme.COLORS["neutral"]),
        ("Standard", 130, theme.COLORS["blue"]),
        ("Intensive", 120, theme.COLORS["teal"]),
    ]
    FOOTNOTE = "Target SBP in mmHg"


class ACSPathwayScene(FlowScene):
    TITLE = "ACS Rapid Pathway"
    STEPS = [
        ("Chest pain", theme.COLORS["warning"]),
        ("ECG", theme.COLORS["blue"]),
        ("STEMI/NSTEMI", theme.COLORS["danger"]),
        ("Reperfusion", theme.COLORS["success"]),
    ]


class STEMITimelineScene(TimelineScene):
    TITLE = "STEMI Door-to-Balloon"
    EVENTS = [
        ("0 min", "ECG"),
        ("30 min", "Cath lab"),
        ("90 min", "PCI"),
        ("24h", "DAPT"),
    ]


class PlaqueRuptureScene(FlowScene):
    TITLE = "Plaque Rupture Cascade"
    STEPS = [
        ("Plaque rupture", theme.COLORS["danger"]),
        ("Platelet plug", theme.COLORS["warning"]),
        ("Thrombus", theme.COLORS["danger"]),
        ("MI", theme.COLORS["navy"]),
    ]


class DAPTTimelineScene(TimelineScene):
    TITLE = "DAPT Timeline"
    EVENTS = [
        ("0 mo", "PCI"),
        ("1 mo", "DAPT"),
        ("6 mo", "De-escalate"),
        ("12 mo", "Stop"),
    ]


class AFManagementScene(FlowScene):
    TITLE = "Atrial Fibrillation Care"
    STEPS = [
        ("AF diagnosed", theme.COLORS["warning"]),
        ("CHA2DS2-VASc", theme.COLORS["blue"]),
        ("Anticoagulation", theme.COLORS["teal"]),
        ("Rate/Rhythm", theme.COLORS["success"]),
    ]


class RateRhythmComparisonScene(ComparisonScene):
    TITLE = "Rate vs Rhythm Control"
    LEFT_LABEL = "Rate control"
    RIGHT_LABEL = "Rhythm control"
    LEFT_VALUE = "HR <110"
    RIGHT_VALUE = "Sinus rhythm"
    METRIC = "Symptom relief + stroke prevention"


class ConductionSystemScene(Scene):
    def construct(self) -> None:
        title = Text(
            "Cardiac Conduction",
            font=theme.PRIMARY_FONT,
            font_size=theme.FONT_SIZES["title"],
            color=theme.COLORS["navy"],
        ).to_edge(UP)

        chambers = heart_chambers().next_to(title, DOWN, buff=0.8)

        sa_node = Dot(chambers.get_corner(UP + LEFT) + RIGHT * 0.8 + DOWN * 0.2, color=theme.COLORS["danger"])
        av_node = Dot(chambers.get_center() + DOWN * 0.1, color=theme.COLORS["danger"])
        his = Dot(chambers.get_center() + DOWN * 0.8, color=theme.COLORS["danger"])

        labels = VGroup(
            Text("SA", font=theme.PRIMARY_FONT, font_size=theme.FONT_SIZES["small"], color=theme.COLORS["text"]).next_to(sa_node, RIGHT, buff=0.2),
            Text("AV", font=theme.PRIMARY_FONT, font_size=theme.FONT_SIZES["small"], color=theme.COLORS["text"]).next_to(av_node, RIGHT, buff=0.2),
            Text("His", font=theme.PRIMARY_FONT, font_size=theme.FONT_SIZES["small"], color=theme.COLORS["text"]).next_to(his, RIGHT, buff=0.2),
        )

        self.play(FadeIn(title))
        self.play(Create(chambers))
        self.play(FadeIn(sa_node), FadeIn(av_node), FadeIn(his))
        self.play(FadeIn(labels))
        self.wait(0.5)


class HeartChambersScene(AnatomyChambersScene):
    TITLE = "Heart Chambers"


class TroponinKineticsScene(LineScene):
    TITLE = "Troponin Kinetics"
    POINTS = [(0, 0.1), (1, 0.3), (2, 0.6), (3, 0.85), (4, 0.7), (5, 0.5)]
    X_LABEL = "Hours"
    Y_LABEL = "Relative level"


class EchoViewsScene(PanelGridScene):
    TITLE = "Echo Views Overview"
    LABELS = ["PLAX", "PSAX", "A4C", "A2C"]


class CTAWorkupScene(FlowScene):
    TITLE = "Chest Pain CTA Pathway"
    STEPS = [
        ("Chest pain", theme.COLORS["warning"]),
        ("Risk score", theme.COLORS["blue"]),
        ("CTA", theme.COLORS["teal"]),
        ("Rule-out CAD", theme.COLORS["success"]),
    ]


class StressTestFlowScene(FlowScene):
    TITLE = "Stress Test Workflow"
    STEPS = [
        ("Symptoms", theme.COLORS["warning"]),
        ("Baseline ECG", theme.COLORS["blue"]),
        ("Stress test", theme.COLORS["teal"]),
        ("Ischemia?", theme.COLORS["danger"]),
    ]


class ARRRRScene(ComparisonScene):
    TITLE = "ARR vs RRR"
    LEFT_LABEL = "Control risk"
    RIGHT_LABEL = "Treatment risk"
    LEFT_VALUE = "20%"
    RIGHT_VALUE = "12%"
    METRIC = "ARR 8% | RRR 40%"


class NNTExplainerScene(BarScene):
    TITLE = "Number Needed to Treat"
    BARS = [
        ("NNT 12", 12, theme.COLORS["success"]),
        ("NNT 18", 18, theme.COLORS["teal"]),
        ("NNT 25", 25, theme.COLORS["neutral"]),
    ]
    FOOTNOTE = "Lower NNT is better"


class ForestPlotSummaryScene(ForestPlotScene):
    TITLE = "Forest Plot Summary"
    STUDIES = [
        ("Trial A", 0.82, 0.70, 0.97),
        ("Trial B", 0.76, 0.62, 0.92),
        ("Trial C", 0.88, 0.74, 1.02),
        ("Pooled", 0.81, 0.70, 0.93),
    ]


class EventsPer1000Scene(BarScene):
    TITLE = "Events per 1000"
    BARS = [
        ("Control", 120, theme.COLORS["danger"]),
        ("Treatment", 90, theme.COLORS["success"]),
    ]
    FOOTNOTE = "Lower events with treatment"


class ICDDecisionScene(FlowScene):
    TITLE = "ICD Decision Path"
    STEPS = [
        ("LVEF <=35%", theme.COLORS["warning"]),
        ("NYHA II-III", theme.COLORS["blue"]),
        ("Optimal GDMT", theme.COLORS["teal"]),
        ("ICD", theme.COLORS["success"]),
    ]


class CRTSelectionScene(FlowScene):
    TITLE = "CRT Selection"
    STEPS = [
        ("LBBB", theme.COLORS["warning"]),
        ("QRS >=150", theme.COLORS["blue"]),
        ("LVEF <=35%", theme.COLORS["teal"]),
        ("CRT", theme.COLORS["success"]),
    ]


class TAVRPathwayScene(FlowScene):
    TITLE = "TAVR Pathway"
    STEPS = [
        ("Severe AS", theme.COLORS["warning"]),
        ("Heart team", theme.COLORS["blue"]),
        ("TAVR", theme.COLORS["teal"]),
        ("Follow-up", theme.COLORS["success"]),
    ]


class LVADBridgeScene(TimelineScene):
    TITLE = "LVAD Bridge Timeline"
    EVENTS = [
        ("0 mo", "Advanced HF"),
        ("1 mo", "LVAD"),
        ("6 mo", "Bridge"),
        ("12 mo", "Transplant"),
    ]


def _ecg_wave(points: List, color: str) -> VMobject:
    wave = VMobject(color=color, stroke_width=4)
    wave.set_points_as_corners(points)
    return wave
