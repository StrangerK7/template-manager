# DaVinci Resolve Template Manager

Save & reuse Resolve project structures (bins, timelines, render settings) with one click.

## 🎬 Features

- **Save Template** — Current Resolve project ki pura structure JSON template mein save
- **Apply Template** — Saved template se naya project banayega with all bins + timelines + settings
- **Live refresh** — Save karte hi dropdown update
- **Auto-naming** — Project naam khali rakho, timestamp se auto-generate
- **Error handling** — Duplicate names, missing data sab handle

## 🚀 Usage

### Resolve Menu (recommended)
Workspace → Scripts → Utility → **Template Manager v2**

UI khulegi foreground mein. Dropdown se template choose, Apply ya Save click. Done.

### Terminal (CLI versions)

    python3 read_project.py        # Save current project as template
    python3 apply_template.py      # Interactive apply with prompts

## 📁 Project Structure

    template-manager/
    ├── core.py                              # Shared logic
    ├── read_project.py                      # CLI: save
    ├── apply_template.py                    # CLI: apply
    ├── resolve_scripts/
    │   ├── Template_Manager_v2.py           # Main GUI (UIManager)
    │   ├── Save_Template.py                 # Menu: quick save
    │   └── Apply_Template.py                # Menu: quick apply
    ├── experiments/                         # Learning artifacts
    ├── LOG.md
    └── README.md

## 📍 Templates Location

`~/Documents/ResolveTemplates/*.json`

## 🛠 Tech Stack

- Python 3.10
- DaVinci Resolve Studio Python API
- Resolve UIManager (Fusion's Qt-based UI framework)
- macOS (Windows support TBD)

## 📊 Status

✅ **v1.0 — Production Ready**
- Core engine: Working
- Resolve menu integration: Working
- UI: Native, foreground, dark-themed
- Tested on Resolve 18+ Studio (macOS)

## 🗺 Roadmap

- [ ] Confirmation dialogs
- [ ] Template metadata (description, thumbnail, tags)
- [ ] Template delete from UI
- [ ] Windows compatibility
- [ ] Export/import templates as bundles