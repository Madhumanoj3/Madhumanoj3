"""Generate assets/dev_coding.svg: dark-room developer scene.
Loop (9s): lights up -> hands open laptop -> types behind it -> hands close it -> total blackout."""
T = 9.0
EASE, LIN = "0.4 0 0.2 1", "0 0 1 1"
LID_BOTTOM, LID_H = 362, 62          # lid is scaled about its bottom edge
OPEN_T, OPEN_END, CLOSE_T, CLOSE_END = 0.8, 1.7, 4.4, 5.3
KT = lambda t: round(t / T, 4)


def keyframes(bob, layer):
    """(time, x, y, spline-to-next) for the left hand; the right hand mirrors about x=360."""
    top_closed, top_open = 354, 300
    if layer == "F":
        f = [(0, 272, 372, LIN), (0.25, 272, 372, LIN), (OPEN_T, 292, top_closed, EASE),
             (OPEN_END, 292, top_open, LIN), (2.1, 268, 332, LIN), (4.0, 268, 332, LIN),
             (CLOSE_T, 292, top_open, EASE), (CLOSE_END, 292, top_closed, LIN),
             (5.7, 272, 372, LIN), (T, 272, 372, LIN)]
    else:
        f = [(0, 268, 332, LIN), (2.1, 268, 332, LIN), (2.4, 322, 346, LIN)]
        t, up = 2.4 + bob, True
        if bob > 0:
            f.append((round(t, 3), 322, 346, LIN))
        while t + 0.15 <= 3.6:
            t = round(t + 0.15, 3)
            f.append((t, 322, 340 if up else 346, LIN))
            up = not up
        f += [(3.7, 322, 346, LIN), (4.0, 268, 332, LIN), (T, 268, 332, LIN)]
    out, last = [], -1
    for fr in f:
        if fr[0] > last:
            out.append(fr)
            last = fr[0]
    return out


HAND = """<rect x="-14.5" y="-21" width="29" height="14" rx="7" fill="#c2410c" />
          <path d="M-12 -8 Q0 -4 12 -8" stroke="#fdba74" stroke-width="1.6" fill="none" stroke-linecap="round" />
          <path d="M-10 -1 Q-19 1 -18.5 11" stroke="#ffb86b" stroke-width="7.5" fill="none" stroke-linecap="round" />
          <g stroke="#ffb86b" stroke-width="6.6" stroke-linecap="round" fill="none">
            <path d="M-9.3 8 L-9.3 20" /><path d="M-3.1 8 L-3.1 24" /><path d="M3.1 8 L3.1 22" /><path d="M9.3 8 L9.3 17" />
          </g>
          <g stroke="#e8924a" stroke-width="0.9" stroke-linecap="round" stroke-opacity="0.8">
            <path d="M-6.2 12 L-6.2 22" /><path d="M0 12 L0 24" /><path d="M6.2 12 L6.2 19" />
          </g>
          <path d="M-12.5 -8 Q-15 6 -10.5 12.5 L10.5 12.5 Q15 6 12.5 -8 Z" fill="#ffb86b" />
          <path d="M-7 8 q1.5 2 3.4 0 M-1.4 8 q1.5 2 3.4 0 M4.2 8 q1.5 2 3.4 0" stroke="#e8924a" stroke-width="1" fill="none" stroke-linecap="round" />
          <ellipse cx="-4" cy="-2" rx="4.5" ry="2.6" fill="#ffd9b8" opacity="0.55" />"""


def arm_hand(side, bob, layer):
    fr = keyframes(bob, layer)
    kts = ";".join(str(KT(t)) for t, *_ in fr)
    spl = ";".join(sp for *_, sp in fr[:-1])
    mir = (lambda x: x) if side == "L" else (lambda x: 720 - x)
    pts = [(mir(x), y) for _, x, y, _ in fr]
    sx = 292 if side == "L" else 428
    ox = -10 if side == "L" else 10
    d = lambda x, y: f"M{sx} 272 Q{sx + ox} {round((272 + y) / 2 + 10)} {x} {y - 9}"
    common = f'dur="{T}s" repeatCount="indefinite" calcMode="spline" keyTimes="{kts}" keySplines="{spl}"'
    flip = "scale(-0.72,0.72)" if side == "R" else "scale(0.72,0.72)"
    dvals = ";".join(d(x, y) for x, y in pts)
    tvals = ";".join(f"{x} {y}" for x, y in pts)
    return f"""      <path d="{d(*pts[0])}" fill="none" stroke="url(#skin)" stroke-width="18" stroke-linecap="round" stroke-linejoin="round">
        <animate attributeName="d" {common} values="{dvals}" />
      </path>
      <g>
        <animateTransform attributeName="transform" type="translate" {common} values="{tvals}" />
        <g transform="{flip}">
          {HAND}
        </g>
      </g>
"""


def layer(kind, label):
    vis = "1;0;1;1" if kind == "F" else "0;1;0;0"
    return f"""    <!-- {label} -->
    <g opacity="{vis.split(";")[0]}">
      <animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;{KT(2.1)};{KT(4.0)};1" values="{vis}" />
{arm_hand("L", 0, kind)}{arm_hand("R", 0.15, kind)}    </g>
"""


