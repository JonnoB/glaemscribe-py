"""Rule implementation for Glaemscribe.

This is a port of the Ruby Rule class, which represents a transcription
rule with source and destination sheaf chains.
"""

from __future__ import annotations
from typing import List, Optional
from .sheaf_chain import SheafChain
from .sheaf_chain_iterator import SheafChainIterator
from .sub_rule import SubRule


class Rule:
    """A transcription rule with source and destination chains.
    
    Rules are processed through SheafChainIterator to generate
    all possible SubRule combinations.
    """
    
    def __init__(self, line: int, rule_group):
        """Initialize a rule.
        
        Args:
            line: Line number where the rule was defined
            rule_group: The parent rule group
        """
        self.line = line
        self.rule_group = rule_group
        self.mode = rule_group.mode
        self.sub_rules: List[SubRule] = []
        self.errors: List[str] = []
        self.cross_schema: Optional[str] = None  # Store cross schema
        
        # These will be set by finalize_rule
        self.src_sheaf_chain: Optional[SheafChain] = None
        self.dst_sheaf_chain: Optional[SheafChain] = None
    
    def finalize(self, cross_schema: Optional[str] = None):
        """Finalize the rule by generating all sub-rules.
        
        Args:
            cross_schema: Optional cross schema for rule processing
        """
        # Store the cross schema
        self.cross_schema = cross_schema
        if self.errors:
            # Add errors to mode
            for error in self.errors:
                self.mode.errors.append(error)
            return
        
        if not self.src_sheaf_chain or not self.dst_sheaf_chain:
            self.errors.append("Rule missing source or destination chain")
            return
        
        # Create iterators for source and destination chains
        srccounter = SheafChainIterator(self.src_sheaf_chain)
        dstcounter = SheafChainIterator(self.dst_sheaf_chain, cross_schema)
        
        if srccounter.errors:
            self.errors.extend(srccounter.errors)
            for error in self.errors:
                self.mode.errors.append(error)
            return
        
        if dstcounter.errors:
            self.errors.extend(dstcounter.errors)
            for error in self.errors:
                self.mode.errors.append(error)
            return
        
        # Check prototypes match
        srcp = srccounter.prototype
        dstp = dstcounter.prototype
        
        if srcp != dstp:
            error_msg = f"Source and destination are not compatible ({srcp} vs {dstp})"
            self.errors.append(error_msg)
            self.mode.errors.append(error_msg)
            return
        
        # Generate all sub-rules (match JS logic exactly)
        try:
            # do-while loop: process current state first, then iterate
            while True:
                # Get all source combinations for current iterator state
                src_combinations = srccounter.combinations()
                
                # Get ONE destination combination (all sources map to same destination)
                dst_combinations = dstcounter.combinations()
                dst_combination = dst_combinations[0] if dst_combinations else []
                
                # Create sub-rules pairing each source with this destination
                for src_combination in src_combinations:
                    self.sub_rules.append(SubRule(self, src_combination, dst_combination))
                
                # Advance destination iterator
                dstcounter.iterate()
                
                # Advance source iterator; if no more sources, stop
                if not srccounter.iterate():
                    break
                    
        except Exception as e:
            self.errors.append(f"Error generating sub-rules: {e}")
            for error in self.errors:
                self.mode.errors.append(error)
    
    def __str__(self) -> str:
        """String representation of the rule."""
        return f"<Rule line={self.line}: {len(self.sub_rules)} sub-rules>"
