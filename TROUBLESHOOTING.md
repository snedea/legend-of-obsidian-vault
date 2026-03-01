# TROUBLESHOOTING.md - Debugging Guide

## Table of Contents

- [Combat Narrative System](#combat-narrative-system)
- [Working Directory Issues](#working-directory-issues)
- [AI Integration Problems](#ai-integration-problems)
- [Import and Module Errors](#import-and-module-errors)
- [Performance Issues](#performance-issues)
- [Common Error Messages](#common-error-messages)

## Combat Narrative System

### Overview: The Three-Stage Narrative Pipeline

Combat narratives in LOV flow through three distinct stages, each in a separate file:

1. **Generation** (AI or Template-based) → `brainbot.py` or `obsidian.py`
2. **Storage** → `Enemy.encounter_narrative` attribute
3. **Display Rendering** → `screens/combat/combat.py`

**CRITICAL**: Most narrative issues stem from stage 3 (display), not generation!

### Stage 1: Narrative Generation

#### AI Generation Path (Primary)
**File**: `brainbot.py`
**Function**: `generate_enemy_from_note()` (lines 240-329)
**Key Parameters**:
- Line 282: `max_tokens=400` - Controls AI output length (400 tokens ≈ 300-400 words)
- Line 273: Prompt instructs "3-4 sentence narrative"
- Line 286: Stores result in `encounter_narrative` field

```python
# brainbot.py:282
response = self.generate_text(prompt, max_tokens=400, generation_type="enemy")
```

**When to modify**: Only if AI generates too-short content (rare)

#### Template Generation Path (Fallback)
**File**: `obsidian.py`
**Function**: `_generate_dynamic_encounter_narrative()` (lines 891-1024)
**Key Features**:
- Line 893: Reads up to 300 chars of note content for keyword detection
- Lines 929-990: Content-aware templates (code, meetings, recipes, etc.)
- Lines 995-1024: Extension logic ensures 600+ character minimum

```python
# obsidian.py:995-1024 - Ensures rich narratives
if len(narrative) < 600:
    extensions = []
    # Adds atmospheric details from note content
    if details['numbers'] and len(details['numbers']) > 1:
        extra_nums = ', '.join(str(n) for n in details['numbers'][1:3])
        extensions.append(f"Additional mystical frequencies {extra_nums}...")
```

**When to modify**: If fallback narratives feel generic or too short

### Stage 2: Storage
**Location**: `game_data.py` - `Enemy` dataclass
**Field**: `encounter_narrative: str = ""`

This stage is just data storage - no processing happens here.

### Stage 3: Display Rendering (MOST COMMON ISSUE)

**File**: `screens/combat/combat.py`
**Critical Line**: **Line 47**
```python
narrative_lines = self._wrap_narrative_text_smart(self.enemy.encounter_narrative, 75, max_lines=8)
```

**Parameters**:
- `75` = character width per line
- `max_lines=8` = **DISPLAY LIMIT** (recently fixed from 4 → 8)

**Function**: `_wrap_narrative_text_smart()` (lines 151-195)
- Line 173-174: Stops processing at `max_lines - 1`
- Line 181-187: Adds "..." ellipsis when content exceeds limit
- Line 189-191: Pads with empty lines to ensure consistent height

### Critical Lesson Learned: October 2025 Multi-Hour Debugging Session

#### The Problem
User reported: "I see only 4 lines with '...' truncation, narratives aren't long enough!"

#### The Wrong Path (2+ hours wasted)
1. ❌ Edited `ai_engine.py` in `/Users/name/homelab/ai-red-dragon` (WRONG DIRECTORY)
2. ❌ Increased `max_tokens` from 150 → 800 in wrong files
3. ❌ Added extension logic to wrong `obsidian.py`
4. ❌ Blamed cache, AI token limits, stop sequences
5. ❌ Added debug logging that never appeared (wrong directory!)

**Root Cause Discovery**:
- User ran game from `/Users/name/homelab/legend_of_obsidian`
- All edits were in `/Users/name/homelab/ai-red-dragon` (wrong project!)
- Changes never took effect because they were in the wrong codebase

#### The Actual Root Cause
**File**: `screens/combat/combat.py`
**Line 47**: Hardcoded `max_lines=4`

```python
# BEFORE (October 2025)
narrative_lines = self._wrap_narrative_text_smart(self.enemy.encounter_narrative, 75, max_lines=4)
# Result: Always shows exactly 4 lines, truncates rest with "..."

# AFTER (Fixed October 2025)
narrative_lines = self._wrap_narrative_text_smart(self.enemy.encounter_narrative, 75, max_lines=8)
# Result: Shows up to 8 lines, displays full AI-generated content
```

**The Fix**: Changed ONE NUMBER from 4 → 8 in combat.py line 47

**Time to Fix**: 5 seconds (after finding the right line)
**Time Wasted**: 2+ hours (editing wrong directory, wrong functions)

### Quick Reference Guide

#### Common Narrative Modifications

**Change Display Line Count (6-12 lines)**
- **File**: `screens/combat/combat.py`
- **Line**: 47
- **Change**: `max_lines=8` (or any number 1-12)
- **Impact**: Immediate - controls how many lines render on screen

**Increase AI Generation Length**
- **File**: `brainbot.py`
- **Line**: 282
- **Change**: `max_tokens=400` (current), can increase to 600-800
- **Impact**: Slower generation, more detailed narratives

**Add/Modify Template Narratives**
- **File**: `obsidian.py`
- **Lines**: 929-990 (content-specific templates)
- **Lines**: 995-1024 (extension logic)
- **Impact**: Better fallback when AI unavailable

**Adjust Text Wrapping Width**
- **File**: `screens/combat/combat.py`
- **Line**: 47
- **Change**: First parameter (currently `75`)
- **Impact**: Wider/narrower text columns

#### Debugging Narrative Issues

**Step 1: Identify Which Stage Fails**
```python
# Add temporary debug in combat.py compose() method
print(f"📏 Narrative length: {len(self.enemy.encounter_narrative)} chars")
print(f"📏 First 100 chars: {self.enemy.encounter_narrative[:100]}")
```

**Step 2: Check Generation (if empty/generic)**
```python
# Check in obsidian.py or brainbot.py
print(f"🎭 Generated narrative: {encounter_narrative[:200]}")
```

**Step 3: Check Display (if truncated)**
```python
# Check max_lines parameter in combat.py:47
narrative_lines = self._wrap_narrative_text_smart(..., max_lines=???)
```

**90% of issues are Stage 3 (display)** - check `screens/combat/combat.py:47` first!

## Working Directory Issues

### Working Directory Verification Protocol

**Problem**: Changes not taking effect after editing files

**Cause**: Editing files in wrong project directory (e.g., `/ai-red-dragon/` instead of `/legend_of_obsidian/`)

### Verification Steps

When user reports "changes aren't working":
1. **Check**: `pwd` or "What directory are you in?"
2. **Verify**: Files exist in user's reported directory
3. **Test**: `ls screens/combat/combat.py` in correct location
4. **Confirm**: Git status shows modifications in correct repo

```bash
# ✅ CORRECT working directory
/Users/name/homelab/legend_of_obsidian/

# ❌ WRONG directory (old test copy)
/Users/name/homelab/ai-red-dragon/
```

### Quick Fix

```bash
# Always verify before making changes
pwd
git status

# If in wrong directory
cd /Users/name/homelab/legend_of_obsidian
```

**Never assume directory location** - always verify!

## AI Integration Problems

### AI Not Loading

**Symptom**: "AI unavailable" message in combat/settings

**Common Causes**:
1. Incorrect threading initialization
2. Model download failed
3. Insufficient memory (< 2GB available)
4. Missing dependencies

### Debugging Steps

**1. Check AI Initialization**
```bash
python3 -c "from brainbot import initialize_ai, is_ai_available; initialize_ai(); import time; time.sleep(3); print(is_ai_available())"
```

**Expected Output**: `True`
**If False**: Check error messages in terminal

**2. Verify Model Download**
```bash
ls ~/.cache/huggingface/hub/
# Should see: models--TheBloke--TinyLlama-1.1B-Chat-v1.0-GGUF
```

**3. Check Memory Usage**
```bash
# Mac/Linux
free -h
# or
top

# Should have at least 2GB free
```

**4. Test Model Loading**
```python
# test_ai.py
from brainbot import LocalAIClient

client = LocalAIClient()
client.initialize()
print(f"AI available: {client.available}")
```

### AI Initialization Fix (v0.0.2)

**Problem**: Incorrect async/await usage causing startup crashes

```python
# ❌ BEFORE: Incorrect - asyncio.create_task() outside event loop
asyncio.create_task(initialize_ai())

# ✅ AFTER: Proper threading for background initialization
import threading
ai_thread = threading.Thread(target=initialize_ai, daemon=True)
ai_thread.start()
```

### Slow AI Response Times

**Symptom**: 5+ second delay for quiz questions or narratives

**Solutions**:
1. **Check Cache**: Clear response cache in `brainbot.py`
2. **Reduce Context**: Lower `max_tokens` parameter
3. **CPU Optimization**: Ensure no other heavy processes running
4. **Model Selection**: TinyLlama 1.1B is optimal for speed/quality

```python
# Adjust in brainbot.py
response = self.generate_text(
    prompt,
    max_tokens=200,  # Reduced from 400 for faster responses
    generation_type="quiz"
)
```

## Import and Module Errors

### Circular Import Issues

**Symptom**: `ImportError: cannot import name 'X' from partially initialized module`

**Cause**: Screens import each other directly

**Solution**: Use delayed imports (v0.0.3 pattern)

```python
# ❌ BAD: Top-level import
from screens.town.inn import InnScreen

# ✅ GOOD: Delayed import inside method
def _show_inn(self):
    from screens.town.inn import InnScreen
    self.app.push_screen(InnScreen())
```

### Missing Screen Imports

**Symptom**: `NameError: name 'XScreen' is not defined`

**Cause**: Screen not imported in `lov.py` or calling module

**Fix**: Add delayed import where screen is used

```python
def on_button_pressed(self, event: Button.Pressed) -> None:
    if event.button.id == "go_to_forest":
        from screens.combat.forest import ForestScreen
        self.app.push_screen(ForestScreen())
```

### Module Not Found Errors

**Symptom**: `ModuleNotFoundError: No module named 'textual'`

**Solution**: Run setup script

```bash
# Auto-install all dependencies
./run.sh        # Mac/Linux
run.bat         # Windows

# Or manual install
pip install -r requirements.txt
```

## Performance Issues

### Slow Vault Scanning

**Symptom**: 5+ second delay when entering Forest

**Cause**: Large vault (1000+ notes) without caching

**Solutions**:

**1. Check Cache Status**
```python
# In obsidian.py
print(f"Cache size: {len(self._note_cache)}")
print(f"Last scan: {self._last_scan_time}")
```

**2. Increase Cache TTL**
```python
# obsidian.py - extend cache duration
CACHE_DURATION = 600  # 10 minutes instead of 5
```

**3. Exclude Folders**
```python
# Add to vault scanning logic
SKIP_FOLDERS = {'.trash', '.obsidian', 'Archive', 'Templates'}
```

### Memory Leaks

**Symptom**: RAM usage grows over time (> 3GB after 30 minutes)

**Debugging**:
```python
import tracemalloc
tracemalloc.start()

# In game loop
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)
```

**Common Causes**:
1. AI response cache not clearing
2. Screen stack not properly popping
3. Event handlers not disconnecting

## Common Error Messages

### `NoMatches` Error

**Full Error**: `textual.css.query.NoMatches: No nodes match '#combat_status'`

**Cause**: UI element not yet mounted or ID mismatch

**Fix**: Check element exists before querying
```python
# ❌ BAD
status_widget = self.query_one("#combat_status")

# ✅ GOOD
try:
    status_widget = self.query_one("#combat_status")
except NoMatches:
    self.notify("Combat status widget not ready", severity="warning")
    return
```

### `can_focus` Keyboard Input Issues

**Symptom**: Keyboard shortcuts not responding

**Cause**: Screen lacks focus capability

**Fix**: Add focus management (v0.0.2 pattern)
```python
class MyScreen(Screen):
    can_focus = True  # Enable keyboard input

    def on_mount(self) -> None:
        self.focus()  # Auto-focus on mount
        self.notify("Screen ready! Keyboard active")
```

### Database Migration Errors

**Symptom**: `OperationalError: no such column: fairy_lore`

**Cause**: Old save file missing new columns

**Fix**: Automatic migration in `game_data.py`
```python
# Database migration runs automatically
# But you can force it:
from game_data import migrate_database
migrate_database()
```

### File Not Found: `.icloud` Files

**Symptom**: `FileNotFoundError` when accessing notes

**Cause**: iCloud placeholder files not downloaded

**Fix**: Already handled in `obsidian.py`
```python
# Automatically skips .icloud placeholders
if file_path.suffix == '.icloud':
    continue
```

## Debug Logging

### Enable Verbose Logging

```python
# Add to top of lov.py
import logging
logging.basicConfig(level=logging.DEBUG)

# In specific modules
logger = logging.getLogger(__name__)
logger.debug(f"Enemy narrative: {enemy.encounter_narrative[:100]}")
```

### Textual Debug Mode

```bash
# Run with Textual devtools
textual console
# In another terminal
python3 lov.py
```

### Quick Debug Snippets

**Check Player State**
```python
print(f"Player: {lov.current_player.name}, HP: {lov.current_player.hitpoints}")
```

**Check AI Status**
```python
from brainbot import is_ai_available
print(f"AI Ready: {is_ai_available()}")
```

**Check Vault Status**
```python
from obsidian import vault
print(f"Vault: {vault.get_vault_path()}")
print(f"Notes: {len(vault.scan_notes())}")
```

---

For general development guide, see [CLAUDE.md](CLAUDE.md).
For feature roadmap, see [ROADMAP.md](ROADMAP.md).
For version history, see [CHANGELOG.md](CHANGELOG.md).
