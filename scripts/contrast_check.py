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

print('=== LIGHT THEME CONTRAST RESULTS ===')
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

# Parse dark theme variables
print('\n\n=== DARK THEME CONTRAST AUDIT ===')
m_dark = re.search(r'\[data-theme="dark"\]\s*\{([^}]*)\}', css, re.S)
dark_vars_raw = m_dark.group(1) if m_dark else ''
dark_vars = {}
for line in dark_vars_raw.splitlines():
    line = line.strip()
    if line.startswith('--'):
        try:
            k,v = line.split(':',1)
            k = k.strip()[2:]
            v = v.strip().rstrip(';')
            dark_vars[k]=v
        except Exception:
            continue

dark_color_vars = {}
for k,v in dark_vars.items():
    c = parse_color(v)
    dark_color_vars[k]=c

# Dark theme accent pairs to check
dark_pairs = [
    ('accent','bg','Accent on dark background'),
    ('accent','card','Accent on dark card'),
    ('accent','card2','Accent on dark card2'),
    ('accent-dk','bg','Accent-dk on dark background'),
    ('accent-dk','card','Accent-dk on dark card'),
    ('accent-dk','card2','Accent-dk on dark card2'),
    ('accent-decor','bg','Accent-decor on dark background'),
    ('accent-decor','card','Accent-decor on dark card'),
    ('accent-decor','card2','Accent-decor on dark card2'),
]

dark_results = []
for fgk,bgk,label in dark_pairs:
    fg = dark_color_vars.get(fgk)
    bg = dark_color_vars.get(bgk)
    if fg is None or bg is None:
        dark_results.append((label, fgk,bgk, 'MISSING'))
        continue
    if fg[3]<1.0:
        fgc = composite(fg, bg)
    else:
        fgc = fg
    if bg[3]<1.0:
        bgc = composite(bg, (0,0,0,1))
    else:
        bgc = bg
    ratio = contrast_ratio(fgc,bgc)
    dark_results.append((label, fgk,bgk, round(ratio,2)))

print('\nDark theme accent color contrast ratios:')
for r in dark_results:
    status = '✓ PASS' if isinstance(r[3], (int,float)) and r[3] >= 4.5 else ('⚠ WARN' if isinstance(r[3], (int,float)) and r[3] >= 3.0 else '✗ FAIL')
    print(f"- {status}: {r[0]}: {r[3]}")

dark_fails_aa = [r for r in dark_results if isinstance(r[3], (int,float)) and r[3] < 4.5]
dark_fails_aaa = [r for r in dark_results if isinstance(r[3], (int,float)) and r[3] < 3.0]

print(f'\n✗ WCAG AA failures (< 4.5): {len(dark_fails_aa)}')
if dark_fails_aa:
    for f in dark_fails_aa:
        print(f"  - {f[0]}: {f[3]}")

print(f'\n✗ WCAG AAA failures (< 3.0): {len(dark_fails_aaa)}')
if dark_fails_aaa:
    for f in dark_fails_aaa:
        print(f"  - {f[0]}: {f[3]}")
else:
    print('  None — all decorative uses meet minimum contrast.')
