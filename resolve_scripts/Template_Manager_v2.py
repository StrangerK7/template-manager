"""
Template_Manager_v2.py — Resolve menu version (UIManager-based)
Workspace → Scripts → Utility → Template Manager v2

Production-quality UI. Foreground, dark theme, crash-free.
"""

import sys
import datetime
from pathlib import Path

# core.py ka path
PROJECT_DIR = Path("/Users/kamil/Code/davinci-tools/template-manager")
sys.path.insert(0, str(PROJECT_DIR))

from core import (
    list_template_files,
    load_template,
    save_template,
    read_project_to_dict,
    apply_template_to_new_project,
)


# ============================================
# UI setup
# ============================================
ui = fu.UIManager
disp = bmd.UIDispatcher(ui)


# Section header style — bold + larger
SECTION_HEADER_STYLE = "font-size: 14px; font-weight: bold; padding: 6px 0px; color: #4A9EFF;"


# ============================================
# Window
# ============================================
win = disp.AddWindow({
    "ID": "TemplateManagerV2Window",
    "WindowTitle": "DaVinci Template Manager",
    "Geometry": [400, 200, 500, 520],
}, [
    ui.VGroup({
        "Spacing": 12,
        "Weight": 1,
    }, [
        # ========== Title ==========
        ui.Label({
            "ID": "TitleLabel",
            "Text": "🎬 Template Manager",
            "Alignment": {"AlignHCenter": True, "AlignVCenter": True},
            "Weight": 0,
            "StyleSheet": "font-size: 18px; font-weight: bold; padding: 8px;",
        }),
        
        # ========== Section 1: Apply Template ==========
        ui.Label({
            "Text": "▸ APPLY TEMPLATE",
            "Weight": 0,
            "StyleSheet": SECTION_HEADER_STYLE,
        }),
        
        ui.Label({
            "Text": "Template choose karo:",
            "Weight": 0,
        }),
        ui.ComboBox({
            "ID": "TemplateComboBox",
            "Weight": 0,
        }),
        
        ui.Label({
            "Text": "Naye project ka naam (khali = auto-name):",
            "Weight": 0,
        }),
        ui.LineEdit({
            "ID": "ProjectNameLineEdit",
            "PlaceholderText": "Optional — timestamp se auto-generate hoga",
            "Weight": 0,
        }),
        
        ui.HGroup({
            "Spacing": 8,
            "Weight": 0,
        }, [
            ui.Button({
                "ID": "RefreshButton",
                "Text": "🔄 Refresh",
                "Weight": 0,
            }),
            ui.Button({
                "ID": "ApplyButton",
                "Text": "🚀 Apply Template",
                "Weight": 1,
            }),
        ]),
        
        # ========== Spacer ==========
        ui.Label({
            "Text": "",
            "Weight": 0,
            "StyleSheet": "padding: 4px;",
        }),
        
        # ========== Section 2: Save Current ==========
        ui.Label({
            "Text": "▸ SAVE CURRENT PROJECT",
            "Weight": 0,
            "StyleSheet": SECTION_HEADER_STYLE,
        }),
        
        ui.Label({
            "Text": "Current Resolve project ko template banao:",
            "Weight": 0,
        }),
        ui.Button({
            "ID": "SaveButton",
            "Text": "💾 Save Current Project as Template",
            "Weight": 0,
        }),
        
        # ========== Status Label ==========
        ui.Label({
            "ID": "StatusLabel",
            "Text": "Ready",
            "Alignment": {"AlignHCenter": True, "AlignVCenter": True},
            "Weight": 1,
        }),
        
        # ========== Close button ==========
        ui.Button({
            "ID": "CloseButton",
            "Text": "Close",
            "Weight": 0,
        }),
    ]),
])


# ============================================
# Template paths cache
# ============================================
template_paths_cache = []


# ============================================
# Helper functions
# ============================================

def set_status(text, color="white"):
    """Status label update with color."""
    label = win.Find("StatusLabel")
    label.Text = text
    label.StyleSheet = f"color: {color};"


def refresh_templates():
    """Reload templates list from disk."""
    global template_paths_cache
    
    template_paths_cache = list_template_files()
    
    combo = win.Find("TemplateComboBox")
    combo.Clear()
    
    if not template_paths_cache:
        set_status("⚠️  Koi templates nahi — Save Current chala", "orange")
        return
    
    for t in template_paths_cache:
        combo.AddItem(t.stem)
    
    combo.CurrentIndex = 0
    set_status(f"✅ {len(template_paths_cache)} templates loaded", "lightgreen")


# ============================================
# Event handlers
# ============================================

def on_refresh_click(ev):
    refresh_templates()


def on_apply_click(ev):
    combo = win.Find("TemplateComboBox")
    idx = combo.CurrentIndex
    
    if idx < 0 or not template_paths_cache:
        set_status("⚠️  Pehle template choose kar", "orange")
        return
    
    chosen_path = template_paths_cache[idx]
    name_input = win.Find("ProjectNameLineEdit").Text.strip()
    
    try:
        template_data = load_template(chosen_path)
        
        if name_input:
            new_name = name_input
        else:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            new_name = f"{template_data['project_name']} - {timestamp}"
        
        set_status(f"🏗  Bana raha hoon: {new_name}", "lightblue")
        
        new_proj = apply_template_to_new_project(
            resolve, template_data, new_name, print_progress=True
        )
        
        if new_proj:
            set_status(f"✅ '{new_proj.GetName()}' ready hai!", "lightgreen")
            win.Find("ProjectNameLineEdit").Text = ""
        else:
            set_status(f"❌ '{new_name}' naam shayad exist karta hai", "red")
    
    except Exception as e:
        set_status(f"❌ Error: {e}", "red")
        print(f"Apply error: {e}")


def on_save_click(ev):
    pm = resolve.GetProjectManager()
    proj = pm.GetCurrentProject()
    
    if not proj:
        set_status("⚠️  Koi project khula nahi hai Resolve mein", "orange")
        return
    
    try:
        set_status("💾 Save ho raha hai...", "lightblue")
        
        template_data = read_project_to_dict(proj, print_progress=True)
        output_file = save_template(template_data)
        
        set_status(f"✅ Saved: {output_file.name}", "lightgreen")
        refresh_templates()
    
    except Exception as e:
        set_status(f"❌ Save error: {e}", "red")
        print(f"Save error: {e}")


def on_close_click(ev):
    disp.ExitLoop()


def on_window_close(ev):
    disp.ExitLoop()


# ============================================
# Handlers connect karo
# ============================================
win.On.RefreshButton.Clicked = on_refresh_click
win.On.ApplyButton.Clicked = on_apply_click
win.On.SaveButton.Clicked = on_save_click
win.On.CloseButton.Clicked = on_close_click
win.On.TemplateManagerV2Window.Close = on_window_close


# ============================================
# Initial setup + show
# ============================================
print("=" * 50)
print("🎬 Template Manager v2 (UIManager) launching...")
print("=" * 50)

refresh_templates()

win.Show()
disp.RunLoop()
win.Hide()

print("✅ Template Manager v2 closed")