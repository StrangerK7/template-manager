# Daily Log

## Day 1 — Setup
- Python 3.10, VS Code, zsh env vars setup
- Resolve Console + Terminal dono se Python chalna verify

## Day 2 — First Real Script
- 10 API commands explored
- read_project.py written — Resolve project → JSON
- Git + GitHub setup (with one wrong-folder mishap, fixed)
- First commit pushed

## Day 3 — Tomorrow
- apply_template.py — JSON se naya project banana

## Day 3 — First Working Tool
- apply_template.py written
- Interactive CLI: template choose karo → naam do → project ready
- Tested: Reel Template successfully apply hua
- Bins, timelines, settings sab automatically create huye
- **Milestone: First end-to-end DaVinci tool functional**

## Day 4 — Resolve Menu Integration
- Refactored: shared logic core.py mein, scripts thin
- Banaye: resolve_scripts/Save_Template.py + Apply_Template.py
- Symlinks setup — Resolve ke Utility folder mein link
- **Workspace → Scripts → Utility menu se dono scripts chal rahi hain**
- Apply Template successfully tested — naya project + bins + timeline created
- Save Template tested — JSON properly save hua

**Milestone: First plugin-style tool — Resolve ke andar se chala**

## Day 5 — UIManager Discovery & First Window

### Tkinter Detour (productive failure)
- Tkinter GUI banayi terminal mein chal gayi
- macOS foreground issue — lift/topmost partial fix
- AppKit NSApplication tried → fuscript crash
- Lesson: Tkinter not suitable for embedded Resolve scripts

### 🎯 Big Win — UIManager
- User found Snap Captions Lua script as reference
- Identified correct approach: fu.UIManager + bmd.UIDispatcher
- ui_test.py written and tested in Resolve menu
- **Window opens in foreground automatically, no hacks**
- Buttons, events, close handler — all working

### Status
- CLI scripts: production-ready ✅
- Save_Template / Apply_Template: production-ready ✅
- UI: pivoting to UIManager (Day 6)
- Tkinter version: kept as standalone/CLI tool

### Day 6 plan
- Template Manager UI rebuild in UIManager
- ComboBox, LineEdit, multiple buttons
- Replace template_manager_ui.py (Tkinter) with native version

## Day 6 — Production UI in UIManager

### Learning (Block 1)
- ui_test2.py — explored ComboBox, LineEdit, HGroup
- Confirmed 6 widgets: Label, Button, ComboBox, LineEdit, VGroup, HGroup
- Event handling pattern: win.On.WidgetID.Event = handler

### Build (Block 2-3)
- Template_Manager_v2.py — production UIManager version
- GroupBox issue (None type) → replaced with styled Labels
- Section headers with CSS styling (blue ▸ headers)
- Status bar with dynamic colors (green/orange/red/blue)
- Live refresh on save
- try/except error handling — no crashes

### Test (Block 4) — ALL PASSED ✅
- Apply with auto-name
- Apply with custom name
- Save current project
- Manual refresh
- Error handling (duplicate name)
- Close (button + X)

### Cleanup (Block 5)
- experiments/ folder for learning files
- Tkinter version archived
- Resolve symlinks cleaned (3 active)
- README rewrote as production doc

### Milestone
🎯 **v1.0 production-ready** — 5 days zero-to-shipping plugin