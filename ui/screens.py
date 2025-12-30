"""Textual screens for Talos Decoder.

This module re-exports all screen classes for backward compatibility.
Individual screens are now in separate files for better maintainability.
"""
from ui.main_menu_screen import MainMenuScreen
from ui.decode_screen import DecodeScreen
from ui.history_screen import HistoryScreen, HistoryDetailScreen
from ui.about_screen import AboutScreen

# Re-export for backward compatibility
__all__ = [
    "MainMenuScreen",
    "DecodeScreen",
    "HistoryScreen",
    "HistoryDetailScreen",
    "AboutScreen",
]
