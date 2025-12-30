# Talos Decoder - Architecture Documentation

## Overview

The Talos Decoder has been refactored into a clean, maintainable architecture with clear separation of concerns. This document explains the structure and design decisions.

## Project Structure

```
Talos Decoder/
├── main.py                 # Application entry point
├── models.py               # Data models (Replacement, DecodeResult, HistoryEntry)
├── decoder.py              # Core hex decoding logic
├── history.py              # History management (load, save, add, delete)
├── ui/                     # UI components
│   ├── __init__.py
│   ├── screens.py          # Compatibility layer (re-exports screen classes)
│   ├── main_menu_screen.py # Main menu screen
│   ├── decode_screen.py    # Decode screen (input/output panels)
│   ├── history_screen.py   # History browser screens
│   ├── about_screen.py     # About screen
│   ├── constants.py        # UI constants (banners, etc.)
│   └── formatters.py       # Text formatting utilities
├── images/                 # Image assets
│   └── demo.png            # Demo screenshot for README
├── requirements.txt
├── README.md
├── ARCHITECTURE.md         # This file
└── talos_history.json      # History database (created automatically)
```

## Architecture Layers

### 1. Data Models (`models.py`)

**Purpose**: Define data structures used throughout the application.

**Classes**:
- `Replacement`: Represents a single hex byte sequence replacement
- `DecodeResult`: Complete result of a decode operation with statistics
- `HistoryEntry`: Represents a saved history entry

**Benefits**:
- Type safety and clear data contracts
- Centralized data structure definitions
- Easy to extend with new fields

### 2. Business Logic Layer

#### `decoder.py` - Core Decoding Logic

**Purpose**: Pure business logic for hex decoding. No UI dependencies.

**Functions**:
- `find_replacements(text)`: Find hex sequences in text
- `apply_replacements(text, reps)`: Apply replacements to text
- `decode_text(text)`: Main decoding function returning DecodeResult

**Benefits**:
- Testable without UI
- Reusable in other contexts (CLI, API, etc.)
- Single responsibility: hex decoding only

#### `history.py` - History Management

**Purpose**: Handle persistence and retrieval of decode history.

**Functions**:
- `load_history()`: Load history from JSON file
- `save_history(history)`: Save history to JSON file
- `add_to_history(...)`: Add new entry
- `delete_history_entry(entry)`: Delete entry
- `get_history_count()`: Get count of entries

**Benefits**:
- Encapsulates file I/O
- Easy to change storage backend (database, etc.)
- Centralized history management

### 3. UI Layer (`ui/`)

**Purpose**: All Textual-specific code. Handles presentation only.

**Modules**:
- `screens.py`: Compatibility layer that re-exports all screen classes
- `main_menu_screen.py`: Main menu screen with navigation buttons
- `decode_screen.py`: Decode screen with side-by-side input/output panels
- `history_screen.py`: History browser and detail screens
- `about_screen.py`: About/info screen
- `constants.py`: UI constants (banners, titles)
- `formatters.py`: Text formatting utilities (markup, timestamps, highlights)

**Benefits**:
- UI can be swapped (web, desktop, CLI) without changing logic
- Clear separation of presentation from business logic
- Easier to test business logic independently
- Modern Textual framework with better performance and features

### 4. Application Layer (`main.py`)

**Purpose**: Orchestrates the application, connects UI to business logic.

**Class**: `TalosDecoderApp`
- Manages application state
- Connects Textual screens to business logic
- Handles screen navigation and lifecycle

**Benefits**:
- Single entry point
- Clear application flow
- Easy to add features (settings, themes, etc.)

## Design Principles

### 1. Separation of Concerns
- **Business Logic**: No UI dependencies
- **UI Layer**: Only handles presentation
- **Data Models**: Shared between layers

### 2. Single Responsibility Principle
Each module has one clear purpose:
- `decoder.py` → Decoding only
- `history.py` → History management only
- `ui/*.py` → UI components only

### 3. Dependency Direction
```
main.py → ui/ → decoder.py, history.py
                ↓
            models.py
```

UI depends on business logic, not vice versa. This allows:
- Testing business logic without UI
- Replacing UI without changing logic
- Using business logic in other contexts

### 4. Data Flow
```
User Input → UI → Business Logic → Data Models → History
                ↓
            UI Display
```

## Benefits of This Architecture

### Maintainability
- **Easy to locate code**: Clear file organization
- **Easy to modify**: Changes isolated to specific modules
- **Easy to understand**: Clear responsibilities

### Testability
- Business logic can be tested independently
- UI can be mocked for testing
- Data models provide clear test fixtures

### Extensibility
- Add new UI components without touching logic
- Add new features (export, import) easily
- Swap UI framework (e.g., to web) without changing core

### Reusability
- Decoder logic can be used in scripts, APIs, etc.
- History management can be reused in other projects
- Models provide clear interfaces

## Adding New Features

### Example: Add Export Functionality

1. **Add to business logic** (`history.py`):
   ```python
   def export_history(format: str) -> str:
       # Export logic
   ```

2. **Add UI component** (`ui/export_window.py`):
   ```python
   def show_export_window(manager):
       # UI for export
   ```

3. **Wire up in main** (`main.py`):
   ```python
   def on_export(self):
       show_export_window(self.manager)
   ```

### Example: Add Different UI Framework

1. Keep all business logic (`decoder.py`, `history.py`, `models.py`)
2. Create new UI layer (e.g., `ui_web/` or `ui_cli/`)
3. Update `main.py` to use new UI

## Testing Strategy

### Unit Tests
- Test `decoder.py` functions with various inputs
- Test `history.py` with mock file operations
- Test `models.py` data transformations

### Integration Tests
- Test UI components with mock business logic
- Test full decode workflow

### Example Test Structure
```
tests/
├── test_decoder.py
├── test_history.py
├── test_models.py
└── test_ui/
    └── test_screens.py
```

## Future Improvements

1. **Configuration Management**: Add `config.py` for settings
2. **Error Handling**: Centralized error handling module
3. **Logging**: Add logging throughout application
4. **Validation**: Input validation layer
5. **Plugins**: Plugin system for extensions

## Migration Notes

The refactored code maintains 100% backward compatibility:
- Same functionality
- Same history file format
- Same user experience

All existing history files will continue to work.

