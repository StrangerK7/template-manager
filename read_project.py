"""
read_project.py
DaVinci Resolve ke current project ki structure read karke JSON mein save karta hai.

Run: python3 read_project.py
"""

import sys
import json
from pathlib import Path

# Resolve modules import path
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


def read_bins(folder, depth=0):
    """Recursively saari bins aur subfolders read kar."""
    bins_data = []
    sub_folders = folder.GetSubFolderList()
    
    for sub in sub_folders:
        clips = sub.GetClipList()
        bin_info = {
            "name": sub.GetName(),
            "clip_count": len(clips),
            "subfolders": read_bins(sub, depth + 1)  # recursive
        }
        bins_data.append(bin_info)
        print("  " * depth + f"📁 {sub.GetName()} ({len(clips)} clips)")
    
    return bins_data


def read_timelines(proj):
    """Saari timelines aur unke settings read kar."""
    timelines = []
    count = proj.GetTimelineCount()
    
    for i in range(1, count + 1):
        tl = proj.GetTimelineByIndex(i)
        tl_info = {
            "name": tl.GetName(),
            "fps": tl.GetSetting("timelineFrameRate"),
            "width": tl.GetSetting("timelineResolutionWidth"),
            "height": tl.GetSetting("timelineResolutionHeight"),
        }
        timelines.append(tl_info)
        print(f"🎬 Timeline: {tl.GetName()} — {tl_info['width']}x{tl_info['height']} @ {tl_info['fps']}fps")
    
    return timelines


def main():
    print("=" * 50)
    print("Reading current Resolve project...")
    print("=" * 50)
    
    resolve = get_resolve()
    pm = resolve.GetProjectManager()
    proj = pm.GetCurrentProject()
    
    if not proj:
        print("❌ Koi project khula nahi hai.")
        sys.exit(1)
    
    project_name = proj.GetName()
    print(f"\n📦 Project: {project_name}\n")
    
    # Bins
    print("Bins:")
    mp = proj.GetMediaPool()
    root = mp.GetRootFolder()
    bins = read_bins(root)
    
    print()
    
    # Timelines
    print("Timelines:")
    timelines = read_timelines(proj)
    
    # Project settings (relevant subset)
    proj_settings = proj.GetSetting("")
    interesting_settings = {
        "timelineResolutionWidth": proj_settings.get("timelineResolutionWidth"),
        "timelineResolutionHeight": proj_settings.get("timelineResolutionHeight"),
        "timelineFrameRate": proj_settings.get("timelineFrameRate"),
        "videoMonitorFormat": proj_settings.get("videoMonitorFormat"),
        "colorScienceMode": proj_settings.get("colorScienceMode"),
    }
    
    # Sab data ek structure mein
    template_data = {
        "project_name": project_name,
        "bins": bins,
        "timelines": timelines,
        "settings": interesting_settings,
    }
    
    # JSON file mein save
    output_dir = Path.home() / "Documents" / "ResolveTemplates"
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / f"{project_name}.json"
    with open(output_file, "w") as f:
        json.dump(template_data, f, indent=2)
    
    print(f"\n✅ Saved to: {output_file}")
    print("=" * 50)


if __name__ == "__main__":
    main()