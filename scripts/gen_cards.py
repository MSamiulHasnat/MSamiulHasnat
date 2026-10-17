import sys, os
OUT = sys.argv[1]

STYLE = """<style>
.bg{fill:#0B1020}.edge{stroke:#1F2B4D}.ink{fill:#F1F5F9}.muted{fill:#94A3B8}.dim{fill:#64748B}
.accent{fill:#5EEAD4}.violet{fill:#A78BFA}.amber{fill:#FBBF24}.green{fill:#4ADE80}
.chip{fill:#131C38;stroke:#24335C}.chiptext{fill:#CBD5E1}.faint{fill:#1A2444}.fstroke{stroke:#1F2B4D;fill:none}
.win{fill:#111832;stroke:#24335C}.blk{fill:#1E2A4A}.blk2{fill:#2A3A66}
.sans{font-family:ui-sans-serif,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif}
.mono{font-family:ui-monospace,'SF Mono','Cascadia Code',Consolas,monospace}
.pulse{animation:p 1.8s ease-in-out infinite}@keyframes p{50%{opacity:.25}}
@media (prefers-color-scheme: light){
.bg{fill:#FFFFFF}.edge{stroke:#DCE3EE}.ink{fill:#0F172A}.muted{fill:#475569}.dim{fill:#64748B}
.accent{fill:#0D9488}.violet{fill:#7C3AED}.amber{fill:#D97706}.green{fill:#16A34A}
.chip{fill:#F1F5F9;stroke:#DCE3EE}.chiptext{fill:#334155}.faint{fill:#EEF2F7}.fstroke{stroke:#E2E8F0}
.win{fill:#F8FAFC;stroke:#DCE3EE}.blk{fill:#E2E8F0}.blk2{fill:#CBD5E1}
}
</style>"""

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def chips(items, x, y):
    out = []
    for t in items:
        w = round(len(t) * 7.4 + 22)
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="28" rx="8" class="chip"/>'
                   f'<text x="{x+11}" y="{y+19}" class="mono chiptext" font-size="12.5">{esc(t)}</text>')
        x += w + 8
    return "".join(out)

def pill(text, x_right, y, cls, dot=True):
    w = round(len(text) * 7.6 + (40 if dot else 24))
    x = x_right - w
    s = f'<rect x="{x}" y="{y}" width="{w}" height="28" rx="14" class="chip"/>'
    tx = x + 12
    if dot:
        s += f'<circle cx="{x+16}" cy="{y+14}" r="4.5" class="{cls} pulse"/>'
        tx = x + 28
    s += f'<text x="{tx}" y="{y+19}" class="mono {cls}" font-size="12.5" font-weight="700" letter-spacing="1">{esc(text)}</text>'
    return s

