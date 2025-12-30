"""Main entry point for Talos Decoder."""
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Header, Footer, Static, TextArea, Label
from textual.screen import Screen

from ui.screens import MainMenuScreen


class TalosDecoderApp(App):
    """Main application class using Textual."""
    
    TITLE = "Talos Decoder"
    SHOW_HEADER = False  # Disable default header to show custom banner
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    .banner {
        text-align: center;
        padding: 1;
    }
    
    .button-row {
        align: center middle;
        padding: 1;
    }
    
    Button {
        margin: 1;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]
    
    def on_mount(self) -> None:
        """Called when app starts."""
        self.push_screen(MainMenuScreen())
    
    def action_quit(self) -> None:
        """Quit the application."""
        self.exit()


def main() -> None:
    """Main entry point."""
    import sys
    import atexit
    
    def cleanup_terminal():
        """Ensure terminal is restored on exit."""
        try:
            # Reset terminal to normal mode
            print("\033[?25h", end="")  # Show cursor
            print("\033[0m", end="")    # Reset colors
            sys.stdout.flush()
        except:
            pass
    
    # Register cleanup function
    atexit.register(cleanup_terminal)
    
    try:
        app = TalosDecoderApp()
        app.run()
    except KeyboardInterrupt:
        cleanup_terminal()
        sys.exit(0)
    except Exception as e:
        cleanup_terminal()
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
