#!/usr/bin/env python3
"""
Plotly Medical Chart Templates

Pre-built templates for common medical/cardiology data visualizations.
Generates interactive HTML and static PNG exports.

Usage:
    python plotly_charts.py bar --data trial_data.csv --output results.html
    python plotly_charts.py forest --data meta_analysis.csv --output forest.png
"""

import argparse
import sys
from typing import Optional, List, Dict, Any

try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import pandas as pd
except ImportError:
    print("❌ Install dependencies:")
    print("   pip install plotly pandas kaleido --break-system-packages")
    sys.exit(1)


# Medical color palette
MEDICAL_COLORS = {
    'primary': '#1e3a5f',      # Deep navy
    'secondary': '#2d6a9f',    # Medical blue
    'accent': '#48a9a6',       # Teal
    'success': '#4caf50',      # Green
    'warning': '#ff9800',      # Orange
    'danger': '#f44336',       # Red
    'neutral': '#607d8b',      # Blue-gray
    'light': '#ecf0f1',        # Light gray
    'background': '#ffffff',   # White
}

MEDICAL_PALETTE = ['#1e3a5f', '#2d6a9f', '#48a9a6', '#5bc0be', '#3d5a80', '#293241']


def apply_medical_theme(fig: go.Figure, title: str = "") -> go.Figure:
    """Apply consistent medical styling to any Plotly figure."""
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=18, color=MEDICAL_COLORS['primary']),
            x=0.5,
            xanchor='center'
        ),
        font=dict(family="Arial, sans-serif", size=12, color='#333'),
        plot_bgcolor=MEDICAL_COLORS['background'],
        paper_bgcolor=MEDICAL_COLORS['background'],
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=60, r=40, t=80, b=60)
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#eee')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#eee')
    return fig


def create_bar_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str = "Clinical Outcomes",
    color: Optional[str] = None,
    orientation: str = "v"
) -> go.Figure:
    """Create a bar chart for trial results or comparisons."""
    fig = px.bar(
        data,
        x=x if orientation == "v" else y,
        y=y if orientation == "v" else x,
        color=color,
        orientation=orientation,
        color_discrete_sequence=MEDICAL_PALETTE,
        text=y if orientation == "v" else x
    )
    fig.update_traces(textposition='outside')
    return apply_medical_theme(fig, title)


