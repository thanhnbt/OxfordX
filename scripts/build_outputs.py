"""Build the main menu and self-contained per-unit HTML deliverables."""
from pathlib import Path
import base64
import html
import json
from build_reading_spread import build_reading_spread

ROOT = Path(__file__).resolve().parents[1]


def _image_data(payload):
    images = {}
    for asset in payload['assets']:
        path = ROOT / asset['asset_path']
        mime = 'image/svg+xml' if path.suffix.lower() == '.svg' else 'image/webp'
        images[asset['id']] = f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode('ascii')
    return images


def _render_app(payload, images, menu_href):
    template = (ROOT / 'web' / 'review.template.html').read_text(encoding='utf-8')
    scripts = (ROOT / 'web' / 'v2.js').read_text(encoding='utf-8')
    scripts += '\n' + '\n'.join((ROOT / 'web' / name).read_text(encoding='utf-8')
                                 for name in ('dictionary-config.js', 'dictionary-audio.js'))
    packed = dict(payload, images=images)
    if any(unit["id"] == 3 for unit in payload["units"]):
        packed["cultureNote"] = json.loads((ROOT / "data" / "culture-note.json").read_text(encoding="utf-8-sig"))
    serialized = json.dumps(packed, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    return (template.replace('href="#home" class="brand"', f'href="{menu_href}" class="brand"')
            .replace('__V2_STYLES__', (ROOT / 'web' / 'v2.css').read_text(encoding='utf-8'))
            .replace('__V2_SCRIPT__', scripts)
            .replace('__REVIEW_DATA__', serialized))


def build_outputs(payload, images=None):
    """Write output/unit-N.html, the root menu, and an ignored full-app QA fixture."""
    images = images or _image_data(payload)
    lesson_path = ROOT / 'inputdata' / 'Unit3' / 'lesson.html'
    if not lesson_path.is_file():
        raise FileNotFoundError(f'Required original lesson not found: {lesson_path}')
    lesson = lesson_path.read_text(encoding='utf-8')
    lesson = build_reading_spread(lesson, ROOT)

    output_dir = ROOT / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)
    for unit in payload['units']:
        used_ids = {unit['hero'], *(word['visual'] for word in unit['vocabulary'])}
        unit_assets = [asset for asset in payload['assets'] if asset['id'] in used_ids]
        bundle = dict(payload)
        bundle['units'] = [unit]
        bundle['assets'] = unit_assets
        bundle['classwork'] = {str(unit['id']): payload.get('classwork', {}).get(str(unit['id']), {})}
        unit_images = {key: images[key] for key in used_ids}
        if unit['id'] == 3:
            bundle['embeddedLesson'] = lesson
        page = _render_app(bundle, unit_images, '../index.html')
        (output_dir / f'unit-{unit["id"]}.html').write_text(page, encoding='utf-8')

    full_bundle = dict(payload)
    full_bundle['embeddedLesson'] = lesson
    qa_path = ROOT / 'tmp' / 'qa' / 'full-review.html'
    qa_path.parent.mkdir(parents=True, exist_ok=True)
    qa_path.write_text(_render_app(full_bundle, images, '#home'), encoding='utf-8')

    links = []
    for unit in payload['units']:
        title = html.escape(unit['title'])
        subtitle = html.escape(unit['subtitle'])
        color = html.escape(unit['color'], quote=True)
        visual = images[unit['hero']]
        alt = html.escape(next(asset['alt'] for asset in payload['assets'] if asset['id'] == unit['hero']), quote=True)
        links.append(
            f'<a class="unit-link" style="--accent:{color}" href="output/unit-{unit["id"]}.html">'
            f'<img class="unit-visual" src="{visual}" alt="{alt}"><div class="unit-copy"><span class="unit-number">UNIT {unit["id"]:02}</span>'
            f'<h2>{title}</h2><p>{subtitle}</p></div>'
            f'<span class="open">Open Unit {unit["id"]}<span aria-hidden="true">→</span></span></a>'
        )
    menu = (ROOT / 'web' / 'menu.template.html').read_text(encoding='utf-8')
    (ROOT / 'index.html').write_text(menu.replace('__UNIT_LINKS__', ''.join(links)), encoding='utf-8')
    print('Built index.html and ' + ', '.join(f'output/unit-{u["id"]}.html' for u in payload['units']))


if __name__ == '__main__':
    data = json.loads((ROOT / 'data' / 'review.json').read_text(encoding='utf-8'))
    build_outputs(data)
