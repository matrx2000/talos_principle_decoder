"""Text formatting utilities for UI display."""
from typing import List

from models import Replacement


def create_aligned_banner(title_lines: List[str], subtitle: str = "", width: int = 65) -> str:
    """
    Create a properly aligned ASCII art banner with straight borders.
    
    Args:
        title_lines: List of lines for the main title/ASCII art
        subtitle: Optional subtitle text
        width: Total width of the banner (must be consistent)
        
    Returns:
        Formatted banner string with aligned borders
    """
    # Ensure width is consistent and odd for better centering
    if width % 2 == 0:
        width += 1
    
    # Top border
    top_border = "╔" + "═" * (width - 2) + "╗"
    bottom_border = "╚" + "═" * (width - 2) + "╝"
    empty_line = "║" + " " * (width - 2) + "║"
    
    lines = [top_border, empty_line]
    
    # Add title lines (centered)
    for line in title_lines:
        # Calculate padding to center the line
        line_len = len(line)
        if line_len > width - 4:  # Account for borders and padding
            # Truncate if too long
            line = line[:width - 4]
            line_len = len(line)
        
        padding = (width - 2 - line_len) // 2
        left_pad = padding
        right_pad = width - 2 - line_len - padding
        
        centered_line = "║" + " " * left_pad + line + " " * right_pad + "║"
        lines.append(centered_line)
    
    # Add empty line before subtitle if subtitle exists
    if subtitle:
        lines.append(empty_line)
        # Handle multi-line subtitle
        subtitle_lines = subtitle.split('\n')
        for subtitle_line in subtitle_lines:
            subtitle_len = len(subtitle_line)
            if subtitle_len > width - 4:
                subtitle_line = subtitle_line[:width - 4]
                subtitle_len = len(subtitle_line)
            
            padding = (width - 2 - subtitle_len) // 2
            left_pad = padding
            right_pad = width - 2 - subtitle_len - padding
            
            centered_subtitle = "║" + " " * left_pad + subtitle_line + " " * right_pad + "║"
            lines.append(centered_subtitle)
    
    lines.append(empty_line)
    lines.append(bottom_border)
    
    return "\n".join(lines)


def format_text_with_highlights(original_text: str, reps: List[Replacement], highlight_hex: bool = True) -> str:
    """
    Format text with Textual/Rich markup for highlighting hex sequences or decoded portions.
    
    Args:
        original_text: The ORIGINAL text (before decoding) to format
        reps: List of replacements with positions in original text
        highlight_hex: If True, highlight hex runs in yellow; if False, highlight decoded text in green
        
    Returns:
        Formatted text with Textual/Rich markup
    """
    if not reps:
        return original_text
    
    # Sort replacements by start position
    reps_sorted = sorted(reps, key=lambda x: x.start)
    
    result = []
    cursor = 0
    
    for r in reps_sorted:
        # Add text before this replacement (unchanged)
        result.append(original_text[cursor:r.start])
        
        if highlight_hex:
            # Show original hex with yellow highlight
            result.append(f"[bold yellow]{original_text[r.start:r.end]}[/bold yellow]")
        else:
            # Show decoded text with green highlight
            result.append(f"[bold green]{r.decoded}[/bold green]")
        
        cursor = r.end
    
    # Add remaining text after last replacement
    result.append(original_text[cursor:])
    
    return "".join(result)


def format_decoded_text_with_highlights(decoded_text: str, original_text: str, reps: List[Replacement]) -> str:
    """
    Format decoded text with Textual/Rich markup highlighting the decoded portions in green.
    
    This function builds the formatted text by applying replacements and highlighting
    the decoded portions in green, matching the structure of the decoded text.
    
    Args:
        decoded_text: The decoded text (after replacements applied) - used for validation
        original_text: The original text (before decoding)
        reps: List of replacements with positions in original text
        
    Returns:
        Formatted decoded text with decoded portions highlighted in green
    """
    if not reps:
        return decoded_text
    
    # Sort replacements by start position in original text
    reps_sorted = sorted(reps, key=lambda x: x.start)
    
    # Build the formatted decoded text by applying replacements and highlighting
    result = []
    cursor = 0
    
    for r in reps_sorted:
        # Add text before this replacement (unchanged text)
        result.append(original_text[cursor:r.start])
        
        # Add the decoded portion highlighted in green
        result.append(f"[bold green]{r.decoded}[/bold green]")
        
        cursor = r.end
    
    # Add remaining text after last replacement
    result.append(original_text[cursor:])
    
    return "".join(result)


def format_timestamp(timestamp: str) -> str:
    """
    Format ISO timestamp to readable format.
    
    Args:
        timestamp: ISO format timestamp string
        
    Returns:
        Formatted timestamp string
    """
    from datetime import datetime
    try:
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return timestamp
