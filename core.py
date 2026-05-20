"""
core.py
Sabhi shared logic — read karna, write karna, helper functions.
Yahan SE koi script direct chala nahi sakti — ye sirf import hoti hai.
"""

import sys
import json
from pathlib import Path


# Common path constants
TEMPLATES_DIR = Path.home() / "Documents" / "ResolveTemplates"
RESOLVE_SCRIPT_API = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"


def ensure_templates_dir():
    """Templates folder pakka exist kare."""
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    return TEMPLATES_DIR


def list_template_files():
    """Saari JSON template files list kar."""
    ensure_templates_dir()
    return sorted(TEMPLATES_DIR.glob("*.json"))


def get_resolve_terminal():
    """Terminal se chalti script ke liye Resolve handle.
    
    Yeh function CLI scripts use karti hain — sys.path setup karke
    DaVinciResolveScript module load karta hai.
    """
    sys.path.insert(0, f"{RESOLVE_SCRIPT_API}/Modules")
    import DaVinciResolveScript as dvr_script
    resolve = dvr_script.scriptapp("Resolve")
    return resolve


# ==========================================
# READ — Project ko JSON template banane wala logic
# ==========================================

def read_bins(folder, depth=0, print_progress=True):
    """Recursively saari bins read kar."""
    bins_data = []
    sub_folders = folder.GetSubFolderList()
    
    for sub in sub_folders:
        clips = sub.GetClipList()
        bin_info = {
            "name": sub.GetName(),
            "clip_count": len(clips),
            "subfolders": read_bins(sub, depth + 1, print_progress),
        }
        bins_data.append(bin_info)
        if print_progress:
            print("  " * depth + f"📁 {sub.GetName()} ({len(clips)} clips)")
    
    return bins_data


def read_timelines(proj, print_progress=True):
    """Saari timelines read kar settings ke saath."""
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
        if print_progress:
            print(f"🎬 {tl.GetName()} — {tl_info['width']}x{tl_info['height']} @ {tl_info['fps']}fps")
    
    return timelines


def read_project_to_dict(proj, print_progress=True):
    """Resolve project ko dictionary mein convert kar (JSON-ready)."""
    project_name = proj.GetName()
    
    mp = proj.GetMediaPool()
    root = mp.GetRootFolder()
    
    if print_progress:
        print(f"\n📦 Project: {project_name}")
        print("\nBins:")
    bins = read_bins(root, print_progress=print_progress)
    
    if print_progress:
        print("\nTimelines:")
    timelines = read_timelines(proj, print_progress=print_progress)
    
    proj_settings = proj.GetSetting("")
    interesting = {
        "timelineResolutionWidth": proj_settings.get("timelineResolutionWidth"),
        "timelineResolutionHeight": proj_settings.get("timelineResolutionHeight"),
        "timelineFrameRate": proj_settings.get("timelineFrameRate"),
        "videoMonitorFormat": proj_settings.get("videoMonitorFormat"),
        "colorScienceMode": proj_settings.get("colorScienceMode"),
    }
    
    return {
        "project_name": project_name,
        "bins": bins,
        "timelines": timelines,
        "settings": interesting,
    }


def save_template(template_data, template_name=None):
    """Template dict ko JSON file mein save kar."""
    ensure_templates_dir()
    name = template_name or template_data["project_name"]
    output_file = TEMPLATES_DIR / f"{name}.json"
    
    with open(output_file, "w") as f:
        json.dump(template_data, f, indent=2)
    
    return output_file


# ==========================================
# APPLY — JSON se naya project banane wala logic
# ==========================================

def load_template(template_path):
    """JSON file load karke dict return kar."""
    with open(template_path, "r") as f:
        return json.load(f)


def create_bins_recursively(media_pool, parent_folder, bins_data, depth=0, print_progress=True):
    """JSON ke bins recursively banao."""
    for bin_info in bins_data:
        new_bin = media_pool.AddSubFolder(parent_folder, bin_info["name"])
        if new_bin:
            if print_progress:
                print("  " * depth + f"📁 {bin_info['name']}")
            if bin_info.get("subfolders"):
                create_bins_recursively(media_pool, new_bin, bin_info["subfolders"], depth + 1, print_progress)
        else:
            print("  " * depth + f"⚠️  Failed: {bin_info['name']}")


def create_timelines_from_data(media_pool, timelines_data, print_progress=True):
    """JSON ki timelines banao with settings."""
    for tl_info in timelines_data:
        tl = media_pool.CreateEmptyTimeline(tl_info["name"])
        if tl:
            tl.SetSetting("timelineFrameRate", str(tl_info["fps"]))
            tl.SetSetting("timelineResolutionWidth", str(tl_info["width"]))
            tl.SetSetting("timelineResolutionHeight", str(tl_info["height"]))
            if print_progress:
                print(f"🎬 {tl_info['name']} — {tl_info['width']}x{tl_info['height']} @ {tl_info['fps']}fps")
        else:
            print(f"⚠️  Timeline failed: {tl_info['name']}")


def apply_project_settings(proj, settings, print_progress=True):
    """Project settings apply kar."""
    applied = 0
    for key, value in settings.items():
        if value is not None:
            if proj.SetSetting(key, str(value)):
                applied += 1
    if print_progress:
        print(f"⚙️  {applied} settings applied")


def apply_template_to_new_project(resolve, template_data, new_project_name, print_progress=True):
    """Pura template apply kar — naya project banana se settings tak."""
    pm = resolve.GetProjectManager()
    
    if print_progress:
        print(f"\n🏗  Creating project: {new_project_name}")
    
    new_proj = pm.CreateProject(new_project_name)
    if not new_proj:
        return None  # Naam pehle se exist karta hai shayad
    
    mp = new_proj.GetMediaPool()
    root = mp.GetRootFolder()
    
    if print_progress:
        print("\nBins:")
    create_bins_recursively(mp, root, template_data.get("bins", []), print_progress=print_progress)
    
    if print_progress:
        print("\nTimelines:")
    create_timelines_from_data(mp, template_data.get("timelines", []), print_progress=print_progress)
    
    if print_progress:
        print()
    apply_project_settings(new_proj, template_data.get("settings", {}), print_progress=print_progress)
    
    return new_proj