#!/usr/bin/env python3
"""Render the Namárië poem as a PNG image using Tengwar Unicode characters."""

import json
import os
from PIL import Image, ImageDraw, ImageFont
from src.glaemscribe.parsers.mode_parser import ModeParser

def load_poem_outputs():
    """Load the poem transcription outputs."""
    with open('poem_transcription_canonical.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def render_poem():
    """Render the poem as PNG."""
    # Load the transcribed poem
    poem_data = load_poem_outputs()
    
    # Create image
    width = 800
    height = 600
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to load FreeMonoTengwar font
    try:
        font = ImageFont.truetype('src/glaemscribe/fonts/FreeMonoTengwar.ttf', 20)
        title_font = ImageFont.truetype('src/glaemscribe/fonts/FreeMonoTengwar.ttf', 24)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()
    
    # Draw title
    draw.text((50, 30), "Namárië (Galadriel's Lament)", font=title_font, fill='black')
    draw.text((50, 60), "Transcribed using Glaemscribe Python", font=font, fill='gray')
    
    # Draw the poem lines
    y_position = 100
    for i, line_data in enumerate(poem_data):
        # Draw line number and original text
        line_text = f"{i+1}. {line_data['line']}"
        draw.text((50, y_position), line_text, font=font, fill='black')
        
        # Draw Tengwar transcription
        tengwar_text = line_data['output']
        draw.text((50, y_position + 25), tengwar_text, font=font, fill='blue')
        
        y_position += 60
    
    # Add footer
    draw.text((50, height - 40), "Unicode Tengwar (Private Use Area U+E000+)", font=font, fill='gray')
    
    # Ensure data directory exists
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(output_dir, exist_ok=True)

    # Save the image
    out1 = os.path.join(output_dir, 'namarie_poem_transcription.png')
    img.save(out1)
    print(f"Poem rendered as '{out1}'")
    
    # Also create a version with just the Tengwar
    img2 = Image.new('RGB', (width, height), color='white')
    draw2 = ImageDraw.Draw(img2)
    
    draw2.text((50, 30), "Namárië - Tengwar Transcription", font=title_font, fill='black')
    y_position = 80
    for i, line_data in enumerate(poem_data):
        tengwar_text = line_data['output']
        draw2.text((50, y_position), tengwar_text, font=font, fill='black')
        y_position += 50
    
    draw2.text((50, height - 40), "FreeMonoTengwar charset - Unicode PUA", font=font, fill='gray')
    out2 = os.path.join(output_dir, 'namarie_poem_tengwar_only.png')
    img2.save(out2)
    print(f"Tengwar-only version saved as '{out2}'")

if __name__ == "__main__":
    render_poem()
