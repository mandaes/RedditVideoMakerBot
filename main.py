#!/usr/bin/env python3
"""RedditVideoMakerBot - Main entry point.

This bot automatically creates videos from Reddit posts by combining
text-to-speech narration with background footage.
"""

import sys
import os
from pathlib import Path

# Ensure we're running from the project root
if not Path("config.toml").exists() and not Path("config.toml.template").exists():
    print("[ERROR] Please run this script from the project root directory.")
    sys.exit(1)


def check_dependencies():
    """Check that all required dependencies are installed."""
    required = [
        "praw",
        "moviepy",
        "requests",
        "toml",
        "rich",
    ]
    missing = []
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"[ERROR] Missing required packages: {', '.join(missing)}")
        print("Please run: pip install -r requirements.txt")
        sys.exit(1)


def check_config():
    """Verify that the config file exists and is properly configured."""
    config_path = Path("config.toml")
    if not config_path.exists():
        template_path = Path("config.toml.template")
        if template_path.exists():
            print(
                "[ERROR] config.toml not found. "
                "Please copy config.toml.template to config.toml and fill in your credentials."
            )
        else:
            print("[ERROR] config.toml not found. Please create a config.toml file.")
        sys.exit(1)


def main():
    """Main entry point for RedditVideoMakerBot."""
    print("Starting RedditVideoMakerBot...")

    # Pre-flight checks
    check_dependencies()
    check_config()

    # Late imports after dependency check
    import toml
    from rich.console import Console
    from rich.traceback import install as install_rich_traceback

    # Install rich traceback handler for better error output
    install_rich_traceback()
    console = Console()

    # Load configuration
    try:
        config = toml.load("config.toml")
    except toml.TomlDecodeError as e:
        console.print(f"[bold red][ERROR] Failed to parse config.toml:[/bold red] {e}")
        sys.exit(1)

    console.print("[bold green]RedditVideoMakerBot[/bold green] \u2014 Starting up")
    console.print(f"Python version: {sys.version}")

    # Ensure output directories exist
    Path("assets/temp").mkdir(parents=True, exist_ok=True)
    Path("results").mkdir(parents=True, exist_ok=True)

    # Import and run the video creation pipeline
    try:
        from video_creation.main import make_final_video
        from reddit.subreddit import get_subreddit_threads

        console.print("[cyan]Fetching Reddit posts...[/cyan]")
        reddit_thread, reddit_comments = get_subreddit_threads(config)

        console.print("[cyan]Creating video...[/cyan]")
        make_final_video(reddit_thread, reddit_comments, config)

        # Print the output path so it's easy to find the finished video
        results_dir = Path("results").resolve()
        console.print(f"[bold green]Done![/bold green] Output saved to: {results_dir}")

    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user. Exiting.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold red][ERROR] An unexpected error occurred:[/bold red] {e}")
        raise


if __name__ == "__main__":
    main()
