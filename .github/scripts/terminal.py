#!/usr/bin/env python3

# Regenerate assets/terminal.svg from the LINES below.
#
#   python3 .github/scripts/terminal.py
#
# Edit LINES, run the script, and commit the new SVG. Each entry is one row:
#   ("cmd", "whoami")                         a prompt, then the command typed out
#   ("out", [("text", "color"), ...])         an output row, made of coloured parts
#   ("gap",)                                  an empty row
# The last row is always an empty prompt with a blinking cursor.
# Rows are 8.4px per character; keep each row under ~110 characters.

from html import escape
from pathlib import Path

USER, HOST = "yixian", "cloud"

FG = "#e5e7eb"
MUTED = "#94a3b8"
GREEN = "#34d399"
BLUE = "#38bdf8"
PURPLE = "#a78bfa"
AMBER = "#fbbf24"
QUOTE = "#fde68a"

LINES = [
    ("cmd", "whoami"),
    ("out", [("Yi Xian", FG), (" — cloud & infrastructure on AWS · Malaysia", MUTED)]),
    ("cmd", "cat focus.txt"),
    ("out", [("cloud infrastructure", BLUE), ("  ·  ", MUTED), ("networking & security", GREEN),
             ("  ·  ", MUTED), ("agentic AI", PURPLE)]),
    ("cmd", "aws certs --list"),
    ("out", [("  ✓ ", GREEN), ("Cloud Practitioner (CLF-C02) ........... ", FG), ("1000/1000", GREEN)]),
    ("out", [("  ~ ", AMBER), ("Solutions Architect – Associate ........ ", FG), ("in progress", AMBER)]),
    ("cmd", "echo $MOTTO"),
    ("out", [('"Keep it simple. Make it secure. Build it to scale."', QUOTE)]),
]

# Read by screen readers and shown when the image fails to load.
LABEL = ("Terminal: whoami — Yi Xian, cloud and infrastructure on AWS. "
         "AWS Cloud Practitioner 1000/1000, Solutions Architect Associate in progress.")

WIDTH = 1000
CHAR = 8.4           # width of one character at font-size 14
LEFT = 30.0
TOP = 78             # baseline of the first row
ROW = 25
START = 0.50         # when the first prompt appears
TYPE_DELAY = 0.50    # pause between a prompt appearing and typing starting
AFTER_CMD = 0.41     # pause between the last keystroke and the output
NEXT_OUT = 0.06      # between consecutive output rows
NEXT_CMD = 0.30      # between the last output row and the next prompt
KEYS = [0.063, 0.115, 0.083, 0.057, 0.105, 0.069, 0.130, 0.087, 0.055, 0.093, 0.075, 0.100]

HEAD = """\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{label}">
<title>whoami</title>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1020"/><stop offset="1" stop-color="#121b3d"/></linearGradient>
  <linearGradient id="brand" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#38bdf8"/><stop offset="1" stop-color="#a78bfa"/></linearGradient>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1" fill="#5b6fa8" fill-opacity=".22"/></pattern>
  <radialGradient id="glowC"><stop offset="0" stop-color="#38bdf8" stop-opacity=".35"/><stop offset="1" stop-color="#38bdf8" stop-opacity="0"/></radialGradient>
  <radialGradient id="glowV"><stop offset="0" stop-color="#a78bfa" stop-opacity=".35"/><stop offset="1" stop-color="#a78bfa" stop-opacity="0"/></radialGradient><clipPath id="tc"><rect width="{w}" height="{h}" rx="14"/></clipPath></defs>
<style>
  .mono {{ font-family: ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace; }} .sans {{ font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Roboto,Helvetica,Arial,sans-serif; }}
  .fade {{ opacity: 0; animation: fade .7s ease-out forwards; }}
  @keyframes fade {{ to {{ opacity: 1; }} }}
  .up {{ opacity: 0; animation: up .8s cubic-bezier(.2,.8,.2,1) forwards; }}
  @keyframes up {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: none; }} }}
  .pulse {{ animation: pulse 2.2s ease-in-out infinite; }}
  @keyframes pulse {{ 0%,100% {{ opacity: .35; }} 50% {{ opacity: 1; }} }}
  .breathe {{ animation: breathe 7s ease-in-out infinite; }}
  @keyframes breathe {{ 0%,100% {{ opacity: .55; }} 50% {{ opacity: 1; }} }}
  .blink {{ animation: blink 1s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  .flow {{ stroke-dasharray: 4 6; animation: flow 1.2s linear infinite; }}
  @keyframes flow {{ to {{ stroke-dashoffset: -20; }} }}
  .draw {{ stroke-dasharray: 1.02; stroke-dashoffset: 1.02; animation: draw 1.6s ease-out forwards; }}
  @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
  .ring {{ transform-box: fill-box; transform-origin: center; animation: ring 2s ease-out infinite; }}
  @keyframes ring {{ from {{ transform: scale(1); opacity: .8; }} to {{ transform: scale(2.1); opacity: 0; }} }}
  @media (prefers-reduced-motion: reduce) {{
    .fade, .up {{ animation: none; opacity: 1; }}
    .draw {{ animation: none; stroke-dashoffset: 0; }}
    .pulse, .breathe, .blink, .flow, .ring {{ animation: none; }}
  }}</style>
<g clip-path="url(#tc)"><rect width="{w}" height="{h}" fill="#0a0f1e"/><rect width="{w}" height="{h}" fill="url(#dots)" opacity=".5"/>
<rect width="{w}" height="38" fill="#141b33"/><path d="M0 38.5H{w}" stroke="#26314f"/></g>
<rect x=".5" y=".5" width="{w1}" height="{h1}" rx="13.5" fill="none" stroke="#334155" stroke-opacity=".8"/>
<circle cx="24" cy="19" r="6" fill="#ff5f57"/><circle cx="44" cy="19" r="6" fill="#febc2e"/><circle cx="64" cy="19" r="6" fill="#28c840"/>
<text x="{mid}" y="23.5" class="mono" font-size="12" fill="#94a3b8" text-anchor="middle">{user}@{host}: ~</text>
"""


