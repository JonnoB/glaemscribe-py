"""
Tengwar font renderer.

Provides functionality to render Tengwar Unicode text as images,
solving the "tofu" problem where characters appear as boxes.
"""

from PIL import Image, ImageDraw, ImageFont
import io
import base64
import os
from typing import Optional, Tuple, Union


class TengwarRenderer:
    """Renders Tengwar Unicode text as images."""
    
    # Bundled fonts (AGPL-3.0 licensed from Glaemscribe project)
    # Only fonts that actually support FTF/Everson Unicode mapping are listed
    BUNDLED_FONTS = {
        'eldamar': 'tengwar-eldamar-glaemscrafu-noautohint.ttf',  # ✅ Full FTF/Everson support
        # Legacy fonts (limited or no FTF/Everson support):
        # 'annatar': 'tengwar-annatar-glaemscrafu-noautohint.ttf',      # ❌ Empty glyphs
        # 'parmaite': 'tengwar-parmaite-glaemscrafu-noautohint.ttf',    # ❌ Reports tofu
        # 'elfica': 'tengwar-elfica-glaemscrafu-noautohint.ttf',        # ❌ Unknown support
        # 'sindarin': 'tengwar-sindarin-glaemscrafu-noautohint.ttf',    # ❌ Unknown support
    }
    
    def __init__(self, font_name: str = 'eldamar', font_path: Optional[str] = None, font_size: int = 24):
        """
        Initialize the renderer.
        
        Args:
            font_name: Name of bundled font to use (see BUNDLED_FONTS)
            font_path: Path to custom Tengwar font file. If provided, overrides font_name.
            font_size: Font size for rendering.
        """
        self.font_size = font_size
        self.font = None
        
        # Determine font path
        if font_path:
            self.font_path = font_path
        else:
            # Use bundled font
            font_filename = self.BUNDLED_FONTS.get(font_name, self.BUNDLED_FONTS['eldamar'])
            fonts_dir = os.path.join(os.path.dirname(__file__), 'fonts')
            self.font_path = os.path.join(fonts_dir, font_filename)
        
        # Load the font
        try:
            self.font = ImageFont.truetype(self.font_path, font_size)
        except Exception as e:
            print(f"Warning: Could not load font {self.font_path}: {e}")
            print("Falling back to default font (will show tofu)")
            self.font = None
    
    def render_text(self, text: str, 
                   output_format: str = "PNG",
                   size: Optional[Tuple[int, int]] = None,
                   padding: int = 10,
                   background_color: str = "white",
                   text_color: str = "black") -> Image.Image:
        """
        Render Tengwar text as an image.
        
        Args:
            text: The Tengwar Unicode text to render
            output_format: Image format (PNG, JPEG, etc.)
            size: Optional fixed size for the image (width, height)
            padding: Padding around the text
            background_color: Background color
            text_color: Text color
            
        Returns:
            PIL Image object
        """
        if not self.font:
            # Fallback to default font (will show tofu, but at least works)
            self.font = ImageFont.load_default()
        
        # Create a temporary image to measure text
        temp_draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        bbox = temp_draw.textbbox((0, 0), text, font=self.font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Calculate image size
        if size:
            img_width, img_height = size
        else:
            img_width = text_width + (padding * 2)
            img_height = text_height + (padding * 2)
        
        # Create the actual image
        image = Image.new("RGB", (img_width, img_height), background_color)
        draw = ImageDraw.Draw(image)
        
        # Calculate text position (centered)
        text_x = (img_width - text_width) // 2
        text_y = (img_height - text_height) // 2
        
        # Draw the text
        draw.text((text_x, text_y), text, font=self.font, fill=text_color)
        
        return image
    
    def render_to_file(self, text: str, 
                      output_path: str,
                      **kwargs) -> None:
        """
        Render Tengwar text directly to a file.
        
        Args:
            text: The Tengwar Unicode text to render
            output_path: Path to save the image
            **kwargs: Additional arguments passed to render_text()
        """
        image = self.render_text(text, **kwargs)
        image.save(output_path)
    
    def render_to_bytes(self, text: str, 
                       format: str = "PNG",
                       **kwargs) -> bytes:
        """
        Render Tengwar text to bytes.
        
        Args:
            text: The Tengwar Unicode text to render
            format: Image format
            **kwargs: Additional arguments passed to render_text()
            
        Returns:
            Image data as bytes
        """
        image = self.render_text(text, **kwargs)
        buffer = io.BytesIO()
        image.save(buffer, format=format)
        return buffer.getvalue()
    
    def render_to_base64(self, text: str,
                        format: str = "PNG", 
                        **kwargs) -> str:
        """
        Render Tengwar text to base64 string for web embedding.
        
        Args:
            text: The Tengwar Unicode text to render
            format: Image format
            **kwargs: Additional arguments passed to render_text()
            
        Returns:
            Base64-encoded image string
        """
        image_bytes = self.render_to_bytes(text, format, **kwargs)
        b64_bytes = base64.b64encode(image_bytes)
        return b64_bytes.decode('ascii')
    
    def render_html_embed(self, text: str, 
                         alt_text: str = "Tengwar text",
                         **kwargs) -> str:
        """
        Render Tengwar text as embeddable HTML.
        
        Args:
            text: The Tengwar Unicode text to render
            alt_text: Alt text for accessibility
            **kwargs: Additional arguments passed to render_text()
            
        Returns:
            HTML img tag with base64-encoded image
        """
        b64_data = self.render_to_base64(text, **kwargs)
        format = kwargs.get('format', 'PNG')
        return f'<img src="data:image/{format.lower()};base64,{b64_data}" alt="{alt_text}" />'


# Convenience functions for quick usage
def render_tengwar(text: str, output_path: str, **kwargs) -> None:
    """Quick function to render Tengwar text to file."""
    renderer = TengwarRenderer()
    renderer.render_to_file(text, output_path, **kwargs)


def tengwar_to_image(text: str, **kwargs) -> Image.Image:
    """Quick function to get PIL Image of Tengwar text."""
    renderer = TengwarRenderer()
    return renderer.render_text(text, **kwargs)


def tengwar_to_base64(text: str, **kwargs) -> str:
    """Quick function to get base64 of Tengwar text."""
    renderer = TengwarRenderer()
    return renderer.render_to_base64(text, **kwargs)
