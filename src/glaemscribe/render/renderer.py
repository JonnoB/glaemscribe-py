"""Tengwar font renderer.

Provides functionality to render Tengwar Unicode text as images,
solving the "tofu" problem where characters appear as boxes.

This module offers both a class-based API (TengwarRenderer) for fine control
and convenience functions for quick rendering tasks.

Quick Start:
    >>> from glaemscribe import transcribe
    >>> from glaemscribe.render import TengwarRenderer
    >>> 
    >>> # Transcribe text to Tengwar Unicode
    >>> tengwar = transcribe("Elen síla lúmenn' omentielvo", mode="quenya")
    >>> 
    >>> # Render with default bundled font
    >>> renderer = TengwarRenderer()
    >>> renderer.render_to_file(tengwar, "output.png")
    >>> 
    >>> # Or use a custom font
    >>> renderer = TengwarRenderer(font_path="fonts/MyTengwar.ttf", font_size=48)
    >>> renderer.render_to_file(tengwar, "output.png")

Convenience Functions:
    For simple one-off rendering tasks, use the convenience functions:
    
    >>> from glaemscribe.render import render_tengwar
    >>> render_tengwar(tengwar_text, "output.png", font_size=36)

Available Bundled Fonts:
    - 'freemono' (default): FreeMonoTengwar
    - 'alcarin-reg': AlcarinTengwar-Regular
    - 'alcarin-bold': AlcarinTengwar-Bold
"""

from PIL import Image, ImageDraw, ImageFont
import io
import base64
import os
from typing import Optional, Tuple, Union