def text(x, y, s, color, extra=""):
    return (f'<text x="{x:.1f}" y="{y}" class="mono" font-size="14" fill="{color}"{extra}>'
            f"{escape(s, quote=False)}</text>")


def segments(y, parts):
    """Coloured parts laid out left to right, each pinned to its exact monospace width."""
    out, x = [], LEFT
    for s, color in parts:
        w = CHAR * len(s)
        out.append(text(x, y, s, color,
                        f' textLength="{w:.1f}" lengthAdjust="spacingAndGlyphs" xml:space="preserve"'))
        x += w
    return "".join(out)


def appear(at, body):
    return f'<g opacity="0"><set attributeName="opacity" to="1" begin="{at:.2f}s" fill="freeze"/>{body}</g>'


def main():
    prompt = [(f"{USER}@{HOST}", GREEN), (":", MUTED), ("~", BLUE), ("$ ", FG)]
    cmd_x = LEFT + CHAR * sum(len(s) for s, _ in prompt)
    rows = LINES + [("prompt",)]
    height = TOP + ROW * (len(rows) - 1) + 29

    body = []
    cursor = [(0.0, cmd_x + 1, TOP - 13)]  # (time, x, y) stops for the cursor
    t = START
    key = 0
    prev = None
    for i, row in enumerate(rows):
        y = TOP + ROW * i
        kind = row[0]
        if kind in ("cmd", "prompt"):
            if prev == "out":
                t += NEXT_CMD - NEXT_OUT
            body.append(appear(t, segments(y, prompt)))
            cursor.append((t, cmd_x + 1, y - 13))
            if kind == "prompt":
                break
            t += TYPE_DELAY
            for c, ch in enumerate(row[1]):
                x = cmd_x + CHAR * c
                if ch != " ":
                    body.append(text(x, y, ch, FG, ' opacity="0"')[:-7]
                                + f'<set attributeName="opacity" to="1" begin="{t:.3f}s" fill="freeze"/></text>')
                cursor.append((t, x + CHAR + 1, y - 13))
                t += KEYS[key % len(KEYS)]
                key += 1
            t += AFTER_CMD - KEYS[(key - 1) % len(KEYS)]
        elif kind == "out":
            body.append(appear(t, segments(y, row[1])))
            t += NEXT_OUT
        prev = kind

    end = cursor[-1][0]
    times = ";".join(f"{c[0] / end:.4f}" for c in cursor[:-1]) + ";0.9999;1"
    xs = ";".join(f"{c[1]:.1f}" for c in cursor) + f";{cursor[-1][1]:.1f}"
    ys = ";".join(str(c[2]) for c in cursor) + f";{cursor[-1][2]}"
    anim = f'keyTimes="{times}" dur="{end:.3f}s" calcMode="discrete" fill="freeze"'
    body.append(
        f'<rect x="{cmd_x + 1:.1f}" y="{TOP - 13}" width="9" height="17" fill="{BLUE}" opacity="0">'
        f'<set attributeName="opacity" to="1" begin="{START:.2f}s"/>'
        f'<animate attributeName="x" values="{xs}" {anim}/>'
        f'<animate attributeName="y" values="{ys}" {anim}/>'
        f'<animate attributeName="opacity" values="1;0" dur="1.06s" begin="{end + 0.5:.2f}s" '
        f'calcMode="discrete" repeatCount="indefinite"/></rect>'
    )

    svg = HEAD.format(w=WIDTH, h=height, w1=WIDTH - 1, h1=height - 1, mid=f"{WIDTH / 2:.1f}",
                      label=escape(LABEL), user=USER, host=HOST)
    svg += "\n".join(body) + "\n</svg>\n"

    out = Path(__file__).resolve().parents[2] / "assets" / "terminal.svg"
    out.write_text(svg)
    print(f"Updated {out}")


if __name__ == "__main__":
    main()
