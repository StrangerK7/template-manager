"""
Apply_Template.py — Resolve menu version (simple)
Workspace → Scripts → Utility → Apply Template

NOTE: Yeh simple version hai — pehla template auto-apply karta hai.
Day 5-6 mein Tkinter dialog add karenge selection ke liye.
"""

import sys
import datetime
from pathlib import Path

# Apne core.py ka path
PROJECT_DIR = Path("/Users/kamil/Code/davinci-tools/template-manager")
sys.path.insert(0, str(PROJECT_DIR))

from core import (
    list_template_files,
    load_template,
    apply_template_to_new_project,
)


# ============================================
# CONFIGURATION — yahan badal sakta hai
# ============================================
# Konsa template apply karna hai? "Reel Template" ya koi aur naam
TEMPLATE_TO_APPLY = "Reel Template"

# Naye project ka naam pattern — timestamp add hoga unique rakhne ke liye
NEW_PROJECT_NAME_PATTERN = "{template} - {timestamp}"
# ============================================


def main():
    print("=" * 50)
    print("🚀 Apply Template — Resolve menu se chal raha hai")
    print("=" * 50)
    
    # Templates list kar
    templates = list_template_files()
    if not templates:
        print("❌ Koi templates nahi mile. Pehle Save Template chala kisi project pe.")
        return
    
    # Configured template dhoondh
    chosen = None
    for t in templates:
        if t.stem == TEMPLATE_TO_APPLY:
            chosen = t
            break
    
    if not chosen:
        print(f"❌ '{TEMPLATE_TO_APPLY}' nahi mila. Available templates:")
        for t in templates:
            print(f"   - {t.stem}")
        print(f"\n📝 Script ke top mein TEMPLATE_TO_APPLY badal de.")
        return
    
    print(f"✅ Template: {chosen.stem}")
    
    # Template load kar
    template_data = load_template(chosen)
    
    # Naam unique banane ke liye timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    new_name = NEW_PROJECT_NAME_PATTERN.format(
        template=template_data["project_name"],
        timestamp=timestamp,
    )
    
    # Apply kar
    new_proj = apply_template_to_new_project(resolve, template_data, new_name)
    
    if not new_proj:
        print(f"\n❌ Project banane mein dikkat. '{new_name}' naam pehle se hai shayad?")
        return
    
    print("\n" + "=" * 50)
    print(f"🎉 Done! Project '{new_proj.GetName()}' ready hai.")
    print("=" * 50)


main()