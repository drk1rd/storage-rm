#!/usr/bin/env python3
"""Render docs/demo.gif: an animated terminal session of example `storage-rm` output.

Frames are drawn directly with Pillow (no screen recording needed):
    python3 docs/make-demo.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).with_name("demo.gif")

W, ROWS, LH, PAD, TOP = 900, 26, 20, 20, 44
H = TOP + ROWS * LH + PAD
BG, BAR = "#1e1e1e", "#2a2a2a"
FG, DIM, BOLD, CYAN, GREEN, YELLOW = "#d4d4d4", "#7a7a7a", "#ffffff", "#4fc1ff", "#6ad07a", "#e5c07b"

FONT = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 13, index=0)
FONT_B = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 13, index=1)
CW = FONT.getlength("M")

DEFAULT = [
    ("docker", "40.1G", "Docker build cache + dangling images (containers and volumes kept)"),
    ("xcode", "12.3G", "Xcode DerivedData, older iOS DeviceSupport, simulator caches"),
    ("gradle", "6.9G", "Gradle caches, daemon logs, old wrapper distributions"),
    ("npm", "3.8G", "npm cache and npx cache"),
    ("pnpm", "1.7G", "pnpm content store"),
    ("brew", "291.0M", "Homebrew download cache and old versions"),
    ("app-caches", "8.9G", "App caches: Spotify, browsers, VS Code, Cursor, Slack, …"),
    ("claude", "2.6G", "Claude desktop simulator builds"),
]
OPTIN = [
    ("android-avd", "10.6G", "Android emulators (AVDs) and SDK system images"),
    ("node-modules", "3.1G", "node_modules in projects untouched for --days"),
]


def row(name, size, what):
    return [(f"  {name:<15} {size:>8}  ", FG), (what, DIM)]


def render(lines, cursor=False):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 34], fill=BAR)
    for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        d.ellipse([14 + i * 20, 11, 26 + i * 20, 23], fill=c)
    d.text((W / 2, 17), "storage-rm — zsh", fill=DIM, font=FONT, anchor="mm")

    visible = lines[-ROWS:]
    for i, spans in enumerate(visible):
        x, y = PAD, TOP + i * LH
        for text, color in spans:
            d.text((x, y), text, fill=color, font=FONT_B if color == BOLD else FONT)
            x += CW * len(text)
        if cursor and i == len(visible) - 1:
            d.rectangle([x + 1, y, x + CW, y + 15], fill=FG)
    return img


frames, durations = [], []


def shot(lines, ms, cursor=False):
    frames.append(render(lines, cursor))
    durations.append(ms)


def type_cmd(lines, cmd):
    """Type a command at a prompt, one character per frame."""
    for n in range(len(cmd) + 1):
        shot(lines + [[("$ ", DIM), (cmd[:n], BOLD)]], 55 if n else 500, cursor=True)
    shot(lines + [[("$ ", DIM), (cmd, BOLD)]], 350, cursor=True)
    return lines + [[("$ ", DIM), (cmd, BOLD)]]


# Scene 1: scan
screen = type_cmd([], "storage-rm")
screen += [[("==>", CYAN), (" Scanning (nothing is deleted)…", FG)]]
shot(screen, 600)
screen += [[], [("  " + f"{'CATEGORY':<15} {'SIZE':>8}  WHAT", BOLD)]]
for r in DEFAULT:
    screen.append(row(*r))
    shot(screen, 120)
screen.append([("  opt-in", YELLOW)])
for r in OPTIN:
    screen.append(row(*r))
    shot(screen, 120)
screen += [
    [],
    [("  ", FG), ("clean", BOLD), (" would free about ", FG), ("76.6G", GREEN), (" — 573.2G available now", FG)],
    [("  opt-in categories hold another ", FG), ("13.7G", YELLOW), (" (use -o name or --all)", FG)],
]
shot(screen, 3200)

# Scene 2: clean
screen = type_cmd([], "storage-rm clean -y")
screen += [[("==>", CYAN), (" Planned cleanup:", FG)]]
screen += [row(*r) for r in DEFAULT]
screen += [[("  total ≈ 76.6G", BOLD)], []]
shot(screen, 1400)
for name, _, _ in DEFAULT:
    screen.append([("==>", CYAN), (f" {name}", FG)])
    shot(screen, 380)
screen += [[], [("Freed 76.6G", GREEN), (" — 649.8G available now.", FG)]]
shot(screen, 4000)

frames[0].save(
    OUT,
    save_all=True,
    append_images=frames[1:],
    duration=durations,
    loop=0,
    optimize=True,
)
print(f"wrote {OUT} ({W}x{H}, {len(frames)} frames, {OUT.stat().st_size // 1024} KB)")
