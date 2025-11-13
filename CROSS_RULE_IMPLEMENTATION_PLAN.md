# Cross Rule Processing Implementation Plan

## 🎯 **Objective:**
Enable complex character reordering for English/Japanese to Tengwar transcription modes

## 📊 **Current Status:**
- ✅ Core Rule/SubRule/SheafChain pipeline working
- ✅ Basic transcription functioning
- ✅ Debug context implemented
- ❌ Cross rule processing missing (blocks advanced modes)

## 🔍 **Cross Rule Examples to Support:**

### **English Tengwar Examples:**
```
{V_D_WN}[{L8}] --> 2,1 --> [{_L8_}]{_V_D_WN_}
{V_D_WN}[{L8_NASAL}] --> 2,1 --> [{_L8_}]{NASAL}{_V_D_WN_}
{V_D_WN}[{L9}] --> 2,1 --> [{_L9_}]{_V_D_WN_}
```

### **Variable-Based Examples:**
```
{V_D_WN}[{ARG_SL}] --> {__LWSX__} --> [{_ARG_SL_}]{_V_D_WN_}{_LWS_}
```

## 🏗️ **Implementation Architecture:**

### **Phase 1: Rule Parsing Enhancement**
**Goal**: Recognize and parse cross rule syntax

#### **1.1 Add Cross Rule Regex Patterns**
```python
class RegexPatterns:
    # Existing patterns...
    CROSS_SCHEMA_REGEXP = re.compile(r'[0-9]+(\s*,\s*[0-9]+)*')
    CROSS_RULE_REGEXP = re.compile(r'^\s*(.*?)\s+-->\s+(?:[0-9]+(?:\s*,\s*[0-9]+)*|[A-Z_]+|identity)\s+-->\s+(.+?)\s*$')
```

#### **1.2 Update RuleGroup.finalize_code_line()**
- Detect cross rule syntax vs normal rule syntax
- Extract cross schema parameter
- Pass to finalize_rule() method

#### **1.3 Update RuleGroup.finalize_rule()**
- Accept cross_schema parameter
- Pass to Rule.finalize() method

### **Phase 2: SheafChainIterator Enhancement**
**Goal**: Implement permutation logic for cross schemas

#### **2.1 Add Cross Schema Processing**
```python
def _construct_cross_array(self, cross_schema: str, iterable_idxs: List[int], prototype_array: List[int]):
    """Process cross schema and create permutation mapping."""
```

#### **2.2 Implement Validation Logic**
- Verify schema length matches iterable count
- Validate schema is proper permutation (1,2,3... in some order)
- Generate meaningful error messages

#### **2.3 Apply Permutation Logic**
- Map source positions to target positions
- Modify prototype array based on cross schema
- Update cross_array for iteration

### **Phase 3: Variable Resolution**
**Goal**: Support variable-based cross schemas

#### **3.1 Variable Schema Detection**
- Recognize `{VAR_NAME}` patterns in cross schema
- Resolve variables from RuleGroup.vars
- Handle recursive variable definitions

#### **3.2 Identity Schema Support**
- Handle `identity` keyword (no reordering)
- Default to 1,2,3... when no schema specified

### **Phase 4: Integration & Testing**
**Goal**: Ensure end-to-end functionality

#### **4.1 End-to-End Testing**
- Test with actual English Tengwar mode files
- Verify complex cross rules work correctly
- Compare output with Ruby/JS implementation

#### **4.2 Error Handling**
- Comprehensive error messages for invalid schemas
- Graceful fallback for malformed cross rules
- Debug context integration for cross rule tracing

## 📋 **Detailed Implementation Steps:**

### **Step 1: Regex Patterns (Day 1)**
```python
# In rule_group.py
CROSS_SCHEMA_REGEXP = re.compile(r'[0-9]+(\s*,\s*[0-9]+)*')
CROSS_RULE_REGEXP = re.compile(r'^\s*(.*?)\s+-->\s+(?:[0-9]+(?:\s*,\s*[0-9]+)*|[A-Z_]+|identity)\s+-->\s+(.+?)\s*$')
```

