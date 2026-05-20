# DaVinci Resolve Template Manager

Personal tool to save & reuse Resolve project structures (bins, timelines, render settings).

## What it does

- **Save Template** — Current Resolve project ki structure ko JSON template mein save karta hai
- **Apply Template** — Saved template se naya Resolve project banata hai with bins + timelines + settings

## Two ways to use

### 1. Resolve Menu (recommended)
Workspace → Scripts → Utility → **Save Template** / **Apply Template**

### 2. Terminal (full interactive)
```bash
python3 read_project.py        # Save current project as template
python3 apply_template.py      # Apply template (interactive prompts)
```

## File structure

- `core.py` — Shared logic (read/write/apply)
- `read_project.py` — CLI: save template
- `apply_template.py` — CLI: apply template with prompts
- `resolve_scripts/` — Resolve menu versions (symlinked to Resolve's Scripts folder)

## Templates location

`~/Documents/ResolveTemplates/*.json`

## Status

🚧 Week 1 — Core working. UI (Tkinter) coming in Day 5-6.

## Tech

- Python 3.10
- DaVinci Resolve Studio Python API
- macOS (Windows support TBD)