lidkt = f"0;{KT(OPEN_T)};{KT(OPEN_END)};{KT(CLOSE_T)};{KT(CLOSE_END)};1"
LID_Y = LID_BOTTOM - LID_H
LID_MID = LID_BOTTOM - LID_H // 2

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 410" width="720" height="410">
  <defs>
    <radialGradient id="wall" cx="50%" cy="62%" r="52%">
      <stop offset="0%" stop-color="#6d4aff" stop-opacity="0.95" />
      <stop offset="45%" stop-color="#4129b8" stop-opacity="0.7" />
      <stop offset="100%" stop-color="#07060d" stop-opacity="0" />
    </radialGradient>
    <linearGradient id="body" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffb347" /><stop offset="100%" stop-color="#f26a1b" />
    </linearGradient>
    <linearGradient id="skin" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ff9a3d" /><stop offset="100%" stop-color="#ea580c" />
    </linearGradient>
    <linearGradient id="face" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffb066" /><stop offset="100%" stop-color="#f97316" />
    </linearGradient>
    <linearGradient id="hair" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ec4899" /><stop offset="100%" stop-color="#be185d" />
    </linearGradient>
    <linearGradient id="lidg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#14111f" /><stop offset="100%" stop-color="#07060d" />
    </linearGradient>
    <filter id="neon"><feGaussianBlur stdDeviation="2" result="b" /><feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge></filter>
  </defs>
  <style>
    .sym {{ font-family: "Fira Code", Consolas, monospace; font-weight: 700; }}
    .f1 {{ animation: fl 4s ease-in-out infinite; }} .f2 {{ animation: fl 5s ease-in-out infinite -1.2s; }}
    .f3 {{ animation: fl 3.6s ease-in-out infinite -2.2s; }} .f4 {{ animation: fl 4.6s ease-in-out infinite -.6s; }}
    @keyframes fl {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-7px); }} }}
    .rise {{ animation: rise 2.4s ease-in-out infinite; }}
    @keyframes rise {{ 0% {{ opacity: 0; transform: translateY(8px); }} 50% {{ opacity: 1; }} 100% {{ opacity: 0; transform: translateY(-10px); }} }}
    .blink {{ animation: bl 1s steps(2) infinite; }} @keyframes bl {{ 50% {{ opacity: 0; }} }}
  </style>

  <rect width="720" height="410" rx="14" fill="#07060d" />

  <!-- Room: glowing wall, couch, lamp, owl -->
  <ellipse cx="360" cy="285" rx="300" ry="190" fill="url(#wall)" />
  <path d="M130 345 C130 235 210 190 360 188 C510 190 590 235 590 345 Z" fill="#241a6b" opacity="0.55" />
  <line x1="222" y1="342" x2="500" y2="342" stroke="#5b4bd6" stroke-width="2" stroke-opacity="0.8" />
  <g fill="#7b6cf0" opacity="0.8">
    <rect x="236" y="343" width="2" height="7" /><rect x="262" y="343" width="2" height="7" /><rect x="288" y="343" width="2" height="7" />
    <rect x="432" y="343" width="2" height="7" /><rect x="458" y="343" width="2" height="7" /><rect x="484" y="343" width="2" height="7" />
  </g>
  <ellipse cx="118" cy="335" rx="74" ry="92" fill="#0d0a1f" stroke="#4338ca" stroke-width="2.5" stroke-opacity="0.8" />
  <ellipse cx="602" cy="335" rx="74" ry="92" fill="#0d0a1f" stroke="#4338ca" stroke-width="2.5" stroke-opacity="0.8" />
  <ellipse cx="100" cy="300" rx="30" ry="46" fill="#17113a" opacity="0.8" />
  <g opacity="0.85" class="f3">
    <ellipse cx="238" cy="262" rx="15" ry="24" fill="#7766f0" transform="rotate(-12 238 262)" />
    <circle cx="242" cy="236" r="13" fill="#8b7bff" />
    <circle cx="246" cy="234" r="4.5" fill="none" stroke="#1b1450" stroke-width="2.5" />
    <path d="M254 238 l9 4 l-8 3 z" fill="#c4b5fd" />
  </g>
  <path d="M16 28 L64 28 L80 86 L0 86 Z" fill="#33297f" />
  <rect x="22" y="86" width="5" height="260" fill="#2d2575" />
  <line x1="58" y1="86" x2="58" y2="112" stroke="#6657d6" stroke-width="2" />
  <circle cx="58" cy="115" r="3.5" fill="#6657d6" />

  <!-- Floating dev symbols -->
  <g>
    <g class="f2">
      <path d="M222 28 l19 -11 l19 11 v22 l-19 11 l-19 -11 z" fill="#6d56e8" />
      <text x="241" y="46" text-anchor="middle" class="sym" font-size="12" fill="#e9e5ff">C+</text>
    </g>
    <g class="f3">
      <rect x="205" y="112" width="34" height="7" rx="2" fill="#f472b6" /><rect x="205" y="123" width="34" height="7" rx="2" fill="#ec4899" /><rect x="205" y="134" width="34" height="7" rx="2" fill="#db2777" />
    </g>
    <g class="f1"><text x="268" y="150" class="sym" font-size="92" font-weight="400" fill="#ff6a1f">{{</text></g>
    <g class="f4">
      <rect x="387" y="38" width="36" height="36" rx="4" fill="#f472b6" />
      <text x="405" y="62" text-anchor="middle" class="sym" font-size="15" fill="#3b0764">JS</text>
    </g>
    <g class="f2"><text x="472" y="150" class="sym" font-size="92" font-weight="400" fill="#ff8a1f">}}</text></g>
    <g class="f1"><text x="405" y="143" class="sym" font-size="42" fill="#7c6cf0">@</text></g>
    <text x="512" y="108" class="sym blink" font-size="16" fill="#e5e7eb">//:</text>
    <g stroke-linecap="round" stroke-width="2.5">
      <line x1="320" y1="22" x2="320" y2="68" stroke="#ff6a1f" class="rise" />
      <line x1="340" y1="30" x2="340" y2="56" stroke="#ff8a1f" class="rise" style="animation-delay:-.7s" />
      <line x1="356" y1="14" x2="356" y2="52" stroke="#ff6a1f" class="rise" style="animation-delay:-1.3s" />
      <line x1="372" y1="34" x2="372" y2="82" stroke="#ff8a1f" class="rise" style="animation-delay:-1.9s" />
    </g>
  </g>

  <rect x="120" y="396" width="480" height="14" rx="3" fill="#0b0818" />

  <!-- Boy (faceless flat style, backlit) -->
  <g>
    <path d="M205 402 C230 372 300 360 372 372 L372 402 Z" fill="#1c1545" />
    <path d="M515 402 C490 372 420 360 348 372 L348 402 Z" fill="#241b5c" />
    <path d="M215 392 C250 378 300 372 350 380 M505 392 C470 378 420 372 370 380" stroke="#3b2f94" stroke-width="3" fill="none" stroke-linecap="round" />
    <path d="M258 372 C262 312 296 270 336 258 L384 258 C424 270 458 312 462 372 Z" fill="url(#body)" />
    <path d="M300 276 C322 292 398 292 420 276 L420 292 C396 306 324 306 300 292 Z" fill="#e8590c" opacity="0.5" />
    <ellipse cx="360" cy="262" rx="30" ry="10" fill="#d9480f" />
    <rect x="347" y="232" width="26" height="34" rx="9" fill="#e8730f" />
    <ellipse cx="327" cy="205" rx="6" ry="9" fill="#f0862a" /><ellipse cx="393" cy="205" rx="6" ry="9" fill="#f0862a" />
    <path d="M328 196 C328 166 392 166 392 196 L392 214 C392 240 376 252 360 252 C344 252 328 240 328 214 Z" fill="url(#face)" />
    <path d="M322 204 C310 150 350 136 368 140 C404 142 414 178 398 208 L392 188 C378 172 350 178 328 196 Z" fill="url(#hair)" />
    <path d="M330 170 L335 152 L346 165 L356 148 L366 163 L378 150 L388 168" stroke="#f472b6" stroke-width="3" fill="none" stroke-linejoin="round" stroke-linecap="round" />
{layer("B", "Hands typing behind the laptop")}
    <path d="M262 372 L458 372 L446 360 L274 360 Z" fill="#0a0814" stroke="#2b2160" stroke-width="1.5" />
    <!-- laptop lid: hands lift it open and push it shut -->
    <g transform="translate(0,{LID_BOTTOM})">
      <g>
        <animateTransform attributeName="transform" type="scale" dur="{T}s" repeatCount="indefinite" calcMode="spline"
          keyTimes="{lidkt}" values="1 0.12;1 0.12;1 1;1 1;1 0.12;1 0.12"
          keySplines="{LIN};{EASE};{LIN};{EASE};{LIN}" />
        <g transform="translate(0,-{LID_BOTTOM})">
          <rect x="281" y="{LID_Y}" width="158" height="{LID_H}" rx="6" fill="url(#lidg)" stroke="#2b2160" stroke-width="2" />
          <circle cx="360" cy="{LID_MID}" r="8" fill="#6d56e8" filter="url(#neon)">
            <animate attributeName="opacity" values="0.6;1;0.6" dur="2s" repeatCount="indefinite" />
          </circle>
        </g>
      </g>
    </g>
{layer("F", "Hands in front: grip the lid top to open and close it")}
  </g>

  <!-- Lights out: fully black -->
  <rect width="720" height="410" rx="14" fill="#000000" opacity="0">
    <animate attributeName="opacity" dur="{T}s" repeatCount="indefinite"
      keyTimes="0;{KT(5.7)};{KT(6.4)};{KT(7.6)};{KT(8.4)};1" values="0;0;1;1;0;0" />
  </rect>
</svg>
"""

import xml.dom.minidom as m

open("assets/dev_coding.svg", "w", encoding="utf-8").write(svg)
m.parse("assets/dev_coding.svg")
print("ok", len(svg))
