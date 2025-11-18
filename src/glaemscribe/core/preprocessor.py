"""Preprocessor for Glaemscribe modes.

Handles text substitutions before transcription, including:
- Simple substitutions (e.g., ë → e)
- Regex substitutions (e.g., ā/â/aa → á)
"""

import re
from typing import List, Dict, Tuple, Pattern


class SubstitutionOperator:
    """Base class for substitution operators."""
    
    def __init__(self, pattern: str, replacement: str, line: int = 0):
        self.pattern = pattern
        self.replacement = replacement
        self.line = line
    
    def apply(self, text: str) -> str:
        """Apply the substitution to the text."""
        raise NotImplementedError("Subclasses must implement apply()")


class SubstituteOperator(SubstitutionOperator):
    """Simple string substitution operator."""
    
    def apply(self, text: str) -> str:
        """Apply simple string substitution."""
        return text.replace(self.pattern, self.replacement)


class RxSubstituteOperator(SubstitutionOperator):
    """Regex substitution operator."""
    
    def __init__(self, pattern: str, replacement: str, line: int = 0):
        super().__init__(pattern, replacement, line)
        # Compile the regex pattern
        try:
            self.regex = re.compile(pattern)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern at line {line}: {pattern} - {e}")
    
    def apply(self, text: str) -> str:
        """Apply regex substitution."""
        return self.regex.sub(self.replacement, text)


class Preprocessor:
    """Handles text preprocessing for Glaemscribe modes."""
    
    def __init__(self):
        self.operators: List[SubstitutionOperator] = []
    
    def add_substitute(self, pattern: str, replacement: str, line: int = 0):
        """Add a simple substitution operator."""
        self.operators.append(SubstituteOperator(pattern, replacement, line))
    
    def add_rxsubstitute(self, pattern: str, replacement: str, line: int = 0):
        """Add a regex substitution operator."""
        self.operators.append(RxSubstituteOperator(pattern, replacement, line))
    
    def apply(self, text: str) -> str:
        """Apply all substitutions to the text."""
        result = text
        for operator in self.operators:
            result = operator.apply(result)
        return result
    
    def clear(self):
        """Clear all operators."""
        self.operators.clear()
    
    def __str__(self) -> str:
        """String representation of the preprocessor."""
        return f"<Preprocessor: {len(self.operators)} operators>"