def card(name, w, h, idx, accent, status, title, desc, body, chip_items, art="", label=""):
    grad = {"accent": ("#5EEAD4", "#A78BFA"), "violet": ("#A78BFA", "#5EEAD4"), "amber": ("#FBBF24", "#A78BFA")}[accent]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(label or title)}">
{STYLE}
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{grad[0]}"/><stop offset="1" stop-color="{grad[1]}"/></linearGradient>
<clipPath id="c"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="22"/></clipPath></defs>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="22" class="bg edge" stroke-width="1.5"/>
<g clip-path="url(#c)">{art}<rect x="1" y="1" width="5" height="{h}" fill="url(#g)"/></g>
<text x="40" y="58" class="mono {accent}" font-size="15" font-weight="700">{idx}</text>
<text x="72" y="58" class="mono dim" font-size="15">/ project</text>
{pill(status[0], w - 32, 38, status[1], status[2])}
<text x="38" y="110" class="sans ink" font-size="36" font-weight="800" letter-spacing="-0.8">{esc(title)}</text>
'''
    y = 146
    for line in desc:
        svg += f'<text x="40" y="{y}" class="sans muted" font-size="16.5">{esc(line)}</text>\n'
        y += 25
    svg += body
    svg += chips(chip_items, 40, h - 62)
    svg += "\n</svg>\n"
    open(os.path.join(OUT, name), "w", encoding="utf8").write(svg)

def bullets(lines, y0, cls):
    s = ""
    for i, t in enumerate(lines):
        y = y0 + i * 28
        s += f'<rect x="40" y="{y-10}" width="8" height="8" rx="2" class="{cls}"/><text x="60" y="{y}" class="sans ink" font-size="15.5">{esc(t)}</text>\n'
    return s

# 01 EASTARCH (wide): a browser frame that auto-scrolls through a real
# full-page capture of the live site (scripts/eastarch-site.jpg, refreshed
# with scripts/capture_site.mjs). Embedded as base64 because SVGs rendered
# through <img> on GitHub cannot load external images.
import base64
from PIL import Image
SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eastarch-site.jpg")
sw, sh = Image.open(SITE).size
site_b64 = base64.b64encode(open(SITE, "rb").read()).decode()

BX, BY, BW, BH, BAR = 690, 84, 476, 330, 38      # browser frame geometry
VW, VH = BW, BH - BAR                            # viewport inside the frame
IH = round(sh * VW / sw)                          # image height at viewport width
travel = IH - VH
thumb = max(24, round(VH * VH / IH))
DUR = "26s"
KT = "0;.08;.84;.92;1"                            # hold top, scroll down, hold, scroll back up
SPL = ".4 0 .6 1;.45 0 .55 1;.4 0 .6 1;.6 0 .4 1"
browser = f'''<defs><clipPath id="vp"><path d="M{BX} {BY+BAR}h{VW}v{VH-14}a14 14 0 0 1-14 14h-{VW-28}a14 14 0 0 1-14-14z"/></clipPath></defs>
<rect x="{BX}" y="{BY}" width="{BW}" height="{BH}" rx="14" class="win"/>
<g clip-path="url(#vp)">
  <image x="{BX}" y="{BY+BAR}" width="{VW}" height="{IH}" preserveAspectRatio="none" href="data:image/jpeg;base64,{site_b64}">
    <animateTransform attributeName="transform" type="translate" dur="{DUR}" repeatCount="indefinite"
      calcMode="spline" keyTimes="{KT}" keySplines="{SPL}" values="0 0;0 0;0 -{travel};0 -{travel};0 0"/>
  </image>
  <rect x="{BX+BW-7}" y="{BY+BAR+2}" width="4" height="{thumb}" rx="2" fill="#0B1020" opacity=".35">
    <animateTransform attributeName="transform" type="translate" dur="{DUR}" repeatCount="indefinite"
      calcMode="spline" keyTimes="{KT}" keySplines="{SPL}" values="0 0;0 0;0 {VH-thumb-4};0 {VH-thumb-4};0 0"/>
  </rect>
