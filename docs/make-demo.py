#!/usr/bin/env python3
"""Render docs/demo.svg: a terminal-window picture of example `storage-rm` output."""
from html import escape

W, LH, PAD, TOP = 920, 20, 20, 44
FG, DIM, BOLD, CYAN, GREEN, YELLOW = "#d4d4d4", "#7a7a7a", "#ffffff", "#4fc1ff", "#6ad07a", "#e5c07b"

rows = [
    ("docker", "40.1G", "Docker build cache + dangling images (containers and volumes kept)"),
    ("xcode", "12.3G", "Xcode DerivedData, older iOS DeviceSupport, simulator caches"),
    ("gradle", "6.9G", "Gradle caches, daemon logs, old wrapper distributions"),
    ("npm", "3.8G", "npm cache and npx cache"),
    ("pnpm", "1.7G", "pnpm content store"),
    ("brew", "291.0M", "Homebrew download cache and old versions"),
    ("app-caches", "8.9G", "App caches: Spotify, browsers, VS Code, Cursor, Slack, …"),
    ("claude", "2.6G", "Claude desktop simulator builds"),
]
optin = [
    ("android-avd", "10.6G", "Android emulators (AVDs) and SDK system images"),
    ("node-modules", "3.1G", "node_modules in projects untouched for --days"),
]

lines = [
    [("$ ", DIM), ("storage-rm", BOLD)],
    [("==>", CYAN), (" Scanning (nothing is deleted)…", FG)],
    [],
    [("  " + f"{'CATEGORY':<15} {'SIZE':>8}  WHAT", BOLD)],
]
for name, size, what in rows:
    lines.append([(f"  {name:<15} {size:>8}  ", FG), (what, DIM)])
lines.append([("  opt-in", YELLOW)])
for name, size, what in optin:
    lines.append([(f"  {name:<15} {size:>8}  ", FG), (what, DIM)])
lines += [
    [],
    [("  ", FG), ("clean", BOLD), (" would free about ", FG), ("77.1G", GREEN), (" — 573.2G available now", FG)],
    [("  opt-in categories hold another ", FG), ("13.7G", YELLOW), (" (use -o name or --all)", FG)],
]

H = TOP + len(lines) * LH + PAD
out = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
    f'<rect width="{W}" height="{H}" rx="10" fill="#1e1e1e"/>',
    '<circle cx="20" cy="18" r="6" fill="#ff5f57"/><circle cx="40" cy="18" r="6" fill="#febc2e"/>'
    '<circle cx="60" cy="18" r="6" fill="#28c840"/>',
    '<g font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="13" xml:space="preserve" style="white-space:pre">',
]
for i, spans in enumerate(lines):
    y = TOP + i * LH + 12
    tspans = ""
    for t, c in spans:
        weight = ' font-weight="bold"' if c == BOLD else ""
        tspans += f'<tspan fill="{c}"{weight}>{escape(t)}</tspan>'

    out.append(f'<text x="{PAD}" y="{y}" xml:space="preserve">{tspans}</text>')
out += ["</g>", "</svg>"]

open("docs/demo.svg", "w").write("\n".join(out) + "\n")
print(f"wrote docs/demo.svg ({W}x{H})")
