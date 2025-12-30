"""About screen displaying README content."""
import os
from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Static, Markdown
from textual.binding import Binding


class AboutScreen(Screen):
    """About screen displaying README content with proper markdown rendering."""
    
    CSS = """
    AboutScreen {
        layout: vertical;
    }
    
    #header {
        height: auto;
        padding: 1;
        text-align: center;
        text-style: bold;
        background: $primary-darken-3;
    }
    
    #content-scroll {
        height: 1fr;
        border: solid $primary;
        padding: 1;
    }
    
    #footer {
        height: auto;
        padding: 1;
        align: center middle;
    }
    
    Markdown {
        padding: 1;
    }
    """
    
    BINDINGS = [
        Binding("1", "back", "Back"),
        Binding("escape", "back", "Back"),
    ]
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        # Header
        yield Static("[bold cyan]═══ ABOUT TALOS DECODER ═══[/bold cyan]", id="header")
        
        # Scrollable content area with rendered markdown
        with VerticalScroll(id="content-scroll"):
            readme_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "README.md")
            
            try:
                with open(readme_path, 'r', encoding='utf-8') as f:
                    readme_content = f.read()
            except IOError:
                readme_content = "# Error\n\nCould not load README.md file."
            
            yield Markdown(readme_content)
        
        # Footer with back button
        with Vertical(id="footer"):
            yield Button("[1] Back to Menu (ESC)", id="back", variant="primary")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "back":
            self.action_back()
    
    def action_back(self) -> None:
        """Go back to main menu."""
        self.app.pop_screen()

