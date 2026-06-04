import re
from pathlib import Path
root = Path(__file__).resolve().parent.parent
html = (root / 'index.html').read_text('utf-8')
css = (root / 'css' / 'styles.css').read_text('utf-8')
classes = set(re.findall(r'class=\"([^\"]+)\"', html))
ids = set(re.findall(r'id=\"([^\"]+)\"', html))
class_names = set(cl for group in classes for cl in group.split())

selectors = re.findall(r'([^\{]+)\{', css)
selector_tokens = set()
for sel in selectors:
    parts = re.split(r',|>|\+|~|\\s+', sel)
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if part.startswith('.'):
            selector_tokens.add(part[1:])
        elif part.startswith('#'):
            selector_tokens.add(part[1:])
        elif part.isalpha():
            selector_tokens.add(part)

base_tags = {'body','html','nav','section','div','img','video','a','h1','h2','h3','h4','h5','h6','p','ul','li','form','input','textarea','select','button','label','main','strong','span'}
unused = [tok for tok in sorted(selector_tokens) if tok not in base_tags and tok not in class_names and tok not in ids]
print('potential unused tokens:', len(unused))
for tok in unused:
    print(tok)
