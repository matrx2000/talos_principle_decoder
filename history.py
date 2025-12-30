"""History management for storing and retrieving decode history."""
import json
import os
from typing import List, Optional
from datetime import datetime

from models import Replacement, HistoryEntry

# History database file
HISTORY_FILE = "talos_history.json"
MAX_HISTORY_ENTRIES = 1000


def load_history() -> List[HistoryEntry]:
    """
    Load history from JSON file.
    
    Returns:
        List of HistoryEntry objects
    """
    if not os.path.exists(HISTORY_FILE):
        return []
    
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [HistoryEntry.from_dict(entry) for entry in data]
    except (json.JSONDecodeError, IOError):
        return []


def save_history(history: List[HistoryEntry]) -> None:
    """
    Save history to JSON file.
    
    Args:
        history: List of HistoryEntry objects to save
    """
    try:
        data = [entry.to_dict() for entry in history]
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except IOError:
        pass  # Silently fail if we can't write


def add_to_history(original: str, decoded: str, replacements: List[Replacement]) -> None:
    """
    Add a new entry to history.
    
    Args:
        original: Original text
        decoded: Decoded text
        replacements: List of replacements that were applied
    """
    history = load_history()
    
    entry = HistoryEntry(
        timestamp=datetime.now().isoformat(),
        original=original,
        decoded=decoded,
        num_replacements=len(replacements),
        replacements=[
            {
                "hex_run": r.hex_run,
                "decoded": r.decoded,
                "start": r.start,
                "end": r.end
            }
            for r in replacements
        ]
    )
    
    history.append(entry)
    # Keep only last MAX_HISTORY_ENTRIES entries to prevent file from growing too large
    if len(history) > MAX_HISTORY_ENTRIES:
        history = history[-MAX_HISTORY_ENTRIES:]
    
    save_history(history)


def delete_history_entry(entry: HistoryEntry) -> bool:
    """
    Delete a history entry.
    
    Args:
        entry: HistoryEntry to delete
        
    Returns:
        True if entry was found and deleted, False otherwise
    """
    history = load_history()
    
    # Find and remove entry
    for i, e in enumerate(history):
        if (e.timestamp == entry.timestamp and 
            e.original == entry.original and 
            e.decoded == entry.decoded):
            history.pop(i)
            save_history(history)
            return True
    
    return False


def get_history_count() -> int:
    """Get the number of history entries."""
    return len(load_history())

