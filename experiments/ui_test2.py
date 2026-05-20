"""
ui_test2.py — UIManager widgets exploration
Run from: Resolve → Workspace → Scripts → Utility → UI Test2

3 cheezein test karenge:
1. ComboBox (dropdown)
2. LineEdit (text input)
3. HGroup (horizontal layout)
"""

ui = fu.UIManager
disp = bmd.UIDispatcher(ui)


# === Window banao ===
win = disp.AddWindow({
    "ID": "UITest2Window",
    "WindowTitle": "UI Test 2 — Widget Playground",
    "Geometry": [400, 300, 450, 400],
}, [
    ui.VGroup({
        "Spacing": 12,
        "Weight": 1,
    }, [
        # ========== Section 1: Title ==========
        ui.Label({
            "ID": "TitleLabel",
            "Text": "Widget Playground 🎨",
            "Alignment": {"AlignHCenter": True, "AlignVCenter": True},
            "Weight": 0,
        }),
        
        # ========== Section 2: ComboBox (Dropdown) ==========
        ui.Label({
            "Text": "Apni fav language choose karo:",
            "Weight": 0,
        }),
        ui.ComboBox({
            "ID": "LangComboBox",
            "Weight": 0,
        }),
        
        # ========== Section 3: LineEdit (Text Input) ==========
        ui.Label({
            "Text": "Apna naam likho:",
            "Weight": 0,
        }),
        ui.LineEdit({
            "ID": "NameLineEdit",
            "PlaceholderText": "Yahan type kar...",
            "Weight": 0,
        }),
        
        # ========== Section 4: HGroup (side-by-side buttons) ==========
        ui.Label({
            "Text": "Actions:",
            "Weight": 0,
        }),
        ui.HGroup({
            "Spacing": 8,
            "Weight": 0,
        }, [
            ui.Button({
                "ID": "GreetButton",
                "Text": "👋 Greet",
                "Weight": 1,  # equal width
            }),
            ui.Button({
                "ID": "ClearButton",
                "Text": "🗑 Clear",
                "Weight": 1,
            }),
            ui.Button({
                "ID": "CloseButton",
                "Text": "❌ Close",
                "Weight": 1,
            }),
        ]),
        
        # ========== Section 5: Status Output ==========
        ui.Label({
            "ID": "StatusLabel",
            "Text": "Status: Ready",
            "Alignment": {"AlignHCenter": True, "AlignVCenter": True},
            "Weight": 1,  # baki space lega
        }),
    ]),
])


# ============================================
# ComboBox ko items se populate karo
# (Window banane ke baad hota hai yeh)
# ============================================
combo = win.Find("LangComboBox")
combo.AddItem("Python 🐍")
combo.AddItem("JavaScript 📜")
combo.AddItem("C++ 🔧")
combo.AddItem("Lua 🌙")
combo.CurrentIndex = 0  # pehla item default selected


# ============================================
# Event handlers
# ============================================

def on_greet_click(ev):
    """Greet button — naam aur language combine karega."""
    name = win.Find("NameLineEdit").Text
    lang = win.Find("LangComboBox").CurrentText
    
    if not name:
        win.Find("StatusLabel").Text = "⚠️  Pehle naam likh"
        return
    
    msg = f"✅ Hi {name}! Tu {lang} likhta hai 🚀"
    win.Find("StatusLabel").Text = msg
    print(msg)


def on_clear_click(ev):
    """Clear button — naam aur status reset."""
    win.Find("NameLineEdit").Text = ""
    win.Find("StatusLabel").Text = "Status: Cleared"
    win.Find("LangComboBox").CurrentIndex = 0
    print("Cleared")


def on_lang_changed(ev):
    """ComboBox selection change — auto status update."""
    selected = win.Find("LangComboBox").CurrentText
    win.Find("StatusLabel").Text = f"Selected: {selected}"
    print(f"Language changed: {selected}")


def on_close_click(ev):
    """Close button."""
    disp.ExitLoop()


def on_window_close(ev):
    """X button (red dot)."""
    disp.ExitLoop()


# ============================================
# Handlers connect karo
# ============================================
win.On.GreetButton.Clicked = on_greet_click
win.On.ClearButton.Clicked = on_clear_click
win.On.CloseButton.Clicked = on_close_click
win.On.LangComboBox.CurrentIndexChanged = on_lang_changed
win.On.UITest2Window.Close = on_window_close


# ============================================
# Show + Run
# ============================================
win.Show()
disp.RunLoop()
win.Hide()

print("✅ UI Test 2 closed")