def create_forest_plot(
    studies: List[str],
    estimates: List[float],
    lower_ci: List[float],
    upper_ci: List[float],
    title: str = "Forest Plot: Hazard Ratios",
    null_value: float = 1.0
) -> go.Figure:
    """Create a forest plot for meta-analysis visualization."""
    fig = go.Figure()
    
    # Add confidence intervals (horizontal lines)
    for i, (study, est, low, high) in enumerate(zip(studies, estimates, lower_ci, upper_ci)):
        fig.add_trace(go.Scatter(
            x=[low, high],
            y=[study, study],
            mode='lines',
            line=dict(color=MEDICAL_COLORS['neutral'], width=2),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Add point estimates
    fig.add_trace(go.Scatter(
        x=estimates,
        y=studies,
        mode='markers',
        marker=dict(
            size=12,
            color=MEDICAL_COLORS['primary'],
            symbol='diamond'
        ),
        name='Point Estimate',
        hovertemplate='%{y}<br>HR: %{x:.2f}<extra></extra>'
    ))
    
    # Add null line
    fig.add_vline(
        x=null_value,
        line_dash="dash",
        line_color=MEDICAL_COLORS['danger'],
        annotation_text=f"Null ({null_value})"
    )
    
    fig.update_layout(
        xaxis_title="Hazard Ratio (95% CI)",
        yaxis_title="",
        xaxis=dict(type='log' if null_value == 1.0 else 'linear')
    )
    
    return apply_medical_theme(fig, title)


def create_survival_curve(
    time_data: List[List[float]],
    survival_data: List[List[float]],
    group_names: List[str],
    title: str = "Kaplan-Meier Survival Curve",
    xlabel: str = "Time (months)",
    ylabel: str = "Survival Probability"
) -> go.Figure:
    """Create Kaplan-Meier style survival curves."""
    fig = go.Figure()
    
    for i, (times, survival, name) in enumerate(zip(time_data, survival_data, group_names)):
        fig.add_trace(go.Scatter(
            x=times,
            y=survival,
            mode='lines',
            name=name,
            line=dict(color=MEDICAL_PALETTE[i % len(MEDICAL_PALETTE)], width=2, shape='hv')
        ))
    
    fig.update_layout(
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        yaxis=dict(range=[0, 1.05])
    )
    
    return apply_medical_theme(fig, title)


def create_trend_line(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str = "Trend Over Time",
    color: Optional[str] = None
) -> go.Figure:
    """Create a line chart for trends over time."""
    fig = px.line(
        data,
        x=x,
        y=y,
        color=color,
        color_discrete_sequence=MEDICAL_PALETTE,
        markers=True
    )
    fig.update_xaxes(rangeslider_visible=True)
    return apply_medical_theme(fig, title)


def create_comparison_bars(
    categories: List[str],
    group1_values: List[float],
    group2_values: List[float],
    group1_name: str = "Treatment",
    group2_name: str = "Control",
    title: str = "Treatment vs Control Comparison"
) -> go.Figure:
    """Create grouped bar chart for treatment comparisons."""
    fig = go.Figure(data=[
        go.Bar(
            name=group1_name,
            x=categories,
            y=group1_values,
            marker_color=MEDICAL_COLORS['secondary']
        ),
        go.Bar(
            name=group2_name,
            x=categories,
            y=group2_values,
            marker_color=MEDICAL_COLORS['neutral']
        )
    ])
    fig.update_layout(barmode='group')
    return apply_medical_theme(fig, title)


def create_pie_chart(
    labels: List[str],
    values: List[float],
    title: str = "Distribution"
) -> go.Figure:
    """Create a pie/donut chart for proportions."""
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=MEDICAL_PALETTE)
    )])
    return apply_medical_theme(fig, title)


def create_heatmap(
    data: pd.DataFrame,
    title: str = "Correlation Matrix"
) -> go.Figure:
    """Create a heatmap for correlation or matrix data."""
    fig = px.imshow(
        data,
        text_auto=True,
        color_continuous_scale='RdBu_r',
        aspect='auto'
    )
    return apply_medical_theme(fig, title)


