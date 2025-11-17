# Known Issues & TODO List - Glaemscribe Python Implementation

## 🚨 Current Issues

### Real-World Test Failures
**Priority**: Medium  
**Files**: `tests/test_real_world.py`  
**Description**: 2 real-world tests fail due to expecting exact string match with font encoding  
**Impact**: Tests expect DS font codes but Python outputs Unicode PUA characters  
**Status**: These are expected failures - the difference is intentional (Unicode vs font encoding)

### Missing Tengwar Characters
**Priority**: Low  
**Files**: `src/glaemscribe/parsers/tengwar_font_mapping.py`  
**Description**: Some rare Tengwar characters may not have Unicode mappings  
**Impact**: Edge cases in transcription might output fallback characters  
**Status**: Core characters are mapped, rare variants may need adding

### Pytest Mark Warnings
**Priority**: Low  
**Files**: Various test files  
**Description**: Custom pytest marks (regression, known_issue, etc.) need registration  
**Impact**: Warnings in test output, but tests run fine  
**Status**: Cosmetic issue - tests work correctly

### Font Rendering / "Tofu" Problem ✅ RESOLVED
**Priority**: Low (documentation only)  
**Files**: `src/glaemscribe/render/` (implemented)  
**Description**: The library outputs Unicode PUA characters which appeared as boxes/tofu (□) unless users had Tengwar fonts installed.  
**Status**: **RESOLVED** - Fixed Unicode mapping to use FTF/Everson standard and implemented PIL-based rendering with working fonts.

**Solution Implemented**:
- ✅ **Fixed Unicode mapping**: Switched from custom mapping to **FTF/Everson Unicode standard**
- ✅ **Font compatibility**: Now works with **Eldamar font** (fully supports FTF/Everson mapping)
- ✅ **Font bundling**: AGPL-3.0 Tengwar fonts included in `src/glaemscribe/render/fonts/`
- ✅ **PIL renderer**: `TengwarRenderer` class with PNG, base64, and HTML output
- ✅ **Working font**: `eldamar` (default) - only font with full FTF/Everson support
- ✅ **Easy API**: Simple rendering with proper Tengwar characters

**Usage**:
```python
from glaemscribe.render import TengwarRenderer
from glaemscribe import transcribe

# Transcribe and render (now works out of the box!)
result = transcribe("Elen síla", "quenya-classical")
renderer = TengwarRenderer("eldamar")  # Only font with FTF/Everson support
renderer.render_to_file(result, "tengwar.png", font_size=32)
# Result: Beautiful Tengwar characters, no more tofu!
```

**Technical Details**:
- **Unicode Standard**: FTF/Everson (U+E000+ range used by modern fonts)
- **Font Codes**: DS charset codes → FTF/Everson Unicode mapping
- **Working Font**: Eldamar (120K, full FTF/Everson support)
- **Legacy Fonts**: Annatar (empty glyphs), Parmaite (reports tofu), others untested

**Remaining work**: Add to main API documentation

### Test Performance
**Priority**: Low  
**Files**: `tests/conftest.py`, `tests/test_transcription_core.py`, `tests/test_transcription_validation.py`, `tests/test_transcription_comparison.py`  
**Description**: Original test suite took ~60 seconds due to repeated mode parsing. After introducing session-scoped fixtures and consolidating tests by function, the consolidated suite now runs in roughly 10–12 seconds on the current hardware.  
**Impact**: Development feedback loop is acceptable; further gains would be nice-to-have rather than essential.  
**Status**: Addressed for normal development use. Remaining performance work is focused on very large texts and potential CI parallelisation.  
**Notes**: Mode loading is still the dominant cost; fixtures ensure it happens only a small number of times per session instead of once per test.

## 📝 TODO List

### High Priority
- [x] **Add font rendering module** to solve "tofu" problem - users need a way to see Tengwar characters without installing fonts manually
  - ✅ **Fixed Unicode mapping**: Switched to FTF/Everson standard for font compatibility
  - ✅ **Implemented**: `src/glaemscribe/render/` with PIL-based rendering
  - ✅ **Working font**: Eldamar font (120K) fully supports FTF/Everson transcriptions
  - ✅ **Usage examples**: `demo_font_rendering.py` shows working implementation
  - 📝 **Documentation needed**: Add to main API docs
- [ ] **Update real-world tests** to use structural validation instead of exact string matching
- [ ] **Add CLI interface** for command-line transcription (matching original glaemscribe binary)
- [ ] **Performance profiling** for large text transcription

### Medium Priority
- [ ] **Add more test cases** for edge cases and complex virtual character scenarios
- [ ] **Document API** with proper docstrings and examples
- [ ] **Add support for custom charsets** and user-defined modes
- [ ] **Optimize test performance** - reduce test suite from 60s to under 30s
- [ ] **Profile test execution** to identify bottlenecks in mode loading

### Low Priority
- [ ] **Register custom pytest marks** to eliminate warnings
- [ ] **Add type hints** throughout codebase
- [ ] **Create Python package** for pip installation
- [ ] **Add integration tests** with real Tolkien texts

## 🐛 Bug Reports

### Remaining Test Failures
Most tests pass; the remaining failures fall into two broad categories:
- **Expectation mismatches** where legacy tests assume font-encoding outputs rather than Unicode PUA/Plane 14 characters.
- **Coverage gaps** around rare Tengwar characters and edge-case sequences that have not yet appeared in real-world usage.

These are being tracked and adjusted as the Unicode-focused design stabilises.

## 🔄 Recently Resolved

### Virtual Character Resolution (2025-11-13)
- ✅ Implemented 2-pass virtual character resolution algorithm
- ✅ Added sequence expansion and character swap support
- ✅ Fixed virtual character lookup tables and trigger state management

### Unicode Output (2025-11-13)
- ✅ Complete Unicode PUA character mapping
- ✅ Font-to-Unicode conversion for all common Tengwar characters
- ✅ Unicode normalization for accented characters

### Test Suite Cleanup (2025-11-13)
- ✅ Removed 40+ old test files
- ✅ Created proper pytest test structure
- ✅ Added JavaScript parity validation tests

## 📊 Current Status

**Implementation**: ✅ Stable and usable for real-world Tengwar transcription  
**Tests**: Majority passing; remaining failures are known and documented above  
**Output Strategy**: Unicode PUA + Plane 14 PUA (modern Unicode-centric design, not font encoding)  
**Performance**: Consolidated core/validation/comparison suites complete in ~10–12 seconds locally

## 🎯 Next Milestones

1. **CLI Tool** - Command-line interface matching original functionality
2. **Package Distribution** - PyPI package for easy installation
3. **Documentation** - Complete API documentation and examples

---

*Last Updated: 2025-11-14*  
*Focus: Active issues and TODOs, not accomplishments*
