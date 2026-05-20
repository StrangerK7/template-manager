"""
apply_template.py — CLI version
Terminal se chala: python3 apply_template.py
Saved JSON template padhke naya Resolve project banata hai.
"""

import sys
from core import (
    get_resolve_terminal,
    list_template_files,
    load_template,
    apply_template_to_new_project,
)


def choose_template(templates):
    """User se template choose karwa (CLI only)."""
    print("\n📋 Available templates:")
    for i, t in enumerate(templates, 1):
        print(f"  {i}. {t.stem}")
    
    while True:
        choice = input(f"\nKaunsa template? (1-{len(templates)}): ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(templates):
                return templates[idx]
            print(f"⚠️  1 se {len(templates)} ke beech daal.")
        except ValueError:
            print("⚠️  Number daal, text nahi.")


def main():
    print("=" * 50)
    print("Apply Template — Naya project banayega")
    print("=" * 50)
    
    templates = list_template_files()
    if not templates:
        print("❌ Koi templates nahi mile. Pehle read_project.py chala.")
        sys.exit(1)
    
    chosen = choose_template(templates)
    print(f"\n✅ Selected: {chosen.stem}")
    
    template_data = load_template(chosen)
    
    default_name = f"{template_data['project_name']} - Copy"
    new_name = input(f"\nNaye project ka naam? (Enter daba '{default_name}' ke liye): ").strip()
    if not new_name:
        new_name = default_name
    
    resolve = get_resolve_terminal()
    if not resolve:
        print("❌ Resolve nahi mila.")
        sys.exit(1)
    
    new_proj = apply_template_to_new_project(resolve, template_data, new_name)
    
    if not new_proj:
        print(f"\n❌ Project banane mein dikkat. '{new_name}' naam pehle se hai shayad?")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print(f"🎉 Done! Project '{new_proj.GetName()}' ready hai.")
    print("=" * 50)


if __name__ == "__main__":
    main()