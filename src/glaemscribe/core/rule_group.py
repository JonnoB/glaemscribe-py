"""Rule group implementation for Glaemscribe.

This is a port of the Ruby RuleGroup class, supporting variables,
rules, and conditional logic.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union, Any, Pattern
import re

from ..parsers.glaeml import Error


@dataclass
class RuleGroupVar:
    """A variable in a rule group."""
    name: str
    value: str
    is_pointer: bool = False
    
    def is_pointer_var(self) -> bool:
        """Check if this is a pointer variable."""
        return self.is_pointer


class CodeBlock:
    """A block of code with conditional logic."""
    
    def __init__(self):
        """Initialize a code block."""
        self.terms: List[Union[IfCond, CodeLine, Any]] = []
        self.parent_if_cond: Optional[IfCond] = None
    
    def add_term(self, term: Union[IfCond, CodeLine, Any]):
        """Add a term to this code block."""
        self.terms.append(term)


@dataclass
class CodeLine:
    """A single line of code in a rule group."""
    expression: str
    line: int
    
    def __post_init__(self):
        """Clean up the expression."""
        self.expression = self.expression.strip()


@dataclass
class IfCond:
    """A conditional statement in a rule group."""
    line: int
    expression: str
    parent_if_term: Optional[IfCond] = None
    child_code_block: Optional[CodeBlock] = field(default_factory=CodeBlock)
    
    def __post_init__(self):
        """Set up the child code block parent."""
        if self.child_code_block:
            self.child_code_block.parent_if_cond = self


class RuleGroup:
    """A group of transcription rules with variables and conditions."""
    
    # Regular expressions for parsing
    VAR_NAME_REGEXP: Pattern = re.compile(r'{([0-9A-Z_]+)}')
    UNICODE_VAR_NAME_REGEXP_IN: Pattern = re.compile(r'^UNI_([0-9A-F]+)$')
    UNICODE_VAR_NAME_REGEXP_OUT: Pattern = re.compile(r'{UNI_([0-9A-F]+)}')
    
    VAR_DECL_REGEXP: Pattern = re.compile(r'^\s*{([0-9A-Z_]+)}\s+===\s+(.+?)\s*$')
    POINTER_VAR_DECL_REGEXP: Pattern = re.compile(r'^\s*{([0-9A-Z_]+)}\s+<=>\s+(.+?)\s*$')
    RULE_REGEXP: Pattern = re.compile(r'^\s*(.*?)\s+-->\s+(.+?)\s*$')
    
    def __init__(self, mode, name: str):
        """Initialize a rule group."""
        self.name: str = name
        self.mode = mode
        self.vars: Dict[str, RuleGroupVar] = {}
        self.macros: Dict[str, Any] = {}
        self.root_code_block: CodeBlock = CodeBlock()
        self.rules: List[Any] = []  # Will be populated after finalization
    
    def add_var(self, var_name: str, value: str, is_pointer: bool = False):
        """Add a variable to the rule group."""
        self.vars[var_name] = RuleGroupVar(var_name, value, is_pointer)
    
    def apply_vars(self, line: int, string: str, allow_unicode_vars: bool = False) -> Optional[str]:
        """Replace all variables in an expression."""
        ret = string
        stack_depth = 0
        had_replacements = True
        
        while had_replacements:
            had_replacements = False
            ret = re.sub(self.VAR_NAME_REGEXP, lambda match: self._replace_var(match, line, string, allow_unicode_vars, had_replacements), ret)
        
        return ret
    
    def _replace_var(self, match, line: int, string: str, allow_unicode_vars: bool, had_replacements: bool) -> str:
        """Replace a single variable."""
        vname = match.group(1)
        cap_var = match.group(0)
        
        v = self.vars.get(vname)
        if not v:
            if self.UNICODE_VAR_NAME_REGEXP_IN.match(vname):
                # Unicode variable
                if allow_unicode_vars:
                    return cap_var
                else:
                    self.mode.errors.append(Error(line, f"In expression: {string}: making wrong use of unicode variable: {cap_var}. Unicode vars can only be used in source members of a rule or in the definition of another variable."))
                    return cap_var
            else:
                self.mode.errors.append(Error(line, f"In expression: {string}: failed to evaluate variable: {cap_var}."))
                return cap_var
        else:
            # Count replacements on non-unicode vars
            had_replacements = True
            return v.value
    
    def finalize(self, trans_options: Dict[str, Any]):
        """Finalize the rule group with given transcription options."""
        # TODO: Implement finalization logic
        # This would evaluate all the conditional logic and build the final rules
        pass
    
    def __str__(self) -> str:
        """String representation of the rule group."""
        return f"<RuleGroup {self.name}: {len(self.vars)} vars, {len(self.rules)} rules>"