def create_dashboard(
    charts: List[go.Figure],
    titles: List[str],
    rows: int = 2,
    cols: int = 2
) -> go.Figure:
    """Combine multiple charts into a dashboard layout."""
    fig = make_subplots(
        rows=rows,
        cols=cols,
        subplot_titles=titles
    )
    
    for i, chart in enumerate(charts):
        row = (i // cols) + 1
        col = (i % cols) + 1
        for trace in chart.data:
            fig.add_trace(trace, row=row, col=col)
    
    fig.update_layout(height=800, showlegend=True)
    return apply_medical_theme(fig, "Clinical Dashboard")


def save_chart(fig: go.Figure, output_path: str):
    """Save chart as HTML or image."""
    if output_path.endswith('.html'):
        fig.write_html(output_path, include_plotlyjs='cdn')
        print(f"✅ Saved interactive chart: {output_path}")
    elif output_path.endswith(('.png', '.jpg', '.jpeg', '.pdf', '.svg')):
        try:
            fig.write_image(output_path, scale=2)
            print(f"✅ Saved static image: {output_path}")
        except Exception as e:
            print(f"⚠️  Image export failed: {e}")
            print("   Install kaleido: pip install kaleido --break-system-packages")
            # Fallback to HTML
            html_path = output_path.rsplit('.', 1)[0] + '.html'
            fig.write_html(html_path)
            print(f"   Saved as HTML instead: {html_path}")
    else:
        # Default to HTML
        fig.write_html(output_path + '.html')
        print(f"✅ Saved: {output_path}.html")


# Quick demo functions
def demo_trial_results():
    """Demo: Clinical trial results bar chart."""
    data = pd.DataFrame({
        'Outcome': ['Primary Endpoint', 'Secondary Endpoint', 'Safety Event'],
        'Treatment': [12.3, 8.5, 3.2],
        'Placebo': [18.7, 14.2, 2.8]
    })
    
    fig = go.Figure(data=[
        go.Bar(name='Treatment', x=data['Outcome'], y=data['Treatment'], 
               marker_color=MEDICAL_COLORS['secondary']),
        go.Bar(name='Placebo', x=data['Outcome'], y=data['Placebo'],
               marker_color=MEDICAL_COLORS['neutral'])
    ])
    fig.update_layout(barmode='group', yaxis_title='Event Rate (%)')
    return apply_medical_theme(fig, 'Clinical Trial Results')


def demo_forest_plot():
    """Demo: Forest plot for meta-analysis."""
    return create_forest_plot(
        studies=['PARADIGM-HF', 'DAPA-HF', 'EMPEROR-Reduced', 'VICTORIA', 'GALACTIC-HF'],
        estimates=[0.80, 0.74, 0.75, 0.90, 0.92],
        lower_ci=[0.73, 0.65, 0.65, 0.82, 0.86],
        upper_ci=[0.87, 0.85, 0.86, 0.98, 0.99],
        title='Heart Failure Trials: Hazard Ratios for Primary Endpoint'
    )


def demo_trends():
    """Demo: Mortality trends over time."""
    data = pd.DataFrame({
        'Year': list(range(2000, 2024)),
        'Mortality': [30, 28, 27, 25, 24, 23, 21, 20, 19, 18, 
                      17, 16, 15, 14, 13, 12, 11, 10, 10, 9, 
                      8, 8, 7, 7]
    })
    return create_trend_line(data, 'Year', 'Mortality', 
                            'Heart Failure In-Hospital Mortality Trends (%)')


def main():
    parser = argparse.ArgumentParser(description="Generate medical charts with Plotly")
    parser.add_argument("chart_type", choices=['bar', 'forest', 'survival', 'trend', 
                                                'comparison', 'pie', 'heatmap', 'demo'],
                        help="Type of chart to create")
    parser.add_argument("--data", "-d", help="CSV file with data")
    parser.add_argument("--output", "-o", default="chart.html", help="Output file")
    parser.add_argument("--title", "-t", default="", help="Chart title")
    parser.add_argument("--x", help="X-axis column name")
    parser.add_argument("--y", help="Y-axis column name")
    parser.add_argument("--color", "-c", help="Color grouping column")
    
    args = parser.parse_args()
    
    if args.chart_type == 'demo':
        print("📊 Generating demo charts...")
        save_chart(demo_trial_results(), 'demo_trial_results.html')
        save_chart(demo_forest_plot(), 'demo_forest_plot.html')
        save_chart(demo_trends(), 'demo_trends.html')
        print("✅ Demo charts created!")
        return
    
    # Load data if provided
    if args.data:
        try:
            data = pd.read_csv(args.data)
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            sys.exit(1)
    else:
        print("❌ Provide --data CSV file for chart generation")
        print("   Or use 'demo' to see example charts")
        sys.exit(1)
    
    # Generate chart
    if args.chart_type == 'bar':
        fig = create_bar_chart(data, args.x or data.columns[0], 
                               args.y or data.columns[1], args.title, args.color)
    elif args.chart_type == 'trend':
        fig = create_trend_line(data, args.x or data.columns[0],
                                args.y or data.columns[1], args.title, args.color)
    elif args.chart_type == 'pie':
        fig = create_pie_chart(data[data.columns[0]].tolist(),
                               data[data.columns[1]].tolist(), args.title)
    elif args.chart_type == 'heatmap':
        fig = create_heatmap(data, args.title)
    else:
        print(f"⚠️  {args.chart_type} requires manual configuration. See script for API.")
        sys.exit(1)
    
    save_chart(fig, args.output)


if __name__ == "__main__":
    main()
