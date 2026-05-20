"""
apply_template.py
Saved JSON template padhke naya Resolve project banata hai
same bins + timelines + settings ke saath.

Run: python3 apply_template.py
"""

import sys
import json
from pathlib import Path

# Resolve modules import path (same as read_project.py)
RESOLVE_SCRIPT_API = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
sys.path.insert(0, f"{RESOLVE_SCRIPT_API}/Modules")

import DaVinciResolveScript as dvr_script


def get_resolve():
    """Resolve se connect kar."""
    resolve = dvr_script.scriptapp("Resolve")
    if not resolve:
        print("❌ Resolve nahi mila. Kya Resolve khula hai?")
        sys.exit(1)
    return resolve


def list_templates():
    """Templates folder se saari JSON files list kar."""
    templates_dir = Path.home() / "Documents" / "ResolveTemplates"
    
    if not templates_dir.exists():
        print(f"❌ Templates folder nahi mila: {templates_dir}")
        print("   Pehle read_project.py chala ke ek template save kar.")
        sys.exit(1)
    
    json_files = sorted(templates_dir.glob("*.json"))
    
    if not json_files:
        print(f"❌ Koi template files nahi mili {templates_dir} mein.")
        sys.exit(1)
    
    return json_files


def choose_template(templates):
    """User se template choose karwa."""
    print("\n📋 Available templates:")
    for i, t in enumerate(templates, 1):
        print(f"  {i}. {t.stem}")  # stem = filename without .json
    
    while True:
        choice = input(f"\nKaunsa template? (1-{len(templates)}): ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(templates):
                return templates[idx]
            print(f"⚠️  1 se {len(templates)} ke beech mein number daal.")
        except ValueError:
            print("⚠️  Number daal, text nahi.")


def create_bins_recursively(media_pool, parent_folder, bins_data, depth=0):
    """JSON ke bins recursively banao."""
    for bin_info in bins_data:
        new_bin = media_pool.AddSubFolder(parent_folder, bin_info["name"])
        if new_bin:
            print("  " * depth + f"📁 Bin banayi: {bin_info['name']}")
            # Agar subfolders hain to unhe bhi banao (recursion)
            if bin_info.get("subfolders"):
                create_bins_recursively(media_pool, new_bin, bin_info["subfolders"], depth + 1)
        else:
            print("  " * depth + f"⚠️  Bin banane mein dikkat: {bin_info['name']}")


def create_timelines(media_pool, timelines_data):
    """JSON ki timelines banao with settings."""
    for tl_info in timelines_data:
        tl = media_pool.CreateEmptyTimeline(tl_info["name"])
        if tl:
            # Settings apply kar
            tl.SetSetting("timelineFrameRate", str(tl_info["fps"]))
            tl.SetSetting("timelineResolutionWidth", str(tl_info["width"]))
            tl.SetSetting("timelineResolutionHeight", str(tl_info["height"]))
            print(f"🎬 Timeline bani: {tl_info['name']} — {tl_info['width']}x{tl_info['height']} @ {tl_info['fps']}fps")
        else:
            print(f"⚠️  Timeline banane mein dikkat: {tl_info['name']}")


def apply_project_settings(proj, settings):
    """Project settings apply kar."""
    applied = 0
    for key, value in settings.items():
        if value is not None:
            result = proj.SetSetting(key, str(value))
            if result:
                applied += 1
    print(f"⚙️  {applied} settings applied")


def main():
    print("=" * 50)
    print("Apply Template — Naya project banayega")
    print("=" * 50)
    
    # 1. Templates list kar
    templates = list_templates()
    
    # 2. User se choose karwa
    chosen = choose_template(templates)
    print(f"\n✅ Selected: {chosen.stem}")
    
    # 3. JSON load kar
    with open(chosen, "r") as f:
        template_data = json.load(f)
    
    # 4. Naye project ka naam puch
    default_name = f"{template_data['project_name']} - Copy"
    new_name = input(f"\nNaye project ka naam? (Enter daba '{default_name}' ke liye): ").strip()
    if not new_name:
        new_name = default_name
    
    # 5. Resolve se connect kar aur naya project bana
    resolve = get_resolve()
    pm = resolve.GetProjectManager()
    
    print(f"\n🏗  Project bana raha hoon: {new_name}")
    new_proj = pm.CreateProject(new_name)
    
    if not new_proj:
        print(f"❌ Project banane mein dikkat. Shayad '{new_name}' naam pehle se hai?")
        sys.exit(1)
    
    print(f"✅ Project banaya: {new_proj.GetName()}\n")
    
    # 6. Bins banao
    print("Bins bana raha hoon:")
    mp = new_proj.GetMediaPool()
    root = mp.GetRootFolder()
    create_bins_recursively(mp, root, template_data.get("bins", []))
    
    print()
    
    # 7. Timelines banao
    print("Timelines bana raha hoon:")
    create_timelines(mp, template_data.get("timelines", []))
    
    print()
    
    # 8. Settings apply kar
    apply_project_settings(new_proj, template_data.get("settings", {}))
    
    print()
    print("=" * 50)
    print(f"🎉 Done! Project '{new_proj.GetName()}' ready hai.")
    print("=" * 50)


if __name__ == "__main__":
    main()