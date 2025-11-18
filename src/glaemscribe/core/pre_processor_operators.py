"""Pre-processor operators for Glaemscribe.

These operators handle text transformations before transcription,
following the JavaScript implementation exactly.
"""

import re
from typing import Any
from .post_processor.base import PrePostProcessorOperator
from ..parsers.glaeml import Node


class SubstitutePreProcessorOperator(PrePostProcessorOperator):
    """Simple string substitution operator.
    
    Matches JavaScript's SubstitutePreProcessorOperator exactly.
    """
    
    def apply(self, text: str) -> str:
        """Apply simple string substitution.
        
        Uses indexOf loop instead of regex to handle special characters.
        """
        # Use finalized element if available, otherwise fall back to original
        if self.finalized_glaeml_element:
            in_to_replace = self.finalized_glaeml_element.args[0]
            in_replace_with = self.finalized_glaeml_element.args[1]
        else:
            in_to_replace = self.glaeml_element.args[0]
            in_replace_with = self.glaeml_element.args[1]
        
        in_source = text
        out_string = []
        rep_len = len(in_to_replace)
        idx = in_source.find(in_to_replace)
        
        while idx != -1:
            out_string.append(in_source[:idx])
            out_string.append(in_replace_with)
            in_source = in_source[idx + rep_len:]
            idx = in_source.find(in_to_replace)
        
        out_string.append(in_source)
        return ''.join(out_string)


class RxSubstitutePreProcessorOperator(PrePostProcessorOperator):
    """Regex substitution operator.
    
    Matches JavaScript's RxSubstitutePreProcessorOperator exactly.
    """
    
    def finalize(self, trans_options: dict):
        """Finalize the operator, converting Ruby-style backrefs to Python-style."""
        super().finalize(trans_options)
        
        # Ruby uses \1, \2, etc for captured expressions.
        # Convert to Python style (we'll handle this in apply() using a custom replacement function)
        if self.finalized_glaeml_element and len(self.finalized_glaeml_element.args) > 1:
            replacement = self.finalized_glaeml_element.args[1]
            # Store the replacement pattern for use in apply()
            self._replacement_pattern = replacement
    
    def apply(self, text: str) -> str:
        """Apply regex substitution."""
        # Use finalized element if available, otherwise fall back to original
        if self.finalized_glaeml_element:
            pattern = self.finalized_glaeml_element.args[0]
            replacement = self._replacement_pattern
        else:
            pattern = self.glaeml_element.args[0]
            replacement = self.glaeml_element.args[1]
        
        def replace_func(match):
            """Handle backreferences in replacement."""
            result = replacement
            # Replace backreferences \1, \2 with actual groups
            for i, group in enumerate(match.groups(), 1):
                result = result.replace(f'\\{i}', group)
            return result
        
        regex = re.compile(pattern)
        return regex.sub(replace_func, text)
