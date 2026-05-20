"""
read_project.py — CLI version
Terminal se chala: python3 read_project.py
Current Resolve project ko JSON template mein save karta hai.
"""

import sys
from core import get_resolve_terminal, read_project_to_dict, save_template


def main():
    print("=" * 50)
    print("Reading current Resolve project...")
    print("=" * 50)
    
    resolve = get_resolve_terminal()
    if not resolve:
        print("❌ Resolve nahi mila. Kya Resolve khula hai?")
        sys.exit(1)
    
    pm = resolve.GetProjectManager()
    proj = pm.GetCurrentProject()
    if not proj:
        print("❌ Koi project khula nahi hai.")
        sys.exit(1)
    
    template_data = read_project_to_dict(proj)
    output_file = save_template(template_data)
    
    print(f"\n✅ Saved to: {output_file}")
    print("=" * 50)


if __name__ == "__main__":
    main()ß