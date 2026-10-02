"""Reconstruct SB30–31 using original crops and existing timed HTML words."""
import base64, hashlib, io, json, re
from PIL import Image

def build_reading_spread(source, root):
    start = source.index('IMGS=') + 5
    images, _ = json.JSONDecoder().raw_decode(source[start:])
    raw = base64.b64decode(images['30'].split(',', 1)[1])
    page = Image.open(io.BytesIO(raw))
    regions = {'soldier': (.008,.005,.146,.945), 'general': (.361,.411,.478,.914),
               'army': (.497,.005,.985,.226), 'craftsmen': (.669,.241,.952,.624)}
    assets = root / 'assets/reading'; assets.mkdir(parents=True, exist_ok=True)
    manifest, packed = {}, {}
    for name,bounds in regions.items():
        box = tuple(round(v*page.size[i%2]) for i,v in enumerate(bounds))
        buffer = io.BytesIO(); page.crop(box).save(buffer,format='WEBP',quality=94)
        content=buffer.getvalue(); path=assets/f'{name}.webp'; path.write_bytes(content)
        packed[name]='data:image/webp;base64,'+base64.b64encode(content).decode('ascii')
        manifest[name]={'source':'inputdata/Unit3/lesson.html: IMGS[30]', 'student_book_pages':[30,31],
          'source_size':list(page.size),'bbox_pixels':list(box),'asset_path':path.relative_to(root).as_posix(),
          'sha256':hashlib.sha256(content).hexdigest(),'source_sha256':hashlib.sha256(raw).hexdigest()}
    (root/'data/reading-spread-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    paragraphs, titles = [], []
    for tag,content in re.findall(r'<(h2|p)>(.*?)</\1>',source):
        ids=re.findall(r'data-id="(\d+)"',content)
        if not ids: continue
        content=re.sub(r'\s*<span class="slash">/</span>\s*',' ',content)
        if tag=='h2': titles.append(content)
        else: paragraphs.append((int(ids[0]),content))
    def text(low,high):
        return ''.join(f'<span class="reading-sentence">{content} </span>' for first,content in paragraphs if low<=first<=high)
    def image(name,alt,cls=''):
        return f'<img class="{cls}" src="{packed[name]}" alt="{alt}">'
    spread=f'''<svg width="0" height="0" aria-hidden="true" style="position:absolute"><defs><clipPath id="craft-art-clip" clipPathUnits="objectBoundingBox"><rect x=".198" y="0" width=".802" height="1"/><ellipse cx=".237" cy=".65" rx=".237" ry=".295"/></clipPath><clipPath id="general-art-clip" clipPathUnits="objectBoundingBox"><polygon points=".30,0 1,0 1,1 0,1 0,.37 .20,.25 .25,.15"/></clipPath></defs></svg><div class="book-scroll"><main class="book-spread" aria-label="Hidden Army, pages 30 and 31">
<section class="book-page page-left lesson-page" data-page="30" id="page-30">
<aside class="soldier-art"><div class="soldier-figure">{image('soldier','Original terracotta soldier')}<div class="think soldier-think"><strong>Think</strong> What is the author’s purpose for this paragraph?</div></div></aside>
<article class="left-copy"><h1>{titles[0]}</h1><h2>{titles[1]}</h2><p>{text(2,6)}</p>
<div class="think first-think"><strong>Think</strong> What is the author’s purpose in the first paragraph?</div>
<p>{text(7,12)}</p><p>{text(13,19)}</p><figure class="general-art">{image('general','Computerized image of a clay general')}<figcaption>a computerized image of a clay general</figcaption></figure>
<p>{text(20,24)}</p><p>{text(25,31)}</p><p>{text(32,43)}</p></article><span class="book-number">30</span></section>
<section class="book-page page-right lesson-page" data-page="31" id="page-31">{image('army','Rows of clay soldiers in the excavation pit','army-art')}
<div class="right-columns"><article><p>{text(44,56)}</p><p>{text(57,66)}</p><p>{text(67,69)}</p><p>{text(70,76)}</p></article>
<article>{image('craftsmen','Craftsmen making clay soldiers, including a close-up of a clay head','craftsmen-art')}<p>{text(77,82)}</p><p>{text(83,89)}</p>
<div class="think"><strong>Think</strong> What is the author’s purpose for the entire reading?</div></article></div><span class="book-number">31</span></section></main></div>'''
    source=source[:source.index('<div class="layout">')]+spread+'\n'+source[source.index('<div class="player">'):]
    start=source.index('IMGS=')+5; _,consumed=json.JSONDecoder().raw_decode(source[start:])
    source=source[:start]+'{}'+source[start+consumed:]
    source=re.sub(r'function setPage\(p\)\{.*?\}\n','function setPage(p){if(p===pg)return;pg=p;document.querySelectorAll(".lesson-page").forEach(x=>x.classList.toggle("active-page",+x.dataset.page===p))}\n',source,count=1)
    source=source.replace('if(scroll)el?.scrollIntoView({behavior:"smooth",block:"center"})',
        'if(scroll&&el){const pane=document.querySelector(".book-scroll");const top=el.getBoundingClientRect().top-pane.getBoundingClientRect().top+pane.scrollTop-pane.clientHeight*.35;pane.scrollTo({top:Math.max(0,top),behavior:"smooth"})}')
    css=(root/'web/embedded-reading.css').read_text(encoding='utf-8')
    return source.replace('</head>',f'<style>{css}</style></head>',1)
