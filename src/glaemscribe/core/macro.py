"""Macro implementation for Glaemscribe.

This is a port of the Ruby Macro class, supporting macro definitions
and argument handling.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

from .rule_group import CodeBlock
from ..parsers.glaeml import Error


@dataclass
class Macro:
    """A macro definition with arguments and code block.
    
    This mirrors the Ruby Macro class implementation.
    """
    rule_group: Any  # RuleGroup instance
    name: str
    arg_names: List[str]
    root_code_block: CodeBlock = field(default_factory=CodeBlock)
    
    def __post_init__(self):
        """Set up the macro."""
        self.mode = self.rule_group.mode
    
    def __str__(self) -> str:
        """String representation of the macro."""
        return f"<Macro {self.name}({', '.join(self.arg_names)})>"
    
    def traverse_if_tree(self, element, text_procedure, element_procedure):
        """Traverse the macro's if tree structure.
        
        This matches the Ruby traverse_if_tree implementation for macros.
        """
        owner = self
        root_element = element
        rule_group = self.rule_group
        root_code_block = self.root_code_block
        current_parent_code_block = root_code_block
        
        # Import IfTerm from rule_group
        from .rule_group import IfTerm
        
        # Process children of the macro element
        for child in root_element.children:
            if child.is_text():
                # Handle text elements
                text_procedure(current_parent_code_block, child)
            elif child.is_element():
                # Handle element nodes
                if child.name == 'if':
                    cond_attribute = child.args[0] if child.args else ""
                    if_term = IfTerm(current_parent_code_block)
                    current_parent_code_block.add_term(if_term)
                    if_cond = rule_group._create_if_cond_for_if_term(child.line, if_term, cond_attribute)
                    current_parent_code_block = if_cond.child_code_block
                    
                elif child.name == 'elsif':
                    cond_attribute = child.args[0] if child.args else ""
                    if_term = current_parent_code_block.parent_if_cond.parent_if_term if current_parent_code_block.parent_if_cond else None
                    
                    if not if_term:
                        self.mode.errors.append(Error(child.line, "'elsif' without a 'if'."))
                        return
                    
                    if_cond = rule_group._create_if_cond_for_if_term(child.line, if_term, cond_attribute)
                    current_parent_code_block = if_cond.child_code_block
                    
                elif child.name == 'else':
                    if_term = current_parent_code_block.parent_if_cond.parent_if_term if current_parent_code_block.parent_if_cond else None
                    
                    if not if_term:
                        self.mode.errors.append(Error(child.line, "'else' without a 'if'."))
                        return
                    
                    if_cond = rule_group._create_if_cond_for_if_term(child.line, if_term, "true")
                    current_parent_code_block = if_cond.child_code_block
                    
                elif child.name == 'endif':
                    if_term = current_parent_code_block.parent_if_cond.parent_if_term if current_parent_code_block.parent_if_cond else None
                    
                    if not if_term:
                        self.mode.errors.append(Error(child.line, "'endif' without a 'if'."))
                        return
                    
                    current_parent_code_block = if_term.parent_code_block
                    
                else:
                    # Handle other element types (deploy, etc.)
                    element_procedure(current_parent_code_block, child)


@dataclass 
class MacroDeployTerm:
    """A macro deployment with arguments.
    
    This represents a \\deploy command that expands a macro.
    """
    macro: Macro
    line: int
    parent_code_block: CodeBlock
    arg_value_expressions: List[str]
    
    def is_macro_deploy(self) -> bool:
        """Check if this is a macro deploy term."""
        return True
    
    def __str__(self) -> str:
        """String representation of the macro deploy."""
        args_str = ', '.join(self.arg_value_expressions)
        return f"<MacroDeploy {self.macro.name}({args_str})>"