### **Step 2: Rule Detection (Day 1-2)**
```python
# In RuleGroup.finalize_code_line()
if code_line.expression =~ CROSS_RULE_REGEXP:
    source = $1
    cross_schema = $2  
    target = $3
    self.finalize_rule(code_line.line, source, target, cross_schema)
elif code_line.expression =~ RULE_REGEXP:
    # Normal rule processing
```

### **Step 3: SheafChainIterator Core (Day 2-3)**
```python
# In SheafChainIterator.__init__()
def _construct_cross_array(self, cross_schema, iterable_idxs, prototype_array):
    if not cross_schema:
        return
    
    # Parse cross schema
    if cross_schema == "identity":
        cross_schema = "1,2,3,..."  # Generate identity
    elif cross_schema.startswith("{") and cross_schema.endswith("}"):
        # Variable resolution
        var_name = cross_schema[1:-1]
        cross_schema = self.sheaf_chain.mode.rule_groups.get_var(var_name)
    
    # Convert to array of indices (0-based)
    schema_array = [int(x.strip()) - 1 for x in cross_schema.split(",")]
    
    # Validation
    if len(schema_array) != len(iterable_idxs):
        self.errors.append(f"Schema length mismatch")
        return
    
    # Verify permutation
    expected = list(range(len(iterable_idxs)))
    if sorted(schema_array) != expected:
        self.errors.append(f"Invalid permutation: {cross_schema}")
        return
    
    # Apply permutation
    for to_idx, from_idx in enumerate(schema_array):
        to_permut = iterable_idxs[from_idx]
        permut = iterable_idxs[to_idx]
        self.cross_array[to_permut] = permut
```

### **Step 4: Integration Testing (Day 3-4)**
```python
# Test cases to implement:
def test_simple_cross_rule():
    # Test {V_D_WN}[{L8}] --> 2,1 --> [{_L8_}]{_V_D_WN_}
    
def test_variable_cross_rule():
    # Test {V_D_WN}[{ARG_SL}] --> {__LWSX__} --> ...
    
def test_identity_cross_rule():
    # Test normal rules (no cross schema)
    
def test_invalid_cross_rule():
    # Test error handling for bad schemas
```

## 🎯 **Success Criteria:**

### **Functional Requirements:**
✅ Parse cross rule syntax correctly
✅ Apply numeric permutations (2,1, 3,1,2, etc.)
✅ Resolve variable-based cross schemas
✅ Handle identity schema properly
✅ Validate permutations and report errors

### **Compatibility Requirements:**
✅ English Tengwar modes work without errors
✅ Japanese Tengwar modes work without errors
✅ Output matches Ruby/JS implementation exactly
✅ All existing functionality preserved

### **Performance Requirements:**
✅ No performance regression for normal rules
✅ Cross rules process efficiently
✅ Memory usage remains reasonable

## 🚀 **Implementation Timeline:**

### **Day 1: Foundation**
- Add regex patterns
- Update rule parsing logic
- Basic cross rule detection

### **Day 2: Core Logic**  
- Implement SheafChainIterator permutation
- Add validation logic
- Handle numeric schemas

### **Day 3: Advanced Features**
- Variable resolution
- Identity schema support
- Error handling

### **Day 4: Testing & Polish**
- End-to-end testing with real modes
- Performance optimization
- Debug context integration

## 🧪 **Test Strategy:**

### **Unit Tests:**
- Regex pattern matching
- Schema validation logic
- Permutation calculation

### **Integration Tests:**
- Full cross rule processing
- Variable resolution
- Error propagation

### **Compatibility Tests:**
- English Tengwar mode files
- Japanese Tengwar mode files
- Output comparison with Ruby/JS

## 📊 **Risk Assessment:**

### **High Risk:**
- Complex permutation logic in SheafChainIterator
- Variable resolution edge cases

### **Medium Risk:**
- Regex pattern accuracy
- Error message quality

### **Low Risk:**
- Integration with existing pipeline
- Performance impact

## 🎯 **Final Goal:**

Enable users to transcribe English and Japanese text to Tengwar writing systems with full fidelity to the original Glaemscribe implementation, opening up the most popular use cases for the Python version.
