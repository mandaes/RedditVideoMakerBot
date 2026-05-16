"""Console utility functions for styled terminal output."""

from rich.console import Console
from rich.theme import Theme
from rich.traceback import install

# Install rich traceback handler for better error display
install()

# Define custom theme for consistent styling
custom_theme = Theme(
    {
        "info": "bold cyan",
        "warning": "bold yellow",
        "error": "bold red",
        "success": "bold green",
        "highlight": "bold magenta",
    }
)

console = Console(theme=custom_theme)


def print_step(step: str) -> None:
    """Print a step message with consistent styling.

    Args:
        step: The step message to display.
    """
    console.print(f"[info]\u27a4 {step}[/info]")


def print_substep(substep: str, style: str = "cyan") -> None:
    """Print a sub-step message with consistent styling.

    Args:
        substep: The sub-step message to display.
        style: Optional rich style string to apply. Defaults to 'cyan' for
               better readability against dark terminal backgrounds.
    """
    console.print(f"  [dim]\u2022[/dim] [{style}]{substep}[/{style}]")


def print_success(message: str) -> None:
    """Print a success message.

    Args:
        message: The success message to display.
    """
    console.print(f"[success]\u2714 {message}[/success]")


def print_warning(message: str) -> None:
    """Print a warning message.

    Args:
        message: The warning message to display.
    """
    console.print(f"[warning]\u26a0 WARNING: {message}[/warning]")


def print_error(message: str) -> None:
    """Print an error message.

    Args:
        message: The error message to display.
    """
    console.print(f"[error]\u2718 ERROR: {message}[/error]")


def print_markdown(markdown_text: str) -> None:
    """Render and print markdown-formatted text to the console.

    Args:
        markdown_text: The markdown text to render.
    """
    from rich.markdown import Markdown

    md = Markdown(markdown_text)
    console.print(md)


def print_table(title: str, data: dict) -> None:
    """Print a formatted table with a title and key-value data.

    Args:
        title: The title of the table.
        data: A dictionary of key-value pairs to display.
    """
    from rich.table import Table

    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("Setting", style="cyan", no_wrap=True)
    table.add_column("Value", style="white")

    for key, value in data.items():
        table.add_row(str(key), str(value))

    console.print(table)
