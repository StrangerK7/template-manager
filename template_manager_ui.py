"""
template_manager_ui.py
Tkinter GUI for Template Manager.

Run from terminal:
    python3 template_manager_ui.py

Run from Resolve menu (Day 5 baad):
    Workspace → Scripts → Utility → Template Manager
"""

import sys
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

# core.py se sab logic import kar
from core import (
    get_resolve_terminal,
    list_template_files,
    load_template,
    save_template,
    read_project_to_dict,
    apply_template_to_new_project,
)


class TemplateManagerApp:
    """Main app class — saara UI yahan hai."""
    
    def __init__(self, root, resolve=None):
        self.root = root
        self.resolve = resolve  # Resolve handle — agar None hai to terminal mode
        
        # Window setup
        self.root.title("DaVinci Template Manager")
        self.root.geometry("500x450")
        self.root.resizable(False, False)
        
        self._build_ui()
        self._refresh_template_list()
    
    def _build_ui(self):
        """Saare widgets create kar."""
        
        # === Title ===
        title = tk.Label(
            self.root,
            text="🎬 DaVinci Template Manager",
            font=("Arial", 18, "bold"),
        )
        title.pack(pady=15)
        
        # === Section 1: Apply Template ===
        apply_frame = tk.LabelFrame(self.root, text="Apply Template", padx=15, pady=10, font=("Arial", 12, "bold"))
        apply_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(apply_frame, text="Template choose karo:").pack(anchor="w")
        self.template_dropdown = ttk.Combobox(apply_frame, state="readonly", width=40)
        self.template_dropdown.pack(fill="x", pady=5)
        
        tk.Label(apply_frame, text="Naye project ka naam:").pack(anchor="w", pady=(10, 0))
        self.project_name_entry = tk.Entry(apply_frame, width=40)
        self.project_name_entry.pack(fill="x", pady=5)
        
        apply_btn = tk.Button(
            apply_frame,
            text="🚀 Apply Template",
            command=self._on_apply_click,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            pady=8,
        )
        apply_btn.pack(fill="x", pady=(10, 0))
        
        # === Section 2: Save Current Project as Template ===
        save_frame = tk.LabelFrame(self.root, text="Save Current Project", padx=15, pady=10, font=("Arial", 12, "bold"))
        save_frame.pack(fill="x", padx=20, pady=5)
        
        save_btn = tk.Button(
            save_frame,
            text="💾 Save Current Project as Template",
            command=self._on_save_click,
            bg="#2196F3",
            fg="white",
            font=("Arial", 12, "bold"),
            pady=8,
        )
        save_btn.pack(fill="x")
        
        # === Status Bar ===
        self.status_label = tk.Label(
            self.root,
            text="Ready",
            relief="sunken",
            anchor="w",
            padx=10,
            font=("Arial", 10),
        )
        self.status_label.pack(side="bottom", fill="x")
    
    def _refresh_template_list(self):
        """Templates folder se list refresh kar."""
        templates = list_template_files()
        if templates:
            self.template_paths = templates
            template_names = [t.stem for t in templates]
            self.template_dropdown["values"] = template_names
            self.template_dropdown.current(0)  # pehla auto-select
            self._set_status(f"✅ {len(templates)} templates loaded")
        else:
            self.template_paths = []
            self.template_dropdown["values"] = []
            self._set_status("⚠️ Koi templates nahi — pehle Save kar")
    
    def _set_status(self, text, color="black"):
        """Status bar update kar."""
        self.status_label.config(text=text, fg=color)
    
    def _get_resolve(self):
        """Resolve handle return kar — context ke hisaab se."""
        if self.resolve:
            return self.resolve
        # Terminal mode mein khud connect kar
        return get_resolve_terminal()
    
    # === Event Handlers ===
    
    def _on_apply_click(self):
        """Apply button click handler."""
        # Template selected hai?
        selected_idx = self.template_dropdown.current()
        if selected_idx < 0 or not self.template_paths:
            messagebox.showwarning("Warning", "Pehle template choose kar.")
            return
        
        chosen_path = self.template_paths[selected_idx]
        
        # Project naam diya hai? Nahi to auto-generate
        new_name = self.project_name_entry.get().strip()
        if not new_name:
            template_data = load_template(chosen_path)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            new_name = f"{template_data['project_name']} - {timestamp}"
        
        # Resolve handle
        resolve = self._get_resolve()
        if not resolve:
            messagebox.showerror("Error", "Resolve se connect nahi ho paya. Resolve khula hai?")
            return
        
        # Apply kar
        self._set_status("🏗 Project bana raha hoon...", "blue")
        self.root.update()  # UI ko refresh hone do
        
        try:
            template_data = load_template(chosen_path)
            new_proj = apply_template_to_new_project(
                resolve, template_data, new_name, print_progress=True
            )
            
            if new_proj:
                self._set_status(f"✅ '{new_name}' ready hai", "green")
                messagebox.showinfo("Success", f"🎉 Project '{new_proj.GetName()}' bana diya!")
                self.project_name_entry.delete(0, tk.END)
            else:
                self._set_status("❌ Failed", "red")
                messagebox.showerror(
                    "Error",
                    f"Project banane mein dikkat. '{new_name}' naam pehle se hai shayad?"
                )
        except Exception as e:
            self._set_status(f"❌ Error: {e}", "red")
            messagebox.showerror("Error", f"Kuch gadbad hui:\n{e}")
    
    def _on_save_click(self):
        """Save button click handler."""
        resolve = self._get_resolve()
        if not resolve:
            messagebox.showerror("Error", "Resolve se connect nahi ho paya.")
            return
        
        pm = resolve.GetProjectManager()
        proj = pm.GetCurrentProject()
        if not proj:
            messagebox.showwarning("Warning", "Koi project khula nahi hai Resolve mein.")
            return
        
        self._set_status("💾 Save ho raha hai...", "blue")
        self.root.update()
        
        try:
            template_data = read_project_to_dict(proj, print_progress=True)
            output_file = save_template(template_data)
            
            self._set_status(f"✅ Saved: {output_file.name}", "green")
            messagebox.showinfo("Saved", f"Template saved:\n{output_file}")
            self._refresh_template_list()  # dropdown update
        except Exception as e:
            self._set_status(f"❌ Error: {e}", "red")
            messagebox.showerror("Error", f"Save mein dikkat:\n{e}")


def main():
    """Terminal se chalane ke liye entry point."""
    root = tk.Tk()
    app = TemplateManagerApp(root, resolve=None)  # resolve=None → terminal mode
    root.mainloop()


if __name__ == "__main__":
    main()