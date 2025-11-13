"""Mode definitions for Glaemscribe."""

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

from .charset import Charset


@dataclass
class TranscriptionRule:
    """Represents a single transcription rule."""
    pattern: str
    replacement: str
    priority: int = 0
    enabled: bool = True
    
    def __post_init__(self):
        """Compile the regex pattern for efficient matching."""
        try:
            self.compiled_pattern = re.compile(self.pattern, re.IGNORECASE)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern '{self.pattern}': {e}")


@dataclass
class Mode:
    """Represents a transcription mode."""
    name: str
    language: str
    writing: str
    human_name: str
    authors: str
    version: str
    options: Dict[str, Any] = field(default_factory=dict)
    supported_charsets: Dict[str, Charset] = field(default_factory=dict)
    default_charset: Optional[str] = None
    rules: List[TranscriptionRule] = field(default_factory=list)
    
    def transcribe(self, text: str, charset: Optional[str] = None, **options) -> str:
        """Transcribe text using this mode."""
        charset_name = charset or self.default_charset
        if not charset_name:
            raise ValueError("No charset specified and no default charset available")
            
        if charset_name not in self.supported_charsets:
            raise ValueError(f"Charset '{charset_name}' is not supported by this mode")
        
        # Apply rules in priority order
        result = text
        sorted_rules = sorted(self.rules, key=lambda r: r.priority, reverse=True)
        
        for rule in sorted_rules:
            if rule.enabled:
                result = rule.compiled_pattern.sub(rule.replacement, result)
        
        # Convert to target charset
        result = self._convert_to_charset(result, charset_name)
        
        return result
    
    def _convert_to_charset(self, text: str, charset_name: str) -> str:
        """Convert the transcribed text to the target character set."""
        charset = self.supported_charsets[charset_name]
        result = text
        
        # Replace character names with actual characters
        for char_name, char_value in charset.characters.items():
            pattern = r'\b' + re.escape(char_name) + r'\b'
            result = re.sub(pattern, char_value, result, flags=re.IGNORECASE)
        
        return result
    
    def add_rule(self, pattern: str, replacement: str, priority: int = 0):
        """Add a new transcription rule."""
        rule = TranscriptionRule(pattern=pattern, replacement=replacement, priority=priority)
        self.rules.append(rule)
