"""Data models for the Talos Decoder application."""
from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class Replacement:
    """Represents a hex byte sequence replacement."""
    start: int
    end: int
    hex_run: str
    decoded: str


@dataclass
class DecodeResult:
    """Result of decoding text containing hex sequences."""
    original: str
    decoded: str
    replacements: List[Replacement]
    num_replacements: int
    
    @property
    def total_hex_bytes(self) -> int:
        """Calculate total number of hex bytes decoded."""
        import re
        return sum(len(re.findall(r"\b[0-9A-Fa-f]{2}\b", r.hex_run)) for r in self.replacements)
    
    @property
    def total_decoded_chars(self) -> int:
        """Calculate total number of decoded characters."""
        return sum(len(r.decoded) for r in self.replacements)
    
    @property
    def avg_bytes_per_run(self) -> float:
        """Calculate average bytes per replacement."""
        if not self.replacements:
            return 0.0
        return self.total_hex_bytes / len(self.replacements)


@dataclass
class HistoryEntry:
    """Represents a history entry."""
    timestamp: str
    original: str
    decoded: str
    num_replacements: int
    replacements: List[Dict[str, Any]]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HistoryEntry':
        """Create HistoryEntry from dictionary."""
        return cls(
            timestamp=data.get('timestamp', ''),
            original=data.get('original', ''),
            decoded=data.get('decoded', ''),
            num_replacements=data.get('num_replacements', 0),
            replacements=data.get('replacements', [])
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert HistoryEntry to dictionary."""
        return {
            'timestamp': self.timestamp,
            'original': self.original,
            'decoded': self.decoded,
            'num_replacements': self.num_replacements,
            'replacements': self.replacements
        }

