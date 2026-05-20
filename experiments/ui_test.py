"""
ui_test.py — UIManager learning script
Run from: Resolve → Workspace → Scripts → Utility → UI Test

Pehla UIManager window — minimal example.
"""

# Resolve menu mein 'fu', 'bmd', 'resolve' automatically available hain
# Manually scriptapp wagairah ki zaroorat nahi

ui = fu.UIManager
disp = bmd.UIDispatcher(ui)


# === Window banao ===
win = disp.AddWindow({
    "ID": "UITestWindow",         # Unique window ID
    "WindowTitle": "UI Test",     # Title bar text
    "Geometry": [400, 300, 350, 200],  # [x, y, width, height]
}, [
    # Layout — VGroup = vertical stack (Tkinter ka pack() jaisa)
    ui.VGroup({
        "Spacing": 10,
        "Weight": 1,
    }, [
        # Widgets yahan andar
        ui.Label({
            "ID": "TitleLabel",
            "Text": "Hello from UIManager! 🎉",
            "Alignment": {"AlignHCenter": True, "AlignVCenter": True},
            "Weight": 0,
        }),
        ui.Label({
            "ID": "StatusLabel",
            "Text": "Button click karo niche",
            "Alignment": {"AlignHCenter": True, "AlignVCenter": True},
            "Weight": 0,
        }),
        ui.Button({
            "ID": "TestButton",
            "Text": "Click Me",
            "Weight": 0,
        }),
        ui.Button({
            "ID": "CloseButton",
            "Text": "Close",
            "Weight": 0,
        }),
    ]),
])


# === Event handlers (function definitions) ===

def on_test_click(ev):
    """Test button click — status label update karega."""
    win.Find("StatusLabel").Text = "✅ Button kaam kar raha hai!"
    print("Test button clicked!")


def on_close_click(ev):
    """Close button — window band karega."""
    print("Closing window...")
    disp.ExitLoop()


def on_window_close(ev):
    """X button click — Mac ka red dot."""
    disp.ExitLoop()


# === Handlers ko connect karo ===
win.On.TestButton.Clicked = on_test_click
win.On.CloseButton.Clicked = on_close_click
win.On.UITestWindow.Close = on_window_close


# === Window show + event loop ===
win.Show()
disp.RunLoop()
win.Hide()

print("✅ UI Test closed")