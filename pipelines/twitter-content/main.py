#!/usr/bin/env python3
"""
Twitter Content System - CLI Interface

A content generation system for cardiology thought leadership.
Harvests ideas from medical Twitter, researches using PubMed + AstraDB RAG,
and generates publication-ready content in Eric Topol + Peter Attia style.

Usage:
    python main.py harvest              # Harvest from Twitter and generate
    python main.py direct "question"    # Generate from direct question
    python main.py direct "question" --format thread
"""

import asyncio
import sys
from datetime import datetime
from typing import Optional

try:
    import typer
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.table import Table
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    print("Note: Install 'rich' and 'typer' for better CLI experience")

from src.config import config
from src.pipeline import ContentPipeline, create_pipeline
from src.writer import ContentFormat


# CLI app
if HAS_RICH:
    app = typer.Typer(help="Twitter Content System for Cardiology Thought Leadership")
    console = Console()


def validate_config():
    """Validate configuration before running."""
    issues = config.validate()
    if issues:
        print("\n⚠️  Configuration Issues:")
        for issue in issues:
            print(f"   - {issue}")
        print("\nPlease check your .env file and try again.")
        print("See .env.example for required variables.")
        return False
    return True


def print_content(content, format_type: str):
    """Print generated content with formatting."""
    if HAS_RICH:
        console.print("\n")
        console.print(Panel(
            Markdown(content.content),
            title=f"[bold green]Generated {format_type.upper()}[/bold green]",
            subtitle=f"Words: {content.word_count} | Chars: {content.char_count}",
        ))
    else:
        print("\n" + "="*60)
        print(f"GENERATED {format_type.upper()}")
        print("="*60)
        print(content.content)
        print(f"\n[Words: {content.word_count} | Chars: {content.char_count}]")


def print_results_summary(results):
    """Print summary of all results."""
    if not results:
        print("\nNo results generated.")
        return

    if HAS_RICH:
        table = Table(title="Generated Content Summary")
        table.add_column("Idea", style="cyan")
        table.add_column("Format", style="green")
        table.add_column("Words", justify="right")
        table.add_column("Sources", justify="right")

        for r in results:
            table.add_row(
                r.idea.research_question[:40] + "...",
                r.content.format.value,
                str(r.content.word_count),
                str(r.research.total_sources),
            )

        console.print("\n")
        console.print(table)
    else:
        print("\n" + "="*60)
        print("RESULTS SUMMARY")
        print("="*60)
        for i, r in enumerate(results, 1):
            print(f"\n{i}. {r.idea.research_question[:50]}...")
            print(f"   Format: {r.content.format.value}")
            print(f"   Words: {r.content.word_count}")
            print(f"   Sources: {r.research.total_sources}")


async def run_harvest(max_ideas: int = 3, format: Optional[str] = None):
    """Run the harvest pipeline."""
    pipeline = create_pipeline()
    content_format = ContentFormat(format) if format else None

    results = await pipeline.harvest_and_process(
        max_ideas=max_ideas,
        format=content_format,
    )

    for result in results:
        print_content(result.content, result.content.format.value)

        # Save to file
        filename = f"output/content_{result.idea.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            import os
            os.makedirs("output", exist_ok=True)
            result.save_to_file(filename)
            print(f"\n📁 Saved to {filename}")
        except Exception as e:
            print(f"\nCould not save to file: {e}")

    print_results_summary(results)
    return results


async def run_direct(question: str, format: Optional[str] = None):
    """Run the direct question pipeline."""
    pipeline = create_pipeline()
    content_format = ContentFormat(format) if format else None

    result = await pipeline.process_direct_question(question, content_format)

    if result:
        print_content(result.content, result.content.format.value)

        # Print research summary
        if HAS_RICH:
            console.print("\n[bold]Research Sources:[/bold]")
            console.print(f"  PubMed: {len(result.research.pubmed_articles)} articles")
            console.print(f"  Guidelines/Textbooks: {len(result.research.rag_results)} chunks")
            console.print(f"\n[bold]Citations:[/bold]")
            for cite in result.brief.citations[:5]:
                console.print(f"  • {cite}")
        else:
            print("\n📚 Research Sources:")
            print(f"   PubMed: {len(result.research.pubmed_articles)} articles")
            print(f"   Guidelines/Textbooks: {len(result.research.rag_results)} chunks")

        # Save to file
        filename = f"output/content_direct_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            import os
            os.makedirs("output", exist_ok=True)
            result.save_to_file(filename)
            print(f"\n📁 Saved to {filename}")
        except Exception as e:
            print(f"\nCould not save to file: {e}")

    return result


if HAS_RICH:
    @app.command()
    def harvest(
        max_ideas: int = typer.Option(3, "--max", "-m", help="Maximum ideas to process"),
        format: Optional[str] = typer.Option(None, "--format", "-f", help="Output format: tweet, thread, long_post"),
    ):
        """Harvest ideas from medical Twitter and generate content."""
        console.print("\n🐦 [bold]Twitter Content System[/bold]")
        console.print("Harvesting ideas from medical influencers...\n")

        if not validate_config():
            raise typer.Exit(1)

        asyncio.run(run_harvest(max_ideas, format))

    @app.command()
    def direct(
        question: str = typer.Argument(..., help="Research question to explore"),
        format: Optional[str] = typer.Option(None, "--format", "-f", help="Output format: tweet, thread, long_post"),
    ):
        """Generate content from a direct question."""
        console.print("\n🐦 [bold]Twitter Content System[/bold]")
        console.print(f"Processing: {question[:60]}...\n")

        if not validate_config():
            raise typer.Exit(1)

        asyncio.run(run_direct(question, format))

    @app.command()
    def config_check():
        """Check configuration status."""
        console.print("\n🔧 [bold]Configuration Check[/bold]\n")

        issues = config.validate()
        if issues:
            console.print("[red]Issues found:[/red]")
            for issue in issues:
                console.print(f"  ❌ {issue}")
            console.print("\n[yellow]Please check your .env file[/yellow]")
        else:
            console.print("[green]✓ All required configuration present[/green]")

            # Show active settings
            table = Table(title="Active Configuration")
            table.add_column("Setting", style="cyan")
            table.add_column("Value", style="green")

            table.add_row("LLM Provider", "OpenRouter" if config.llm.openrouter_api_key else "Anthropic")
            table.add_row("LLM Model", config.llm.openrouter_model if config.llm.openrouter_api_key else config.llm.anthropic_model)
            table.add_row("Embedding Model", config.openai.embedding_model)
            table.add_row("AstraDB Collection", config.astradb.collection_name)
            table.add_row("Inspiration Accounts", str(len(config.apify.max_tweets_per_account)))

            console.print(table)


def main_simple():
    """Simple main function for when rich/typer not available."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main.py harvest              # Harvest from Twitter")
        print("  python main.py direct 'question'    # Direct question")
        print("  python main.py config               # Check configuration")
        sys.exit(1)

    command = sys.argv[1]

    if not validate_config():
        sys.exit(1)

    if command == "harvest":
        max_ideas = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        asyncio.run(run_harvest(max_ideas))

    elif command == "direct":
        if len(sys.argv) < 3:
            print("Error: Please provide a question")
            sys.exit(1)
        question = sys.argv[2]
        format = sys.argv[3] if len(sys.argv) > 3 else None
        asyncio.run(run_direct(question, format))

    elif command == "config":
        issues = config.validate()
        if issues:
            print("Configuration issues:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("✓ Configuration OK")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    if HAS_RICH:
        app()
    else:
        main_simple()
