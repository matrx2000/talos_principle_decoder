"""History browser screens."""
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.screen import Screen, ModalScreen
from textual.widgets import Button, Static, DataTable
from textual.binding import Binding

from history import load_history, delete_history_entry
from ui.formatters import format_timestamp, format_text_with_highlights, format_decoded_text_with_highlights
from models import Replacement


class HistoryScreen(Screen):
    """History browser screen."""
    
    CSS = """
    HistoryScreen {
        layout: vertical;
    }
    
    DataTable {
        height: 1fr;
    }
    
    .banner-container {
        width: 100%;
        height: auto;
        padding: 1;
        text-align: center;
        align: center middle;
    }
    
    .button-container {
        align: center middle;
        padding: 1;
    }
    """
    
    BINDINGS = [
        Binding("1", "view_details", "View Details"),
        Binding("2", "back", "Back"),
        Binding("escape", "back", "Back"),
    ]
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        history = load_history()
        
        if not history:
            yield Static(
                "[dim]No history entries found. Start decoding some text to build your history![/dim]",
                classes="banner-container"
            )
            with Container(classes="button-container"):
                yield Button("Back", id="back", variant="default")
            return
        
        # Sort by timestamp, newest first
        history.sort(key=lambda x: x.timestamp, reverse=True)
        
        yield Static("[bold]DECODING HISTORY[/bold]", classes="banner-container")
        
        table = DataTable(id="history-table")
        table.add_columns("Time", "Original Preview", "Decoded Preview", "Detections")
        
        for entry in history[:50]:  # Show first 50
            formatted_time = format_timestamp(entry.timestamp)
            original_preview = entry.original[:40] + "..." if len(entry.original) > 40 else entry.original
            decoded_preview = entry.decoded[:40] + "..." if len(entry.decoded) > 40 else entry.decoded
            table.add_row(
                formatted_time,
                original_preview,
                decoded_preview,
                str(entry.num_replacements),
                key=str(entry.timestamp)
            )
        
        yield table
        
        with Container(classes="button-container"):
            yield Button("[1] View Details", id="view", variant="primary")
            yield Button("Delete Entry", id="delete", variant="error")
            yield Button("[2] Back", id="back", variant="default")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "view":
            self.view_details()
        elif event.button.id == "delete":
            self.delete_entry()
        elif event.button.id == "back":
            self.action_back()
    
    def view_details(self) -> None:
        """View selected entry details."""
        table = self.query_one("#history-table", DataTable)
        if table.cursor_row is not None:
            # Get the selected entry
            history = load_history()
            history.sort(key=lambda x: x.timestamp, reverse=True)
            if table.cursor_row < len(history):
                entry = history[table.cursor_row]
                self.app.push_screen(HistoryDetailScreen(entry))
    
    def action_view_details(self) -> None:
        """Keyboard shortcut: 1 - View details."""
        self.view_details()
    
    def delete_entry(self) -> None:
        """Show delete confirmation dialog."""
        table = self.query_one("#history-table", DataTable)
        if table.cursor_row is not None:
            history = load_history()
            history.sort(key=lambda x: x.timestamp, reverse=True)
            if table.cursor_row < len(history):
                entry = history[table.cursor_row]
                self.app.push_screen(DeleteConfirmScreen(entry, self))
    
    def action_back(self) -> None:
        """Go back to main menu."""
        self.app.pop_screen()


