import sys, os, importlib.util
OUT = sys.argv[1]
spec = importlib.util.spec_from_file_location("g", os.path.join(os.path.dirname(__file__), "gen_cards.py"))
sys.argv = [sys.argv[0], OUT]
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)

rows = [
    ("AI / ML", "accent", ["PyTorch", "TensorFlow", "Vision Transformers", "LLM Agents", "Knowledge Graphs"]),
    ("Languages", "violet", ["Python", "C++", "C", "TypeScript", "Rust", "Dart"]),
    ("Web & Apps", "amber", ["Next.js", "React", "Tailwind CSS", "FastAPI", "Sanity", "Flutter"]),
    ("Tooling", "accent", ["Git", "Vercel", "Ollama", "Claude Code", "VS Code", "Android Studio"]),
]
W, H = 1200, 340
s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Tech stack">\n{g.STYLE}\n'
s += f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="22" class="bg edge" stroke-width="1.5"/>\n'
for i, (label, cls, items) in enumerate(rows):
    y = 52 + i * 70
    s += f'<text x="44" y="{y+23}" class="mono dim" font-size="13" font-weight="700" letter-spacing="2">{g.esc(label.upper())}</text>'
    x = 220
    for t in items:
        w = round(len(t) * 7.9 + 46)
        s += (f'<rect x="{x}" y="{y}" width="{w}" height="36" rx="18" class="chip"/>'
              f'<circle cx="{x+19}" cy="{y+18}" r="4.5" class="{cls}"/>'
              f'<text x="{x+32}" y="{y+23.5}" class="sans chiptext" font-size="15" font-weight="600">{g.esc(t)}</text>')
        x += w + 10
    if i < len(rows) - 1:
        s += f'<line x1="44" x2="{W-44}" y1="{y+53}" y2="{y+53}" class="fstroke" stroke-width="1" stroke-dasharray="3 6"/>'
    s += "\n"
s += "</svg>\n"
open(os.path.join(OUT, "stack.svg"), "w", encoding="utf8").write(s)

f = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 110" width="1200" height="110" role="img" aria-label="Thanks for visiting">
{g.STYLE}
<defs><linearGradient id="b" x1="0" x2="1"><stop offset="0" stop-color="#5EEAD4"/><stop offset=".5" stop-color="#A78BFA"/><stop offset="1" stop-color="#FBBF24"/></linearGradient></defs>
<rect x="0" y="20" width="1200" height="3" rx="1.5" fill="url(#b)"/>
<text x="600" y="76" text-anchor="middle" class="mono dim" font-size="16">~/samiul $ <tspan class="accent">exit</tspan>  <tspan class="muted">— thanks for stopping by</tspan><tspan class="ink pulse"> ▍</tspan></text>
</svg>
'''
open(os.path.join(OUT, "footer.svg"), "w", encoding="utf8").write(f)
print("ok2")