class TengwarRenderer:
    """Renders Tengwar Unicode text as images.
    
    This class provides a flexible interface for rendering Tengwar Unicode text
    to various output formats (PNG, JPEG, base64, HTML). It supports both bundled
    fonts and custom font files.
    
    Attributes:
        BUNDLED_FONTS (dict): Available bundled fonts (OFL licensed)
        font_size (int): Current font size in points
        font_path (str): Path to the loaded font file
        font (ImageFont): Loaded PIL font object
    
    Examples:
        Basic usage with bundled font:
            >>> from glaemscribe import transcribe
            >>> from glaemscribe.render import TengwarRenderer
            >>> 
            >>> tengwar = transcribe("aiya", mode="quenya")
            >>> renderer = TengwarRenderer(font_size=48)
            >>> renderer.render_to_file(tengwar, "output.png")
        
        Using a custom font:
            >>> renderer = TengwarRenderer(
            ...     font_path="fonts/MyTengwar.ttf",
            ...     font_size=72
            ... )
            >>> renderer.render_to_file(tengwar, "output.png", padding=20)
        
        Using different bundled fonts:
            >>> # Use AlcarinTengwar Bold
            >>> renderer = TengwarRenderer(font_name='alcarin-bold', font_size=36)
            >>> renderer.render_to_file(tengwar, "bold_output.png")
        
        Customizing appearance:
            >>> renderer = TengwarRenderer()
            >>> renderer.render_to_file(
            ...     tengwar,
            ...     "custom.png",
            ...     background_color="black",
            ...     text_color="gold",
            ...     padding=30
            ... )
    """
    
    # Bundled fonts (OFL licensed)
    BUNDLED_FONTS = {
        'freemono': 'FreeMonoTengwar.ttf',
        'alcarin-reg': 'AlcarinTengwar-Regular.ttf',
        'alcarin-bold': 'AlcarinTengwar-Bold.ttf',
    }
    
    def __init__(self, font_name: str = 'freemono', font_path: Optional[str] = None, font_size: int = 24):
        """Initialize the renderer.
        
        Args:
            font_name (str): Name of bundled font to use. Options:
                - 'freemono' (default): FreeMonoTengwar
                - 'alcarin-reg': AlcarinTengwar-Regular
                - 'alcarin-bold': AlcarinTengwar-Bold
            font_path (str, optional): Path to custom Tengwar font file.
                If provided, overrides font_name. Can be absolute or relative.
            font_size (int): Font size in points. Default is 24.
        
        Raises:
            Warning: If font cannot be loaded, falls back to default font
        
        Examples:
            >>> # Use default bundled font
            >>> renderer = TengwarRenderer()
            
            >>> # Use a different bundled font
            >>> renderer = TengwarRenderer(font_name='alcarin-bold', font_size=48)
            
            >>> # Use a custom font file
            >>> renderer = TengwarRenderer(font_path="fonts/MyTengwar.ttf")
        """
        self.font_size = font_size
        self.font = None
        
        # Determine font path
        if font_path:
            self.font_path = font_path
        else:
            # Use bundled font
            font_filename = self.BUNDLED_FONTS.get(font_name, self.BUNDLED_FONTS['freemono'])
            # Fonts are in src/glaemscribe/fonts/
            fonts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fonts')
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
        """Render Tengwar text as an image.
        
        Args:
            text (str): The Tengwar Unicode text to render
            output_format (str): Image format (PNG, JPEG, etc.). Default: "PNG"
            size (tuple, optional): Fixed size for the image (width, height) in pixels.
                If None, size is calculated from text dimensions.
            padding (int): Padding around the text in pixels. Default: 10
            background_color (str): Background color name or hex code. Default: "white"
            text_color (str): Text color name or hex code. Default: "black"
            
        Returns:
            Image.Image: PIL Image object containing the rendered text
        
        Examples:
            >>> renderer = TengwarRenderer()
            >>> img = renderer.render_text(tengwar_text)
            >>> img.show()  # Display the image
            
            >>> # Custom styling
            >>> img = renderer.render_text(
            ...     tengwar_text,
            ...     padding=20,
            ...     background_color="#2c3e50",
            ...     text_color="#ecf0f1"
            ... )
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
        """Render Tengwar text directly to a file.
        
        This is the most common method for saving rendered Tengwar text.
        The image format is automatically determined from the file extension.
        
        Args:
            text (str): The Tengwar Unicode text to render
            output_path (str): Path to save the image (e.g., "output.png")
            **kwargs: Additional arguments passed to render_text():
                - padding (int): Padding in pixels
                - background_color (str): Background color
                - text_color (str): Text color
                - size (tuple): Fixed image size
        
        Examples:
            >>> from glaemscribe import transcribe
            >>> from glaemscribe.render import TengwarRenderer
            >>> 
            >>> tengwar = transcribe("Elen síla", mode="quenya")
            >>> renderer = TengwarRenderer(font_size=48)
            >>> renderer.render_to_file(tengwar, "output.png")
            
            >>> # With custom styling
            >>> renderer.render_to_file(
            ...     tengwar,
            ...     "styled.png",
            ...     padding=30,
            ...     background_color="black",
            ...     text_color="gold"
            ... )
        """
        image = self.render_text(text, **kwargs)
        image.save(output_path)
    
    def render_to_bytes(self, text: str, 
                       format: str = "PNG",
                       **kwargs) -> bytes:
        """Render Tengwar text to bytes.
        
        Useful for serving images over HTTP or storing in databases.
        
        Args:
            text (str): The Tengwar Unicode text to render
            format (str): Image format (PNG, JPEG, etc.). Default: "PNG"
            **kwargs: Additional arguments passed to render_text()
            
        Returns:
            bytes: Image data as bytes
        
        Examples:
            >>> renderer = TengwarRenderer()
            >>> image_bytes = renderer.render_to_bytes(tengwar_text)
            >>> # Send via HTTP response
            >>> return Response(image_bytes, mimetype='image/png')
        """
        image = self.render_text(text, **kwargs)
        buffer = io.BytesIO()
        image.save(buffer, format=format)
        return buffer.getvalue()
    
    def render_to_base64(self, text: str,
                        format: str = "PNG", 
                        **kwargs) -> str:
        """Render Tengwar text to base64 string for web embedding.
        
        Args:
            text (str): The Tengwar Unicode text to render
            format (str): Image format (PNG, JPEG, etc.). Default: "PNG"
            **kwargs: Additional arguments passed to render_text()
            
        Returns:
            str: Base64-encoded image string (without data URI prefix)
        
        Examples:
            >>> renderer = TengwarRenderer()
            >>> b64 = renderer.render_to_base64(tengwar_text)
            >>> html = f'<img src="data:image/png;base64,{b64}" />'
        """
        image_bytes = self.render_to_bytes(text, format, **kwargs)
        b64_bytes = base64.b64encode(image_bytes)
        return b64_bytes.decode('ascii')
    
    def render_html_embed(self, text: str, 
                         alt_text: str = "Tengwar text",
                         **kwargs) -> str:
        """Render Tengwar text as embeddable HTML.
        
        Creates a complete HTML img tag with embedded base64 image data.
        Perfect for including Tengwar in web pages without external files.
        
        Args:
            text (str): The Tengwar Unicode text to render
            alt_text (str): Alt text for accessibility. Default: "Tengwar text"
            **kwargs: Additional arguments passed to render_text()
            
        Returns:
            str: HTML img tag with base64-encoded image
        
        Examples:
            >>> renderer = TengwarRenderer(font_size=36)
            >>> html = renderer.render_html_embed(
            ...     tengwar_text,
            ...     alt_text="Elen síla lúmenn' omentielvo"
            ... )
            >>> print(html)
            <img src="data:image/png;base64,..." alt="..." />
        """
        b64_data = self.render_to_base64(text, **kwargs)
        format = kwargs.get('format', 'PNG')
        return f'<img src="data:image/{format.lower()};base64,{b64_data}" alt="{alt_text}" />'


# Convenience functions for quick usage
def render_tengwar(text: str, output_path: str, **kwargs) -> None:
    """Render Tengwar text to file (convenience function).
    
    Quick one-liner for rendering Tengwar text without creating a renderer object.
    Uses default bundled font (FreeMonoTengwar).
    
    Args:
        text (str): The Tengwar Unicode text to render
        output_path (str): Path to save the image
        **kwargs: Additional rendering options (font_size, padding, colors, etc.)
    
    Examples:
        >>> from glaemscribe import transcribe
        >>> from glaemscribe.render import render_tengwar
        >>> 
        >>> tengwar = transcribe("aiya", mode="quenya")
        >>> render_tengwar(tengwar, "output.png", font_size=48)
    """
    renderer = TengwarRenderer()
    renderer.render_to_file(text, output_path, **kwargs)


def tengwar_to_image(text: str, **kwargs) -> Image.Image:
    """Convert Tengwar text to PIL Image (convenience function).
    
    Quick one-liner for getting a PIL Image object without creating a renderer.
    
    Args:
        text (str): The Tengwar Unicode text to render
        **kwargs: Additional rendering options
    
    Returns:
        Image.Image: PIL Image object
    
    Examples:
        >>> from glaemscribe.render import tengwar_to_image
        >>> img = tengwar_to_image(tengwar_text, font_size=36)
        >>> img.show()
    """
    renderer = TengwarRenderer()
    return renderer.render_text(text, **kwargs)


def tengwar_to_base64(text: str, **kwargs) -> str:
    """Convert Tengwar text to base64 string (convenience function).
    
    Quick one-liner for getting base64-encoded image data.
    
    Args:
        text (str): The Tengwar Unicode text to render
        **kwargs: Additional rendering options
    
    Returns:
        str: Base64-encoded image string
    
    Examples:
        >>> from glaemscribe.render import tengwar_to_base64
        >>> b64 = tengwar_to_base64(tengwar_text)
        >>> html = f'<img src="data:image/png;base64,{b64}" />'
    """
    renderer = TengwarRenderer()
    return renderer.render_to_base64(text, **kwargs)