class HistoryDetailScreen(ModalScreen):
    """History entry detail screen."""
    
    CSS = """
    HistoryDetailScreen {
        align: center middle;
    }
    
    .detail-container {
        width: 95%;
        height: 90%;
        border: solid $primary;
        padding: 1;
    }
    
    /* LEFT PANEL - ORIGINAL */
    #original-panel {
        width: 1fr;
        height: 1fr;
        border: solid $primary;
        padding: 1;
    }
    
    /* RIGHT PANEL - DECODED */
    #decoded-panel {
        width: 1fr;
        height: 1fr;
        border: solid $success;
        padding: 1;
    }
    
    /* Panel titles */
    .panel-title {
        text-align: center;
        text-style: bold;
        height: auto;
        padding: 1;
    }
    
    /* Content areas */
    .content-scroll {
        height: 1fr;
    }
    
    .content-area {
        width: 100%;
        padding: 1;
    }
    
    /* Header info */
    .header-info {
        height: auto;
        padding: 1;
        border-bottom: solid $primary;
    }
    
    /* Button container */
    .button-container {
        height: auto;
        padding: 1;
        border-top: solid $primary;
        align: center middle;
    }
    """
    
    BINDINGS = [
        Binding("1", "back", "Back"),
        Binding("escape", "back", "Back"),
    ]
    
    def __init__(self, entry):
        super().__init__()
        self.entry = entry
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        with Vertical(classes="detail-container"):
            # Header with metadata
            with Container(classes="header-info"):
                yield Static(f"[bold]ENTRY DETAIL[/bold]")
                yield Static(f"Time: {format_timestamp(self.entry.timestamp)}")
                yield Static(f"Detections: {self.entry.num_replacements}")
            
            # Side-by-side panels
            with Horizontal():
                # LEFT PANEL - ORIGINAL
                with Vertical(id="original-panel"):
                    yield Static("[bold cyan]═══ ORIGINAL ═══[/bold cyan]", classes="panel-title")
                    with ScrollableContainer(classes="content-scroll"):
                        # Convert replacements dicts back to Replacement objects for formatting
                        replacements = [
                            Replacement(
                                start=r.get('start', 0),
                                end=r.get('end', 0),
                                hex_run=r.get('hex_run', ''),
                                decoded=r.get('decoded', '')
                            )
                            for r in self.entry.replacements
                        ]
                        formatted_original = format_text_with_highlights(
                            self.entry.original,
                            replacements,
                            highlight_hex=True  # Highlight hex in yellow
                        )
                        yield Static(formatted_original, classes="content-area")
                
                # RIGHT PANEL - DECODED
                with Vertical(id="decoded-panel"):
                    yield Static("[bold green]═══ DECODED ═══[/bold green]", classes="panel-title")
                    with ScrollableContainer(classes="content-scroll"):
                        # Convert replacements dicts back to Replacement objects for formatting
                        replacements = [
                            Replacement(
                                start=r.get('start', 0),
                                end=r.get('end', 0),
                                hex_run=r.get('hex_run', ''),
                                decoded=r.get('decoded', '')
                            )
                            for r in self.entry.replacements
                        ]
                        # Format decoded text with decoded portions highlighted in green
                        formatted_decoded = format_decoded_text_with_highlights(
                            self.entry.decoded,
                            self.entry.original,
                            replacements
                        )
                        yield Static(formatted_decoded, classes="content-area")
            
            # Button container
            with Container(classes="button-container"):
                yield Button("[1] Back", id="back", variant="default")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "back":
            self.action_back()
    
    def action_back(self) -> None:
        """Go back to history list."""
        self.app.pop_screen()


class DeleteConfirmScreen(ModalScreen):
    """Confirmation dialog for deleting a history entry."""
    
    CSS = """
    DeleteConfirmScreen {
        align: center middle;
    }
    
    .dialog-container {
        width: 50;
        height: auto;
        border: solid $error;
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
        Binding("y", "confirm_delete", "Yes"),
        Binding("n", "cancel", "No"),
        Binding("escape", "cancel", "Cancel"),
    ]
    
    def __init__(self, entry, parent_screen):
        super().__init__()
        self.entry = entry
        self.parent_screen = parent_screen
    
    def compose(self) -> ComposeResult:
        """Create confirmation dialog."""
        with Vertical(classes="dialog-container"):
            yield Static("[bold]Are you sure you want to delete this entry?[/bold]", classes="message")
            with Container(classes="button-container"):
                yield Button("[Y] Yes", id="yes", variant="error")
                yield Button("[N] No", id="no", variant="default")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "yes":
            self.action_confirm_delete()
        elif event.button.id == "no":
            self.action_cancel()
    
    def action_confirm_delete(self) -> None:
        """Confirm and delete the entry."""
        delete_history_entry(self.entry)
        # Close the dialog
        self.app.pop_screen()
        # Refresh the history screen
        self.app.pop_screen()
        self.app.push_screen(HistoryScreen())
    
    def action_cancel(self) -> None:
        """Cancel and return to history screen."""
        self.app.pop_screen()

