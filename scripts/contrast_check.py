import re
from math import pow

path = 'css/styles.css'
with open(path, 'r', encoding='utf-8') as f:
    css = f.read()

m = re.search(r":root\s*\{([^}]*)\}", css, re.S)
root = m.group(1) if m else ''
vars = {}
for line in root.splitlines():
    line = line.strip()
    if line.startswith('--'):
        try:
            k,v = line.split(':',1)
            k = k.strip()[2:]
            v = v.strip().rstrip(';')
            vars[k]=v
        except Exception:
            continue


def parse_color(s):
    s=s.strip()
    if s.startswith('#'):
        hex = s.lstrip('#')
        if len(hex)==3:
            r=int(hex[0]*2,16); g=int(hex[1]*2,16); b=int(hex[2]*2,16)
        else:
            r=int(hex[0:2],16); g=int(hex[2:4],16); b=int(hex[4:6],16)
        return (r/255.0,g/255.0,b/255.0,1.0)
    m = re.match(r'rgba?\(([^)]+)\)', s)
    if m:
        parts=[p.strip() for p in m.group(1).split(',')]
        try:
            r=int(parts[0])/255.0; g=int(parts[1])/255.0; b=int(parts[2])/255.0
            a=float(parts[3]) if len(parts)>3 else 1.0
            return (r,g,b,a)
        except Exception:
            return None
    return None


def composite(fg, bg):
    r = fg[3]*fg[0] + (1-fg[3])*bg[0]
    g = fg[3]*fg[1] + (1-fg[3])*bg[1]
    b = fg[3]*fg[2] + (1-fg[3])*bg[2]
    return (r,g,b,1.0)


def lum_channel(c):
    if c<=0.03928:
        return c/12.92
    return pow((c+0.055)/1.055,2.4)


def rel_luminance(rgb):
    r,g,b = rgb[0],rgb[1],rgb[2]
    return 0.2126*lum_channel(r) + 0.7152*lum_channel(g) + 0.0722*lum_channel(b)


def contrast_ratio(c1, c2):
    l1 = rel_luminance(c1)
    l2 = rel_luminance(c2)
    L1 = max(l1,l2); L2 = min(l1,l2)
    return (L1+0.05)/(L2+0.05)

color_vars = {}
for k,v in vars.items():
    c = parse_color(v)
    color_vars[k]=c

pairs = [
    ('text','bg','Primary text on page background'),
    ('text-sec','bg','Secondary text on page background'),
    ('text-body','bg','Body text on page background'),
    ('accent-dk','bg','Accent-dark on page background'),
    ('accent','bg','Accent on page background'),
    ('text','card','Primary text on card background'),
    ('text','card2','Primary text on lighter card background'),
    ('accent','card','Accent on card background'),
]

results = []
for fgk,bgk,label in pairs:
    fg = color_vars.get(fgk)
    bg = color_vars.get(bgk)
    if fg is None or bg is None:
        results.append((label, fgk,bgk, 'MISSING'))
        continue
    if fg[3]<1.0:
        fgc = composite(fg, bg)
    else:
        fgc = fg
    if bg[3]<1.0:
        bgc = composite(bg, (1,1,1,1))
    else:
        bgc = bg
    ratio = contrast_ratio(fgc,bgc)
    results.append((label, fgk,bgk, round(ratio,2)))

print('Contrast results (WCAG):')
for r in results:
    print(f"- {r[0]}: {r[3]}")

fails = [r for r in results if isinstance(r[3], (int,float)) and r[3] < 4.5]
print('\nFailures (ratio < 4.5):')
if not fails:
    print('None — all checked pairs meet WCAG AA for normal text.')
else:
    for f in fails:
        print(f"- {f[0]}: {f[3]}")

# Suggestion: list ratios <7 (for AAA large text) as informational
info = [r for r in results if isinstance(r[3], (int,float)) and r[3] < 7]
print('\nInformational (ratios < 7):')
for i in info:
    print(f"- {i[0]}: {i[3]}")
