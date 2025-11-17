"""
Wrapper around the Rust tengwar library for FTF/CSUR Unicode transcription.

This provides a simple interface to the Rust tengwar tool, which implements
the official FTF/CSUR Unicode standard for Tengwar characters.
"""

import subprocess
import shutil
from typing import Optional, Tuple


class TengwarRustWrapper:
    """
    Wrapper for the Rust tengwar library.
    
    This uses the official Rust implementation which correctly implements
    the FTF/CSUR Unicode standard for Tengwar characters.
    """
    
    def __init__(self):
        """Initialize the wrapper and check if tengwar binary is available."""
        self.tengwar_path = shutil.which('tengwar')
        if not self.tengwar_path:
            raise RuntimeError(
                "Rust 'tengwar' binary not found. Install it with: cargo install tengwar"
            )
    
    def transcribe(self, text: str, mode: str = 'quenya') -> Tuple[bool, str, str]:
        """
        Transcribe Latin text to Tengwar using the Rust library.
        
        Args:
            text: Latin text to transcribe
            mode: Tengwar mode ('quenya', 'beleriand', 'gondor')
        
        Returns:
            Tuple of (success, result, error_message)
        """
        try:
            # Map mode names to Rust library flags
            mode_flags = {
                'quenya': [],  # Default mode
                'beleriand': ['--beleriand'],
                'gondor': ['--gondor'],
            }
            
            flags = mode_flags.get(mode, [])
            
            # Run the tengwar command
            result = subprocess.run(
                [self.tengwar_path] + flags + [text],
                capture_output=True,
                text=True,
                check=True
            )
            
            return (True, result.stdout.strip(), "")
            
        except subprocess.CalledProcessError as e:
            return (False, "", f"Tengwar command failed: {e.stderr}")
        except Exception as e:
            return (False, "", f"Error running tengwar: {str(e)}")
    
    @staticmethod
    def is_available() -> bool:
        """Check if the Rust tengwar binary is available."""
        return shutil.which('tengwar') is not None


# Convenience function
def transcribe_with_rust(text: str, mode: str = 'quenya') -> Tuple[bool, str, str]:
    """
    Transcribe text using the Rust tengwar library.
    
    This is a convenience function that creates a wrapper instance and
    transcribes the text.
    
    Args:
        text: Latin text to transcribe
        mode: Tengwar mode ('quenya', 'beleriand', 'gondor')
    
    Returns:
        Tuple of (success, result, error_message)
    
    Example:
        >>> success, result, error = transcribe_with_rust("Elen sila")
        >>> if success:
        ...     print(f"Tengwar: {result}")
    """
    try:
        wrapper = TengwarRustWrapper()
        return wrapper.transcribe(text, mode)
    except RuntimeError as e:
        return (False, "", str(e))
