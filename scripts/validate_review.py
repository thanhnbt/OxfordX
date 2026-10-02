"""Validate the deliverable against the supplied PDF and image provenance."""
from pathlib import Path
import base64
import hashlib
import json
import re
import subprocess
import fitz
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
report=[]
def check(name,passed,detail=''):
    report.append(dict(name=name,status='PASS' if passed else 'FAIL',detail=detail))

data=json.loads((ROOT/'data/review.json').read_text(encoding='utf-8'))
menu_html=(ROOT/'index.html').read_text(encoding='utf-8')
html=(ROOT/'tmp/qa/full-review.html').read_text(encoding='utf-8')
embedded=json.loads(re.search(r'<script id="review-data" type="application/json">([\s\S]*?)</script>',html)[1])
doc=fitz.open(ROOT/data['source']['file'])
check('Root index is only the main menu','<nav class="unit-list"' in menu_html and '<script' not in menu_html and 'review-data' not in menu_html)
for unit in data['units']:
    unit_html=(ROOT/'output'/f'unit-{unit["id"]}.html').read_text(encoding='utf-8')
    unit_data=json.loads(re.search(r'<script id="review-data" type="application/json">([\s\S]*?)</script>',unit_html)[1])
    check(f'Unit {unit["id"]} is a standalone bundle',[u['id'] for u in unit_data['units']]==[unit['id']])
    check(f'Unit {unit["id"]} has no unresolved template tokens',not re.search(r'__[A-Z0-9_]+__',unit_html))
check('Unit 3 embeds the full synchronized lesson','embeddedLesson' in json.loads(re.search(r'<script id="review-data" type="application/json">([\s\S]*?)</script>',(ROOT/'output'/'unit-3.html').read_text(encoding='utf-8'))[1]) and 'srcdoc=' in (ROOT/'output'/'unit-3.html').read_text(encoding='utf-8'))
check('Source file fingerprint',hashlib.sha256((ROOT/data['source']['file']).read_bytes()).hexdigest()==data['source']['sha256'])
check('Unit scope is exactly 1–3',[u['id'] for u in data['units']]==[1,2,3])
check('33 key words',sum(len(u['vocabulary']) for u in data['units'])==33)
check('12 context words',sum(len(u['contexts']) for u in data['units'])==12)
check('Word study has 18 target forms',sum(sum(len(w.split(' → ')) for w in u['word_study']['words']) for u in data['units'])==18)
check('Packed data equals authored data',all(embedded[k]==data[k] for k in data))
ids=[v['id'] for u in data['units'] for v in u['vocabulary']]
check('Unique vocabulary IDs',len(set(ids))==len(ids))
for u in data['units']:
    text=doc[u['source_pages']['vocabulary']-1].get_text().lower()
    vocab_text=re.search(r'vocabulary:\s*(.*?)\s*words in context:',text,re.S)[1]
    normalize=lambda s:re.sub(r'\s+',' ',s).strip()
    source_words=[normalize(w) for w in vocab_text.split(',')]
    check(f'Unit {u["id"]} exact core word list',source_words==[v['word'] for v in u['vocabulary']],str(source_words))
    for v in u['vocabulary']:
        check(f'{v["id"]}: pronunciation & definitions',all(v.get(k) for k in ['ipa','sound_out','english_meaning','vietnamese_support','example']))
        # Uppercase blocks mark one primary stress; secondary compound stress is lowercased.
        check(f'{v["id"]}: primary stress marker',len(re.findall(r'[A-Z]{2,}',v['sound_out']))==1)
        check(f'{v["id"]}: visual is packed',v['visual'] in embedded['images'])
    grammar_text=doc[u['grammar_page']-1].get_text().lower()
    needle={1:'predictions with will',2:'future real conditional',3:'infinitives'}[u['id']]
    check(f'Unit {u["id"]}: grammar anchored in source',needle in grammar_text)
    for strand in ['reading','grammar','speaking','writing','word_study','listening']:
        check(f'Unit {u["id"]}: {strand} page reference',strand in u['source_pages'])

for a in data['assets']:
    p=ROOT/a['asset_path'];check(a['id']+': asset exists',p.is_file())
    raw=p.read_bytes();check(a['id']+': packed asset matches file',base64.b64decode(embedded['images'][a['id']].split(',',1)[1])==raw)
    if a['source_file']:
        bbox=fitz.Rect(a['bbox_pdf_points']);check(a['id']+': valid PDF region',doc[a['pdf_page_1based']-1].rect.contains(bbox) and not bbox.is_empty)
        with Image.open(p) as im:check(a['id']+': raster decodes',im.width==a['width'] and im.height==a['height'])
    else:
        check(a['id']+': authored diagram identified',a['match_status']=='authored-support-diagram' and a['bbox_pdf_points'] is None)
for unit in [1,3]:
    check(f'Unit {unit}: 11 exact source vocabulary crops',sum(a['id'].startswith(f'u{unit}-') and a['match_status']=='exact-book-image' for a in data['assets'])==11)
check('Unit 2 coverage is six source crops and five authored diagrams',sum(a['id'].startswith('u2-') and a['source_file'] is not None for a in data['assets'])==6 and sum(a['id'].startswith('u2-') and a['source_file'] is None for a in data['assets'])==5)
check('Main menu and Unit pages have no external script/css dependencies',not re.search(r'<script[^>]+src=|<link[^>]+stylesheet',menu_html) and all(not re.search(r'<script[^>]+src=|<link[^>]+stylesheet',(ROOT/'output'/f'unit-{u["id"]}.html').read_text(encoding='utf-8')) for u in data['units']))
check('No template placeholders remain','__REVIEW_DATA__' not in html)
check('No v2 placeholders remain','__V2_STYLES__' not in html and '__V2_SCRIPT__' not in html)
runtime_html=html.split('</script>',1)[1]
js=re.findall(r'<script>([\s\S]*?)</script>',runtime_html)[0]
temp=ROOT/'tmp/qa/app.js';temp.parent.mkdir(parents=True,exist_ok=True);temp.write_text(js,encoding='utf-8')
syntax=subprocess.run(['node','--check',str(temp)],capture_output=True,text=True)
check('JavaScript syntax',syntax.returncode==0,syntax.stderr)
summary=dict(passed=sum(r['status']=='PASS' for r in report),failed=sum(r['status']=='FAIL' for r in report))
(ROOT/'qa/data-results.json').write_text(json.dumps(dict(summary=summary,checks=report),ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary));
if summary['failed']:
    print(json.dumps([r for r in report if r['status']=='FAIL'],ensure_ascii=False,indent=2));raise SystemExit(1)
