# Medium Priority Tasks Analysis: Role and Impact

## 📊 Overview of Medium Priority Features

### **Task 1: Debug Context Functionality** (MEDIUM PRIORITY)

## 🎯 **Role & Purpose**
**Primary Function**: Provides detailed tracing and debugging information during transcription
**Use Case**: Development, troubleshooting, and understanding transcription behavior

## 🔍 **Ruby Implementation Details**
```ruby
class ModeDebugContext
  attr_accessor :preprocessor_output, 
    :processor_pathes, 
    :processor_output, 
    :postprocessor_output,
    :tts_output
    
  def initialize
    @preprocessor_output  = ""
    @processor_pathes     = []
    @processor_output     = []
    @postprocessor_output = ""
    @tts_output = ""
  end
end
```

## 📋 **What It Tracks**
1. **preprocessor_output**: Text preprocessing results
2. **processor_pathes**: Array of `[eaten, tokens, tokens]` - shows each transcription step
3. **processor_output**: Final transcription results
4. **postprocessor_output**: Post-processing results  
5. **tts_output**: Text-to-speech conversion output

## 💡 **Usage Example**
```ruby
debug_context = ModeDebugContext.new
success, result = mode.transcribe(text, charset, debug_context)
# debug_context.processor_pathes contains step-by-step transcription trace
```

## 🎯 **Impact Assessment**
- **Development**: HIGH - Essential for debugging transcription issues
- **User Experience**: MEDIUM - Helps users understand why transcription fails
- **Core Functionality**: LOW - Transcription works without it
- **Implementation Complexity**: MEDIUM - Requires context passing throughout pipeline

---

### **Task 2: Word Boundary Tree vs Breaker** (MEDIUM PRIORITY)

## 🎯 **Role & Purpose**
**Primary Function**: Defines word boundary markers for transcription tree matching
**Use Case**: Ensures correct word boundary handling in pattern matching

## 🔍 **Ruby Constants**
```ruby
WORD_BREAKER        = "|"        # Word separator
WORD_BOUNDARY_LANG  = "_"        # Language boundary  
WORD_BOUNDARY_TREE  = "\u0000"   # Tree boundary (null character)
```

## 🔍 **Ruby Usage**
```ruby
def transcribe_word(word, debug_context)
  word = WORD_BOUNDARY_TREE + word + WORD_BOUNDARY_TREE
  # ... process word
end
```

## 🔍 **Python Current Issue**
```python
# Python (INCORRECT):
word_with_boundaries = self.WORD_BOUNDARY_TREE + word + self.WORD_BREAKER

# Ruby (CORRECT):  
word = WORD_BOUNDARY_TREE + word + WORD_BOUNDARY_TREE
```

## 💡 **Impact Assessment**
- **Correctness**: HIGH - Wrong boundaries could cause transcription errors
- **Compatibility**: HIGH - Must match Ruby exactly for consistent results
- **Implementation Complexity**: LOW - Simple constant fix
- **Risk**: MEDIUM - Could cause subtle transcription bugs

---

### **Task 3: Cross Rule Processing** (MEDIUM PRIORITY)

## 🎯 **Role & Purpose**  
**Primary Function**: Allows complex rule permutations and character reordering
**Use Case**: Advanced transcription scenarios where character positions need to be remapped

## 🔍 **Syntax Example**
```
{V_D_WN}[{L8}] --> 2,1 --> [{_L8_}]{_V_D_WN_}
```
**Meaning**: Source → Cross Schema → Target
- **Source**: `{V_D_WN}[{L8}]`
- **Cross Schema**: `2,1` (reorder positions: second becomes first, first becomes second)
- **Target**: `[{_L8_}]{_V_D_WN_}`

## 🔍 **Ruby Implementation**
```ruby
CROSS_RULE_REGEXP = /^\s*(.*?)\s+-->\s+(#{CROSS_SCHEMA_REGEXP}|#{VAR_NAME_REGEXP}|identity)\s+-->\s+(.+?)\s*$/

# Cross schema processing in SheafChainIterator
if cross_schema
  cross_schema = cross_schema.split(",").map{ |i| i.to_i - 1 }
  # Validate and apply permutation
end
```

## 💡 **Real-World Usage**
Found in multiple mode files:
- `english-tengwar-espeak.glaem` (709 lines)
- `sindarin-tengwar-general_use.glaem`
- `japanese-tengwar.glaem`
- `quenya-sarati.glaem`

## 🎯 **Impact Assessment**
- **Advanced Features**: HIGH - Essential for complex transcription modes
- **Basic Functionality**: LOW - Simple modes work without it
- **Implementation Complexity**: HIGH - Requires full cross-schema validation and permutation logic
- **User Impact**: MEDIUM - Some advanced transcription modes won't work

---

## 📈 **Priority Ranking Recommendation**

### **1. Word Boundary Fix** (HIGHEST Priority)
- **Why**: Critical correctness issue, easy fix
- **Effort**: 1-2 hours
- **Risk**: High if not fixed (subtle bugs)

### **2. Debug Context** (MEDIUM Priority)  
- **Why**: Essential for development, medium complexity
- **Effort**: 4-6 hours
- **Risk**: Low if not implemented

### **3. Cross Rule Processing** (LOWEST Priority)
- **Why**: Advanced feature, high complexity
- **Effort**: 8-12 hours  
- **Risk**: Medium (some modes won't work)

## 🎯 **Implementation Strategy**

### **Phase 1: Quick Win**
Fix word boundary constants - immediate correctness improvement

### **Phase 2: Developer Experience**  
Implement debug context - better debugging and development experience

### **Phase 3: Advanced Features**
Add cross rule processing - complete feature parity for advanced modes

## 📊 **Success Criteria**

### **Word Boundaries**
✅ Python constants match Ruby exactly
✅ Transcription results identical to Ruby/JS
✅ No boundary-related transcription errors

### **Debug Context**  
✅ Complete tracing of transcription steps
✅ All output types tracked (pre, processor, post, TTS)
✅ Easy to use debugging interface

### **Cross Rules**
✅ Complex cross syntax parsed correctly
✅ Character permutations applied properly
✅ Advanced mode files work without errors
