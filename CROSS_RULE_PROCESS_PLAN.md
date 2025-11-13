# Cross Rule Process Implementation Plan

## 🎯 **Objective:**
Implement cross rule processing by following the exact Ruby/JS implementation flow

## 🔍 **Ruby/JS Implementation Flow Analysis:**

### **Step 1: Rule Detection in RuleGroup**
**Ruby Location:** `rule_group.rb` line 252
```ruby
elsif code_line.expression =~ CROSS_RULE_REGEXP
  match         = $1
  cross         = $2
  replacement   = $3
  finalize_rule(code_line.line, match, replacement, cross)
```

**Process:** Detect cross rule syntax → Extract 3 parts → Pass to finalize_rule

### **Step 2: Rule Creation with Cross Schema**
**Ruby Location:** `rule.rb` finalize method
```ruby
def finalize(cross_schema)
  rule.src_sheaf_chain = SheafChain(rule, match, true)
  rule.dst_sheaf_chain = SheafChain(rule, replacement, false)
  # Cross schema passed to iterator creation
end
```

**Process:** Create sheaf chains → Store cross schema → Generate sub-rules

### **Step 3: SheafChainIterator Cross Processing**
**Ruby Location:** `sheaf_chain_iterator.rb` lines 63-82
```ruby
if cross_schema
  cross_schema = cross_schema.split(",").map{ |i| i.to_i - 1 }
  
  # Validation
  it_count = iterable_idxs.count
  ca_count = cross_schema.count
  @errors << "count mismatch" and return if ca_count != it_count
  
  # Permutation validation
  it_identity_array = []
  it_count.times { |i| it_identity_array << i }
  @errors << "invalid permutation" and return if it_identity_array != cross_schema.sort
  
  # Apply permutation
  cross_schema.each_with_index{ |to,from|
    to_permut = iterable_idxs[from]
    permut    = iterable_idxs[to]
    @cross_array[to_permut] = permut
  }
end
```

**Process:** Parse schema → Validate → Apply permutation to cross_array

### **Step 4: Sub-Rule Generation with Permutation**
**Ruby Location:** `sheaf_chain_iterator.rb` iterate method
```ruby
def iterate
  # Apply cross permutation to current combination
  final_combination = []
  @cross_array.each_with_index{ |to_idx, from_idx|
    final_combination[to_idx] = @current_combination[from_idx]
  }
  return final_combination
end
```

**Process:** Use cross_array to reorder each generated combination

## 📋 **Python Implementation Process Steps:**

### **Process Step 1: Update RuleGroup Regex and Detection**

#### **1.1 Add Cross Rule Patterns**
```python
# In rule_group.py - match Ruby exactly
CROSS_SCHEMA_REGEXP = re.compile(r'[0-9]+(\s*,\s*[0-9]+)*')
CROSS_RULE_REGEXP = re.compile(r'^\s*(.*?)\s+-->\s+(?:[0-9]+(?:\s*,\s*[0-9]+)*|[A-Z_]+|identity)\s+-->\s+(.+?)\s*$')
```

#### **1.2 Update finalize_code_line()**
```python
# In RuleGroup.finalize_code_line() - follow Ruby flow
elif code_line.expression =~ self.CROSS_RULE_REGEXP:
    match = self.CROSS_RULE_REGEXP.match(code_line.expression)
    source = match.group(1)
    cross_schema = match.group(2)
    replacement = match.group(3)
    
    self.finalize_rule(code_line.line, source, replacement, cross_schema)
```

### **Process Step 2: Update Rule.finalize() Method**

#### **2.1 Accept Cross Schema Parameter**
```python
# In rule.py - modify finalize() signature
def finalize(self, cross_schema: Optional[str] = None):
    """Finalize rule with optional cross schema."""
    # Create sheaf chains (existing code)
    self.src_sheaf_chain = SheafChain(self, self.src_expression, True)
    self.dst_sheaf_chain = SheafChain(self, self.dst_expression, False)
    
    # Generate sub-rules with cross schema
    self._generate_sub_rules(cross_schema)
```

#### **2.2 Pass Cross Schema to Iterator**
```python
# In rule.py - _generate_sub_rules() method
def _generate_sub_rules(self, cross_schema: Optional[str] = None):
    """Generate sub-rules using cross schema if provided."""
    iterator = SheafChainIterator(
        self.src_sheaf_chain, 
        self.dst_sheaf_chain, 
        cross_schema  # Pass cross schema here
    )
    
    # Generate all combinations (existing code)
    while iterator.iterate():
        src_combo = iterator.get_src_combination()
        dst_combo = iterator.get_dst_combination()
        self.sub_rules.append(SubRule(src_combo, dst_combo))
```

### **Process Step 3: Implement SheafChainIterator Cross Logic**

