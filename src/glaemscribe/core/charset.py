"""Character set definitions for Glaemscribe."""

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class Charset:
    """Represents a character set for a writing system."""
    name: str
    version: str
    characters: Dict[str, str] = field(default_factory=dict)
    virtual_chars: Dict[str, str] = field(default_factory=dict)
    
    def get_character(self, char_name: str) -> str:
        """Get the Unicode character for a given character name."""
        return self.characters.get(char_name, char_name)
    
    def resolve_virtual(self, virtual_name: str) -> Optional[str]:
        """Resolve a virtual character to its definition."""
        return self.virtual_chars.get(virtual_name)
