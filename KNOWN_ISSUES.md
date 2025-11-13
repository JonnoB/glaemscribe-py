# Known Issues - Glaemscribe Python Implementation

## 🐛 **Critical Issues**

### **1. Conditional Macro Deployment Not Working**
**File**: `src/glaemscribe/parsers/mode_parser.py`
**Description**: Macros defined in English Tengwar mode are detected (7 macros) but not deployed
**Root Cause**: Conditional logic in `\if` statements may not be evaluating correctly
**Evidence**: 
- 7 macros detected in `english-tengwar-espeak.glaem`
- 0 cross rules generated (should be many)
- Main deployment: `\deploy serie {L1L} {L1R} {L1L_NASAL} {L1R_NASAL} {_L1L_} {_L1R_}`
**Impact**: Cross rules not activated, advanced transcription fails

### **2. Transcription Options Not Initialized**
**File**: `src/glaemscribe/core/rule_group.py`
**Description**: Conditional expressions like `"pre_consonant_n_with_same_articulation_point == PRE_CONSONANT_N_WITH_SAME_ARTICULATION_POINT_MARK"` may not have default values
**Root Cause**: Mode options may not be properly initialized before finalization
**Evidence**: 169 mode errors related to conditional evaluation
**Impact**: Prevents conditional macro deployment

### **3. Character Parsing Warnings**
**File**: `src/glaemscribe/parsers/glaeml.py`
**Description**: 166 warnings about "No escaped character"
**Root Cause**: `\char` directives in charset files not properly parsed
**Evidence**: Lines 57, 65, 71, 77, 83 in English Tengwar mode
**Impact**: Unicode charset loading may be incomplete

## 🔧 **Medium Priority Issues**

### **4. Empty Target Sheaf Chains in Unicode Rules**
**File**: `src/glaemscribe/core/rule.py`
**Description**: Rules with Unicode variables create empty target chains
**Root Cause**: Unicode variable resolution may happen after sheaf chain creation
**Evidence**: Test shows `Sub-rule: ['\\ue000'] → []`
**Impact**: Unicode transcription may produce incomplete results

### **5. Macro Argument Validation Incomplete**
**File**: `src/glaemscribe/parsers/mode_parser.py`
**Description**: Only basic regex validation for macro argument names
**Root Cause**: Should match Ruby validation exactly
**Evidence**: Current regex: `[0-9A-Z_]+`
**Impact**: May allow invalid argument names

## 🧪 **Test Coverage Gaps**

### **6. No Integration Tests for Cross Rules**
**Description**: Cross rule logic tested in isolation but not end-to-end
**Impact**: Real-world cross rule failures may go undetected

### **7. Unicode Character Round-trip Testing Missing**
**Description**: No tests verify Unicode characters survive full transcription pipeline
**Impact**: Unicode font support may regress

### **8. Macro Recursion Not Tested**
**Description**: No tests for macros that deploy other macros
**Impact**: Complex macro hierarchies may fail

## 📊 **Performance Issues**

### **9. Stack Overflow Protection Inefficient**
**File**: `src/glaemscribe/core/rule_group.py`
**Description`: Uses while loop with manual stack depth counting
**Impact**: May be slow for deeply nested variable references

### **10. Error Accumulation**
**Description**: Errors accumulate in lists without cleanup
**Impact**: Memory usage may grow with large modes

---

## 🎯 **Fix Priority Order**

1. **HIGH**: Conditional macro deployment (unlocks cross rules)
2. **HIGH**: Transcription options initialization
3. **MEDIUM**: Character parsing warnings
4. **MEDIUM**: Unicode rule target chains
5. **LOW**: Improved validation and performance

---

## 🧪 **Test Strategy**

- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end mode loading
- **Regression Tests**: Known issues as failing tests
- **Performance Tests**: Large mode handling

---

*Last Updated: 2025-11-13*
*Status: Macro System Complete, Conditional Deployment Blocked*
