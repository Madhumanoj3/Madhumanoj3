"""Generate assets/activity-graph.svg: a 30-day GitHub contribution area chart."""
import json, os, urllib.request
from datetime import date, timedelta

USER = os.environ.get("GH_USER", "Madhumanoj3")
TOKEN = os.environ["GH_TOKEN"]
DAYS = 30

query = """query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{
totalContributions weeks{contributionDays{date contributionCount}}}}}}"""
req = urllib.request.Request(
    "https://api.github.com/graphql",
    data=json.dumps({"query": query, "variables": {"u": USER}}).encode(),
    headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json", "User-Agent": "activity-graph"},
)
cal = json.load(urllib.request.urlopen(req))["data"]["user"]["contributionsCollection"]["contributionCalendar"]
counts = {d["date"]: d["contributionCount"] for w in cal["weeks"] for d in w["contributionDays"]}
today = date.today()
days = [today - timedelta(days=i) for i in range(DAYS - 1, -1, -1)]
vals = [counts.get(d.isoformat(), 0) for d in days]

W, H, L, R, T, B = 760, 300, 52, 24, 70, 44
top = max(max(vals), 4)
top += (-top) % 2
pw, ph = W - L - R, H - T - B
pts = [(L + pw * i / (DAYS - 1), T + ph * (1 - v / top)) for i, v in enumerate(vals)]

def smooth(p):
    d = f"M{p[0][0]:.1f},{p[0][1]:.1f}"
    for (x0, y0), (x1, y1) in zip(p, p[1:]):
        cx = (x0 + x1) / 2
        d += f" C{cx:.1f},{y0:.1f} {cx:.1f},{y1:.1f} {x1:.1f},{y1:.1f}"
    return d

line = smooth(pts)
area = f"{line} L{pts[-1][0]:.1f},{T + ph} L{pts[0][0]:.1f},{T + ph} Z"
grid = "".join(
    f'<line x1="{L}" x2="{W - R}" y1="{T + ph * (1 - k / 4):.1f}" y2="{T + ph * (1 - k / 4):.1f}" stroke="#22d3ee" stroke-opacity=".12"/>'
    f'<text x="{L - 10}" y="{T + ph * (1 - k / 4) + 4:.1f}" text-anchor="end" class="ax">{round(top * k / 4)}</text>'
    for k in range(5)
)
xl = "".join(
    f'<text x="{pts[i][0]:.1f}" y="{H - 18}" text-anchor="middle" class="ax">{days[i].day} {days[i].strftime("%b")}</text>'
    for i in range(0, DAYS, 5)
)
dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="#0b0d14" stroke="#22d3ee" stroke-width="2"><title>{d.isoformat()}: {v}</title></circle>' for (x, y), d, v in zip(pts, days, vals) if v)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs><linearGradient id="a" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#22d3ee" stop-opacity=".45"/><stop offset="1" stop-color="#818cf8" stop-opacity="0"/></linearGradient>
<linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="#22d3ee"/><stop offset="1" stop-color="#818cf8"/></linearGradient></defs>
<style>text{{font-family:-apple-system,"Segoe UI",Roboto,sans-serif}}.ax{{font-size:11px;fill:#94a3b8}}.t{{font-size:17px;font-weight:700;fill:#22d3ee}}.s{{font-size:12px;fill:#94a3b8}}</style>
<rect width="{W}" height="{H}" rx="12" fill="#0b0d14" stroke="#22d3ee" stroke-opacity=".5"/>
<text x="{L}" y="32" class="t">{USER} — Contribution Activity</text>
<text x="{L}" y="52" class="s">Last {DAYS} days: {sum(vals)} contributions · {cal["totalContributions"]} in the past year · updated {today.isoformat()}</text>
{grid}{xl}
<path d="{area}" fill="url(#a)"/><path d="{line}" fill="none" stroke="url(#l)" stroke-width="3" stroke-linecap="round"/>{dots}
</svg>'''
os.makedirs("assets", exist_ok=True)
open("assets/activity-graph.svg", "w", encoding="utf-8").write(svg)
print("ok", sum(vals), max(vals))
