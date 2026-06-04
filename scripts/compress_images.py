from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parent.parent
images = [
    'images/design-nursery-wall-art.png',
    'images/design-printables-mockup.png',
    'images/calendar-sarah-johnson.png',
    'images/calendar-scheduled-meetings.png',
    'images/calendar-meeting-prep.png',
]
for rel in images:
    path = root / rel
    img = Image.open(path)
    orig = path.stat().st_size
    if img.mode in ('RGBA', 'LA'):
        img = img.convert('RGBA')
    else:
        img = img.convert('RGB')
    img.save(path, optimize=True)
    new = path.stat().st_size
    print(f'{rel}: {orig/1024:.1f} KB -> {new/1024:.1f} KB')

    webp_path = path.with_suffix('.webp')
    img.save(webp_path, 'WEBP', quality=80, method=6)
    webp = webp_path.stat().st_size
    print(f'{webp_path.name}: {webp/1024:.1f} KB (webp)')
