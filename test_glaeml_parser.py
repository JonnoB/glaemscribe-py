#!/usr/bin/env python3
"""Test the Glaeml parser."""

from src.glaemscribe.parsers.glaeml import Parser, NodeType

def test_simple_parsing():
    """Test basic parsing functionality."""
    
    # Simple test content
    content = r"""
\version 1.0.0
\char 0x61 TINCO
\char 0x62 ANDO
"""
    
    parser = Parser()
    doc = parser.parse(content)
    
    print("Parsing test:")
    print(f"Errors: {doc.errors}")
    
    if doc.root_node:
        print(f"Root node has {len(doc.root_node.children)} children")
        
        # Find all char nodes
        char_nodes = doc.root_node.gpath("char")
        print(f"Found {len(char_nodes)} char nodes:")
        
        for node in char_nodes:
            print(f"  Line {node.line}: {node.name} {node.args}")
    
    return len(doc.errors) == 0

def test_real_charset():
    """Test parsing a real charset file."""
    
    try:
        with open("/home/jonno/glaemscribe-py/resources/glaemresources/charsets/tengwar_ds_annatar.cst", "r") as f:
            content = f.read()
        
        parser = Parser()
        doc = parser.parse(content)
        
        print(f"\nReal charset parsing:")
        print(f"Total lines: {len(content.split())}")
        print(f"Errors: {len(doc.errors)}")
        
        if doc.root_node:
            char_nodes = doc.root_node.gpath("char")
            print(f"Found {len(char_nodes)} character definitions")
            
            # Show first few
            for i, node in enumerate(char_nodes[:5]):
                print(f"  {node.name}: {node.args}")
            
            # Check for virtual characters
            virtual_nodes = doc.root_node.gpath("virtual")
            print(f"Found {len(virtual_nodes)} virtual character definitions")
            
            # Show first virtual char
            if virtual_nodes:
                v = virtual_nodes[0]
                print(f"  First virtual: {v.name}")
                class_nodes = v.gpath("class")
                for c in class_nodes[:3]:
                    print(f"    Class {c.name}: {c.args}")
        
        return len(doc.errors) == 0
        
    except Exception as e:
        print(f"Error reading charset file: {e}")
        return False

if __name__ == "__main__":
    success1 = test_simple_parsing()
    success2 = test_real_charset()
    
    if success1 and success2:
        print("\n✓ All Glaeml parser tests passed!")
    else:
        print("\n✗ Some tests failed!")
