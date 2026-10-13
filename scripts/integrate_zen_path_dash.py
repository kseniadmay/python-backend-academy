import os

base_dir = r"C:\Users\fury6\OneDrive\Python_Backend_Academy"
academy_path = os.path.join(base_dir, "academy.html")
assemble_path = os.path.join(base_dir, "scripts/assemble_academy.py")

zen_enhancements_css = """
/* ==========================================================================
   ZEN DISTILLATION: PATH & DASHBOARD AESTHETIC ENHANCEMENTS
   ========================================================================== */
.pro-hero-card,
.panel.coddy-rail-card,
.pro-chapter-box,
.dash-results-panel {
  background: var(--zen-surface, rgba(18, 23, 33, 0.82)) !important;
  backdrop-filter: blur(24px) !important;
  -webkit-backdrop-filter: blur(24px) !important;
  border: 1px solid var(--zen-hairline, rgba(255, 255, 255, 0.08)) !important;
  box-shadow: var(--zen-shadow-island, 0 20px 48px -12px rgba(0, 0, 0, 0.5)) !important;
  border-radius: 22px !important;
}

.pro-lesson-row {
  background: var(--zen-surface-subtle, rgba(255, 255, 255, 0.03)) !important;
  border: 1px solid var(--zen-hairline-subtle, rgba(255, 255, 255, 0.045)) !important;
  border-radius: 14px !important;
  transition: all 0.15s ease !important;
}
.pro-lesson-row:hover {
  background: var(--zen-surface-hover, rgba(255, 255, 255, 0.07)) !important;
  border-color: var(--zen-hairline, rgba(255, 255, 255, 0.08)) !important;
}

.dash-tile {
  background: var(--zen-surface-card, rgba(22, 28, 40, 0.65)) !important;
  backdrop-filter: blur(20px) !important;
  -webkit-backdrop-filter: blur(20px) !important;
  border: 1px solid var(--zen-hairline, rgba(255, 255, 255, 0.08)) !important;
  border-radius: 18px !important;
  padding: 16px 18px !important;
  box-shadow: var(--zen-shadow-lift, 0 12px 28px -8px rgba(0, 0, 0, 0.4)) !important;
}

.dash-skill-row,
.dash-track-chip {
  border-radius: 14px !important;
  background: var(--zen-surface-subtle, rgba(255, 255, 255, 0.03)) !important;
  border: 1px solid var(--zen-hairline-subtle, rgba(255, 255, 255, 0.045)) !important;
}
.dash-track-chip:hover {
  background: var(--zen-surface-hover, rgba(255, 255, 255, 0.07)) !important;
}

.m-sq {
  border-radius: 4px !important;
  transition: all 0.15s ease !important;
}

.btn-3d-orange.pro-hero-cta {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%) !important;
  border-radius: 14px !important;
  box-shadow: 0 4px 0 #c2410c, 0 10px 20px rgba(234, 88, 12, 0.35) !important;
  font-weight: 800 !important;
  letter-spacing: 0.02em !important;
}
.btn-3d-orange.pro-hero-cta:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 0 #c2410c, 0 14px 24px rgba(234, 88, 12, 0.45) !important;
}
"""

def inject_zen_css(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    marker = "/* ================= ZEN DISTILLATION: PATH & DASHBOARD AESTHETIC ENHANCEMENTS ================= */"
    if marker in content:
        # replace existing block
        end_idx = content.find("/* ================= 3D TACTILE BUTTONS", content.find(marker))
        if end_idx != -1:
            content = content[:content.find(marker)] + zen_enhancements_css + "\n" + content[end_idx:]
            print(f"[{filepath}] Updated existing Zen CSS")
    else:
        # Inject right before </style> or before 3D TACTILE BUTTONS
        target = "/* ================= 3D TACTILE BUTTONS & CODDY AESTHETICS ================= */"
        if target in content:
            content = content.replace(target, zen_enhancements_css + "\n  " + target, 1)
            print(f"[{filepath}] Injected Zen CSS before 3D tactile buttons")
        else:
            style_close = "</style>"
            content = content.replace(style_close, zen_enhancements_css + "\n" + style_close, 1)
            print(f"[{filepath}] Injected Zen CSS before </style>")

    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

inject_zen_css(academy_path)
inject_zen_css(assemble_path)

print("CSS enhancements integrated successfully!")
