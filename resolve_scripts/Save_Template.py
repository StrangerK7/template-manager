"""
Save_Template.py — Resolve menu version
Workspace → Scripts → Utility → Save Template

Current khule project ko JSON template banake save karta hai
~/Documents/ResolveTemplates/ folder mein.
"""

import sys
from pathlib import Path

# Apne core.py ka path add kar
PROJECT_DIR = Path("/Users/kamil/Code/davinci-tools/template-manager")
sys.path.insert(0, str(PROJECT_DIR))

from core import read_project_to_dict, save_template


def main():
    print("=" * 50)
    print("💾 Save Template — Resolve menu se chal raha hai")
    print("=" * 50)
    
    # NOTE: Resolve ke andar 'resolve' variable PEHLE SE available hai
    # bmd.scriptapp("Resolve") karne ki zaroorat nahi
    
    pm = resolve.GetProjectManager()
    proj = pm.GetCurrentProject()
    
    if not proj:
        print("❌ Koi project khula nahi hai.")
        return
    
    template_data = read_project_to_dict(proj)
    output_file = save_template(template_data)
    
    print(f"\n✅ Template saved: {output_file}")
    print("=" * 50)


# IMPORTANT: __name__ check yahan NAHI lagana
# Resolve scripts directly main code execute karte hain
main()