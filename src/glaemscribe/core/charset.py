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
    
    def has_character(self, char_name: str) -> bool:
        """Check if a character name exists in this charset."""
        return char_name in self.characters
    
    def __getitem__(self, char_name: str) -> Optional[str]:
        """Allow dictionary-style access to characters."""
        return self.characters.get(char_name)
    
    def get(self, char_name: str, default: Optional[str] = None) -> Optional[str]:
        """Get character with default value."""
        return self.characters.get(char_name, default)
    
    def resolve_virtual(self, virtual_name: str) -> Optional[str]:
        """Resolve a virtual character to its definition."""
        return self.virtual_chars.get(virtual_name)