#### **3.1 Update Constructor to Accept Cross Schema**
```python
# In sheaf_chain_iterator.py
def __init__(self, src_sheaf_chain: SheafChain, dst_sheaf_chain: SheafChain, cross_schema: Optional[str] = None):
    # Existing initialization...
    self.cross_schema = cross_schema
    self.cross_array = list(range(len(self.iterable_idxs)))  # Identity by default
    
    # Process cross schema if provided
    if cross_schema:
        self._process_cross_schema(cross_schema)
```

#### **3.2 Implement _process_cross_schema()**
```python
# In sheaf_chain_iterator.py - match Ruby logic exactly
def _process_cross_schema(self, cross_schema: str):
    """Process cross schema following Ruby implementation."""
    # Handle identity keyword
    if cross_schema == "identity":
        return  # Use default identity permutation
    
    # Handle variable substitution (later phase)
    if cross_schema.startswith("{") and cross_schema.endswith("}"):
        # TODO: Implement variable resolution
        pass
    
    # Parse numeric schema: "2,1" -> [1, 0] (0-based)
    try:
        schema_array = [int(x.strip()) - 1 for x in cross_schema.split(",")]
    except ValueError:
        self.errors.append(f"Invalid cross schema: {cross_schema}")
        return
    
    # Validation: count must match
    it_count = len(self.iterable_idxs)
    ca_count = len(schema_array)
    if ca_count != it_count:
        self.errors.append(f"{it_count} linkable sheaves found, but {ca_count} elements in cross rule")
        return
    
    # Validation: must be proper permutation
    expected = list(range(it_count))
    if sorted(schema_array) != expected:
        self.errors.append("Cross rule schema should be a permutation of the identity")
        return
    
    # Apply permutation to cross_array
    for to_idx, from_idx in enumerate(schema_array):
        to_permut = self.iterable_idxs[from_idx]
        permut = self.iterable_idxs[to_idx]
        self.cross_array[to_permut] = permut
```

#### **3.3 Update Combination Generation**
```python
# In sheaf_chain_iterator.py - modify get_src_combination()
def get_src_combination(self) -> List[str]:
    """Get source combination with cross permutation applied."""
    if not self.cross_schema:
        # No cross schema - return normal combination
        return self._build_normal_combination()
    
    # Apply cross permutation
    final_combination = [''] * len(self.current_combination)
    for to_idx, from_idx in enumerate(self.cross_array):
        final_combination[to_idx] = self.current_combination[from_idx]
    
    return final_combination
```

### **Process Step 4: Variable Resolution (Phase 2)**

#### **4.1 Variable Schema Detection**
```python
# In sheaf_chain_iterator.py - extend _process_cross_schema()
def _resolve_variable_schema(self, var_name: str) -> str:
    """Resolve variable-based cross schema."""
    # Get variable from rule's mode
    if hasattr(self.sheaf_chain, 'rule') and hasattr(self.sheaf_chain.rule, 'mode'):
        rule_group = self.sheaf_chain.rule.mode.rule_groups
        # Find variable in all rule groups
        for rg in rule_group.values():
            if var_name in rg.vars:
                return rg.vars[var_name].value
    
    self.errors.append(f"Cross schema variable not found: {var_name}")
    return None
```

## 🔄 **Complete Data Flow:**

```
1. RuleGroup.finalize_code_line()
   └── Detects "source --> 2,1 --> target" syntax
       └── Calls finalize_rule(line, source, target, "2,1")

2. Rule.finalize(cross_schema="2,1")
   └── Creates src_sheaf_chain and dst_sheaf_chain
       └── Creates SheafChainIterator(src, dst, "2,1")

3. SheafChainIterator.__init__(cross_schema="2,1")
   └── Parses "2,1" -> [1, 0]
   └── Validates it's a proper permutation
   └── Sets cross_array = [1, 0] (swap positions)

4. Iterator.iterate()
   └── Generates normal combination
   └── Applies cross_array permutation
   └── Returns reordered combination

5. Rule generates SubRule with reordered combinations
```

## 🧪 **Verification Process:**

### **Test Case 1: Simple Cross Rule**
```
Input:  {V_D_WN}[{L8}] --> 2,1 --> [{_L8_}]{_V_D_WN_}
Expected: Vowel+Consonant combinations become Consonant+Vowel
```

### **Test Case 2: Variable Cross Rule**
```
Input:  {V_D_WN}[{ARG_SL}] --> {__LWSX__} --> target
Expected: Resolve {__LWSX__} variable and apply
```

### **Test Case 3: Invalid Schema**
```
Input:  {A}{B} --> 2,2,1 --> target
Expected: Error - invalid permutation (duplicate 2)
```

## 🎯 **Implementation Priority:**

1. **Core Logic** - Steps 1-3 (numeric cross schemas)
2. **Variable Resolution** - Step 4 (variable-based schemas)  
3. **Error Handling** - Comprehensive validation and messages
4. **Testing** - End-to-end verification with real modes

This process plan follows the exact Ruby/JS implementation flow, ensuring 100% compatibility and behavior matching.
