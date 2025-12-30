"""Main menu screen."""
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen, ModalScreen
from textual.widgets import Button, Static
from textual.binding import Binding

from history import get_history_count
from ui.formatters import create_aligned_banner
from ui.constants import TALOS_TITLE_LINES
# Import screens here to avoid circular imports
# These will be imported when needed in the action methods


class MainMenuScreen(Screen):
    """Main menu screen."""
    
    CSS = """
    MainMenuScreen {
        align: center middle;
        layout: vertical;
    }
    
    .banner-container {
        width: 100%;
        height: auto;
        padding: 1;
        text-align: center;
        align: center middle;
        content-align: center middle;
    }
    
    Static {
        text-align: center;
    }
    
    .button-row {
        width: 100%;
        height: auto;
        align: center middle;
        padding: 2;
    }
    
    Button {
        margin: 1;
        min-width: 15;
    }
    """
    
    BINDINGS = [
        Binding("1", "decode", "Decode"),
        Binding("2", "history", "History"),
        Binding("3", "about", "About"),
        Binding("4", "quit", "Exit"),
        Binding("q", "quit", "Quit"),
    ]
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        history_count = get_history_count()
        
        # Create banner
        talos_banner = create_aligned_banner(
            title_lines=TALOS_TITLE_LINES,
            subtitle="Hex Byte Decoder & Text Converter\nFor The Talos Principle Game",
            width=75
        )
        
        with Container(classes="banner-container"):
            yield Static(talos_banner, classes="banner-container")
            if history_count > 0:
                yield Static(f"[cyan]You have {history_count} entry(ies) in your history![/cyan]", classes="banner-container")
        
        yield Static("[bold yellow]Select an option:[/bold yellow]", classes="banner-container")
        
        with Horizontal(classes="button-row"):
            yield Button("[1] Decode", id="decode", variant="primary")
            yield Button("[2] History", id="history", variant="primary")
            yield Button("[3] About", id="about", variant="primary")
            yield Button("[4] Exit", id="exit", variant="error")
        
        yield Static("[dim]Use numbers or click buttons to navigate[/dim]", classes="banner-container")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "decode":
            self.action_decode()
        elif event.button.id == "history":
            self.action_history()
        elif event.button.id == "about":
            self.action_about()
        elif event.button.id == "exit":
            self.action_quit()
    
    def action_decode(self) -> None:
        """Open decode screen."""
        import os
        import sys
        # Force reload by importing directly from file path
        decode_screen_path = os.path.join(os.path.dirname(__file__), "decode_screen.py")
        if os.path.exists(decode_screen_path):
            # Clear any cached imports
            if 'ui.decode_screen' in sys.modules:
                del sys.modules['ui.decode_screen']
        from ui.decode_screen import DecodeScreen
        self.app.push_screen(DecodeScreen())
    
    def action_history(self) -> None:
        """Open history screen."""
        from ui.history_screen import HistoryScreen
        self.app.push_screen(HistoryScreen())
    
    def action_about(self) -> None:
        """Open about screen."""
        from ui.about_screen import AboutScreen
        self.app.push_screen(AboutScreen())
    
    def action_quit(self) -> None:
        """Show quit confirmation dialog."""
        self.app.push_screen(QuitConfirmScreen())


class QuitConfirmScreen(ModalScreen):
    """Confirmation dialog for quitting the application."""
    
    CSS = """
    QuitConfirmScreen {
        align: center middle;
    }
    
    .dialog-container {
        width: 50;
        height: auto;
        border: solid $primary;
        padding: 1;
        background: $surface;
    }
    
    .message {
        padding: 1;
        text-align: center;
    }
    
    .button-container {
        height: auto;
        padding: 1;
        align: center middle;
    }
    
    .button-container Button {
        margin: 0 1;
    }
    """
    
    BINDINGS = [
        Binding("y", "confirm_quit", "Yes"),
        Binding("n", "cancel", "No"),
        Binding("escape", "cancel", "Cancel"),
    ]
    
    def compose(self) -> ComposeResult:
        """Create confirmation dialog."""
        with Vertical(classes="dialog-container"):
            yield Static("[bold]Are you sure you want to exit?[/bold]", classes="message")
            with Container(classes="button-container"):
                yield Button("[Y] Yes", id="yes", variant="error")
                yield Button("[N] No", id="no", variant="default")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "yes":
            self.action_confirm_quit()
        elif event.button.id == "no":
            self.action_cancel()
    
    def action_confirm_quit(self) -> None:
        """Confirm and quit the application."""
        self.app.exit()
    
    def action_cancel(self) -> None:
        """Cancel and return to main menu."""
        self.app.pop_screen()

