"""Decode screen - Main functional screen for hex decoding.

This screen provides a side-by-side interface where users can paste
hex-encoded text and see the decoded output.
"""
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button, Static, TextArea
from textual.binding import Binding

from decoder import decode_text
from history import add_to_history
from ui.formatters import format_text_with_highlights


class DecodeScreen(Screen):
    """Decode screen with split input/output panels."""
    
    CSS = """
    DecodeScreen {
        layout: horizontal;
    }
    
    /* LEFT PANEL - INPUT */
    #input-panel {
        width: 1fr;
        height: 100%;
        border: solid $primary;
        padding: 1;
    }
    
    /* RIGHT PANEL - OUTPUT */
    #output-panel {
        width: 1fr;
        height: 100%;
        border: solid $success;
        padding: 1;
    }
    
    /* Panel titles */
    .panel-title {
        text-align: center;
        text-style: bold;
        height: auto;
    }
    
    /* Toolbar section */
    #toolbar {
        height: auto;
        padding: 1;
        border-bottom: solid $primary;
    }
    
    #toolbar Button {
        margin: 0 1;
    }
    
    /* Input label */
    #input-label {
        text-align: center;
        height: auto;
        padding: 1;
        background: $primary-darken-3;
    }
    
    /* TEXT INPUT AREA - THIS MUST BE VISIBLE */
    #input-area {
        width: 100%;
        height: 1fr;
        min-height: 15;
        border: solid white;
        background: $surface;
    }
    
    /* Output content area */
    #output-scroll {
        height: 1fr;
    }
    
    #output-content {
        width: 100%;
        padding: 1;
    }
    """
    
    BINDINGS = [
        Binding("1", "update_preview", "Update Preview"),
        Binding("2", "save_history", "Save to History"),
        Binding("3", "back", "Back to Menu"),
        Binding("escape", "back", "Back to Menu"),
        Binding("ctrl+u", "update_preview", "Update Preview"),
        Binding("ctrl+s", "save_history", "Save to History"),
    ]
    
    def compose(self) -> ComposeResult:
        """Create the screen layout with input and output panels."""
        
        # ========== LEFT PANEL - INPUT ==========
        with Vertical(id="input-panel"):
            yield Static("[bold cyan]═══ INPUT ═══[/bold cyan]", classes="panel-title")
            
            # Toolbar with buttons
            with Horizontal(id="toolbar"):
                yield Button("[1] Update (Ctrl+U)", id="btn-update", variant="success")
                yield Button("[2] Save (Ctrl+S)", id="btn-save", variant="primary")
                yield Button("[3] Back (ESC)", id="btn-back", variant="default")
            
            # Input label
            yield Static("[bold yellow]PASTE YOUR HEX TEXT BELOW:[/bold yellow]", id="input-label")
            
            # TEXT INPUT FIELD
            yield TextArea(id="input-area")
        
        # ========== RIGHT PANEL - OUTPUT ==========
        with Vertical(id="output-panel"):
            yield Static("[bold green]═══ OUTPUT ═══[/bold green]", classes="panel-title")
            
            # Output display area (scrollable)
            with ScrollableContainer(id="output-scroll"):
                yield Static(
                    "[dim]Decoded text will appear here...\n\n"
                    "Paste hex-encoded text in the left panel,\n"
                    "then click 'Update' or press Ctrl+U[/dim]",
                    id="output-content"
                )
    
    def on_mount(self) -> None:
        """Called when screen is mounted - focus the input area."""
        input_area = self.query_one("#input-area", TextArea)
        input_area.focus()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button click events."""
        button_id = event.button.id
        
        if button_id == "btn-update":
            self.update_preview()
        elif button_id == "btn-save":
            self.save_to_history()
        elif button_id == "btn-back":
            self.action_back()
    
    def action_update_preview(self) -> None:
        """Keyboard shortcut: Ctrl+U - Update preview."""
        self.update_preview()
    
    def action_save_history(self) -> None:
        """Keyboard shortcut: Ctrl+S - Save to history."""
        self.save_to_history()
    
    def action_back(self) -> None:
        """Keyboard shortcut: ESC - Back to main menu."""
        self.app.pop_screen()
    
    def update_preview(self) -> None:
        """Process input text and display decoded output."""
        input_area = self.query_one("#input-area", TextArea)
        output_widget = self.query_one("#output-content", Static)
        
        text = input_area.text.strip()
        
        if not text:
            output_widget.update(
                "[dim]Decoded text will appear here...\n\n"
                "Paste hex-encoded text in the left panel,\n"
                "then click 'Update' or press Ctrl+U[/dim]"
            )
            return
        
        result = decode_text(text)
        
        if not result.replacements:
            output_widget.update(
                "[yellow]No hex sequences detected.[/yellow]\n\n"
                "[dim]Make sure your text contains hex byte sequences\n"
                "like: 48 65 6C 6C 6F (which decodes to 'Hello')[/dim]"
            )
            return
        
        # Format with highlights - pass ORIGINAL text, not decoded
        formatted = format_text_with_highlights(
            result.original,  # Use original text - positions refer to original
            result.replacements, 
            highlight_hex=False  # Show decoded portions in green
        )
        
        stats = (
            f"[bold cyan]╔══ DECODE RESULTS ══╗[/bold cyan]\n"
            f"[bold cyan]║[/bold cyan] Detections: {result.num_replacements}\n"
            f"[bold cyan]║[/bold cyan] Total bytes: {result.total_hex_bytes}\n"
            f"[bold cyan]╚════════════════════╝[/bold cyan]\n\n"
        )
        
        output_widget.update(stats + formatted)
    
    def save_to_history(self) -> None:
        """Save current decode result to history database."""
        input_area = self.query_one("#input-area", TextArea)
        output_widget = self.query_one("#output-content", Static)
        
        text = input_area.text.strip()
        
        if not text:
            output_widget.update(
                "[yellow]Nothing to save.[/yellow]\n\n"
                "[dim]Paste some text first, then save to history.[/dim]"
            )
            return
        
        result = decode_text(text)
        add_to_history(result.original, result.decoded, result.replacements)
        
        # Format with highlights - pass ORIGINAL text, not decoded
        formatted = format_text_with_highlights(
            result.original,  # Use original text - positions refer to original
            result.replacements, 
            highlight_hex=False  # Show decoded portions in green
        )
        
        stats = (
            f"[bold cyan]╔══ DECODE RESULTS ══╗[/bold cyan]\n"
            f"[bold cyan]║[/bold cyan] Detections: {result.num_replacements}\n"
            f"[bold cyan]║[/bold cyan] Total bytes: {result.total_hex_bytes}\n"
            f"[bold cyan]╚════════════════════╝[/bold cyan]\n\n"
        )
        
        success_msg = "\n\n[bold green]Saved to history![/bold green]"
        
        output_widget.update(stats + formatted + success_msg)
