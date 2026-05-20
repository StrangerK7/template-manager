"""
Template_Manager.py — Resolve menu version (safe, minimal)
Workspace → Scripts → Utility → Template Manager
"""

import sys
from pathlib import Path

PROJECT_DIR = Path("/Users/kamil/Code/davinci-tools/template-manager")
sys.path.insert(0, str(PROJECT_DIR))

import tkinter as tk
from template_manager_ui import TemplateManagerApp


def main():
    print("=" * 50)
    print("🎬 Template Manager UI launching...")
    print("=" * 50)
    
    root = tk.Tk()
    
    # Basic foreground attempt — NO AppKit (Resolve crash karta hai usse)
    root.lift()
    root.attributes("-topmost", True)
    root.after(500, lambda: root.attributes("-topmost", False))
    
    app = TemplateManagerApp(root, resolve=resolve)
    root.mainloop()
    
    print("✅ Template Manager closed.")


main()