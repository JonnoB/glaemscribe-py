"""Public API for Glaemscribe."""

from typing import Dict, List, Optional, Any

from .core.charset import Charset
from .core.mode import Mode


class Glaemscribe:
    """Main interface for the Glaemscribe transcription library."""
    
    def __init__(self):
        """Initialize a new Glaemscribe instance."""
        self.modes: Dict[str, Mode] = {}
        self.charsets: Dict[str, Charset] = {}
    
    def add_charset(self, charset: Charset):
        """Add a character set."""
        self.charsets[charset.name] = charset
    
    def add_mode(self, mode: Mode):
        """Add a transcription mode."""
        self.modes[mode.name] = mode
    
    def transcribe(self, text: str, mode_name: str, charset: Optional[str] = None) -> str:
        """Transcribe text using the specified mode."""
        if mode_name not in self.modes:
            raise ValueError(f"Mode '{mode_name}' not found")
        
        mode = self.modes[mode_name]
        return mode.transcribe(text, charset)
    
    def list_modes(self) -> List[str]:
        """List all available modes."""
        return list(self.modes.keys())
    
    def list_charsets(self) -> List[str]:
        """List all available character sets."""
        return list(self.charsets.keys())