</g>
<rect x="{BX}" y="{BY}" width="{BW}" height="{BH}" rx="14" fill="none" class="edge" stroke-width="1.5"/>
<line x1="{BX}" x2="{BX+BW}" y1="{BY+BAR}" y2="{BY+BAR}" class="edge" stroke-width="1"/>
<circle cx="{BX+20}" cy="{BY+19}" r="5" fill="#F87171"/><circle cx="{BX+37}" cy="{BY+19}" r="5" fill="#FBBF24"/><circle cx="{BX+54}" cy="{BY+19}" r="5" fill="#4ADE80"/>
<rect x="{BX+76}" y="{BY+9}" width="{BW-96}" height="20" rx="10" class="blk"/>
<text x="{BX+92}" y="{BY+23.5}" class="mono dim" font-size="11.5">🔒 eastarchconsulting.com</text>'''
visit = ('<text x="40" y="330" class="mono accent" font-size="14" font-weight="700">→ eastarchconsulting.com</text>'
         '<text x="250" y="330" class="mono dim" font-size="13">  · live capture, auto-scrolling</text>')
card("card-eastarch.svg", 1200, 440, "01", "accent", ("LIVE", "green", True),
     "EASTARCH Consulting",
     ["Production website for a consultancy that helps international",
      "students study in China, with a student portal for applications."],
     bullets(["Editors manage every page through Sanity CMS",
              "Student portal for application documents, with admin and staff roles",
              "Deployed to Vercel automatically on every push to main"], 222, "accent") + visit,
     ["Next.js 16", "React 19", "TypeScript", "Tailwind v4", "Sanity", "Vercel"], art=browser,
     label="EASTARCH Consulting: production website and student portal")

# 02 HSK ShiFu
han = '<text x="560" y="250" text-anchor="end" class="sans faint" font-size="240" font-weight="900">汉</text>'
card("card-hsk.svg", 600, 380, "02", "violet", ("OPEN SOURCE", "violet", False),
     "HSK ShiFu",
     ["A Chinese tutor that only teaches what's in the",
      "textbook, and cites the page for every answer."],
     bullets(["1,708-node knowledge graph of HSK 1–3",
              "Practice sessions with tutor 王老师",
              "Runs locally or on Claude"], 222, "violet"),
     ["Python", "FastAPI", "Knowledge Graph", "Ollama", "Claude"], art=han,
     label="HSK ShiFu: textbook-grounded Chinese tutor")

# 03 CT-MUSIQ
rings = '<g transform="translate(600 70)">' + "".join(
    f'<circle r="{r}" class="fstroke" stroke-width="10"/>' for r in (40, 80, 120, 160)) + '</g>'
metrics = ""
for i, (v, k) in enumerate([("0.844", "PLCC"), ("0.842", "SROCC"), ("6 GB", "GPU budget")]):
    x = 40 + i * 176
    metrics += (f'<text x="{x}" y="240" class="sans ink" font-size="38" font-weight="800" letter-spacing="-1">{v}</text>'
                f'<text x="{x+2}" y="266" class="mono dim" font-size="12.5" letter-spacing="1.5">{k.upper()}</text>')
card("card-ctmusiq.svg", 600, 380, "03", "amber", ("B.ENG THESIS", "amber", False),
     "CT-MUSIQ",
     ["No-reference quality assessment for low-dose CT.",
      "A multi-scale ViT that predicts radiologist scores."],
     metrics,
     ["PyTorch", "ViT-B/32", "Medical Imaging", "LDCTIQAG"], art=rings,
     label="CT-MUSIQ: low-dose CT image quality assessment, PLCC 0.844")

# 04 Time Survivor (wide, compact)
scene = '''<g transform="translate(760 0)">
<rect x="0" y="236" width="440" height="80" class="faint"/>
<rect x="40" y="196" width="110" height="16" rx="3" class="blk2"/>
<rect x="210" y="150" width="90" height="16" rx="3" class="blk2"/>
<rect x="340" y="110" width="80" height="16" rx="3" class="blk2"/>
<g><rect width="22" height="30" rx="4" fill="#FBBF24"/><rect x="13" y="7" width="5" height="5" fill="#0B1020"/>
<animateTransform attributeName="transform" type="translate" dur="3.2s" repeatCount="indefinite"
 values="30 206; 95 166; 120 166; 230 120; 255 120; 350 80; 375 80; 30 206"
 keyTimes="0;.18;.28;.48;.58;.78;.9;1"/></g>
<g class="mono dim" font-size="13"><text x="20" y="40">TIME 00:42</text></g>
</g>'''
card("card-timesurvivor.svg", 1200, 330, "04", "amber", ("GAME", "amber", False),
     "Time Survivor",
     ["A 2D platformer built from scratch in C++ and SFML: a state-machine",
      "player controller, AABB physics, a following camera, and timed levels."],
     "",
     ["C++", "SFML", "OOP", "Game Loop", "Physics"], art=scene,
     label="Time Survivor: 2D platformer in C++ and SFML")
print("ok")
