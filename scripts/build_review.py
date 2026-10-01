"""Build a portable, self-contained review from audited book regions and authored data."""
from pathlib import Path
import base64
import hashlib
import io
import json
import re
import fitz
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
PDF = next(ROOT.glob('*.pdf'))
ASSETS = ROOT / 'assets' / 'images'
ASSETS.mkdir(parents=True, exist_ok=True)
DATA = ROOT / 'data'
DATA.mkdir(exist_ok=True)
doc = fitz.open(PDF)
manifest = []
images = {}

def crop(key, page, bbox, sb, role='exact-book-image', alt=''):
    region = fitz.Rect(bbox)
    assert doc[page - 1].rect.contains(region), (key, bbox)
    pix = doc[page - 1].get_pixmap(clip=region, matrix=fitz.Matrix(3, 3), alpha=False)
    im = Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')
    buf = io.BytesIO()
    im.save(buf, format='WEBP', quality=90)
    raw = buf.getvalue()
    path = ASSETS / f'{key}.webp'
    path.write_bytes(raw)
    images[key] = 'data:image/webp;base64,' + base64.b64encode(raw).decode()
    manifest.append(dict(id=key, source_file=PDF.name, pdf_page_1based=page,
                         printed_teacher_page=page, student_book_page=sb,
                         bbox_pdf_points=list(bbox), coordinate_system='top-left; points; x0,y0,x1,y1',
                         extraction_method='PyMuPDF PDF region render, 3x',
                         asset_path=path.relative_to(ROOT).as_posix(), width=im.width, height=im.height,
                         match_status=role, alt=alt, review_status='pending-visual-review'))

def native_crop(key, page, xy, sb, role='exact-book-image', alt=''):
    # Coordinates in the original embedded left Student Book page, 533 x 688.
    rect = doc[page - 1].get_image_rects(doc[page - 1].get_images()[0][0])[0]
    x0,y0,x1,y1 = xy
    bbox = (rect.x0+x0*rect.width/533, rect.y0+y0*rect.height/688,
            rect.x0+x1*rect.width/533, rect.y0+y1*rect.height/688)
    crop(key,page,bbox,sb,role,alt)

u1 = ['moon','asteroid','comet','meteorite','solar system','stars','galaxy','universe','spacecraft','telescope','observatory']
u3 = ['army','soldiers','uniform','emperor','armor','treasure','archaeologist','tomb','jade','clay','peasant']
row1 = [(58,127,123,202),(135,127,198,202),(211,127,273,202),(286,127,348,202),(361,127,424,202),(437,127,499,202)]
row2 = [(61,235,137,312),(152,235,228,312),(243,235,318,312),(333,235,410,312),(424,235,499,312)]
# Unit 3 uses a slightly lower second row; all word labels remain outside crops.
row1_u3 = [(x,132,x1,207) for x,_,x1,_ in row1]
row2_u3 = [(x,239,x1,315) for x,_,x1,_ in row2]
for unit,page,sb,words,boxes in [(1,36,8,u1,row1+row2),(3,56,28,u3,row1_u3+row2_u3)]:
    for word,xy in zip(words,boxes):
        native_crop(f'u{unit}-{word.replace(" ","-")}',page,xy,sb,alt=f'Original book illustration for {word}')

native_crop('u2-astronomer',36,row2[3],8,'supporting-book-image','A person observing the sky through a telescope')
native_crop('u2-core',44,(303,438,437,568),16,'supporting-book-image','A cutaway of Earth showing its center')
native_crop('u2-orbit',44,(384,215,501,286),16,'supporting-book-image','Planets on paths around the Sun')
native_crop('u2-craters',44,(387,306,493,373),16,'supporting-book-image','Hollows on the surface of the Moon')
native_crop('u2-surface',44,(387,306,493,373),16,'supporting-book-image','The visible outside of the Moon')
crop('u2-unique',46,(421,353,463,390),19,'supporting-book-image','Earth pictured beside Venus in the book')
crop('hero-space',46,(44,162,294,317),18,'supporting-book-image','A detail of the solar system illustration from the book')
crop('hero-history',58,(298,72,550,166),31,'supporting-book-image','Rows of ancient clay soldiers')
crop('hero-bella',38,(44,254,294,399),10,'supporting-book-image','Bella and her father pictured in the book')

def diagram(key, body, alt):
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180"><rect width="320" height="180" rx="20" fill="#edf4fc"/>'+body+'</svg>'
    raw = svg.encode()
    (ASSETS/f'{key}.svg').write_bytes(raw)
    images[key] = 'data:image/svg+xml;base64,'+base64.b64encode(raw).decode()
    manifest.append(dict(id=key, source_file=None, pdf_page_1based=None, student_book_page=None,
                         bbox_pdf_points=None, asset_path=f'assets/images/{key}.svg', width=320,height=180,
                         extraction_method='authored SVG learning aid', match_status='authored-support-diagram',
                         alt=alt, review_status='pending-visual-review'))

diagram('u2-space-probe','<circle cx="264" cy="60" r="29" fill="#de9870"/><path d="M175 90L222 73" stroke="#6f84a8" stroke-dasharray="5 5" stroke-width="3"/><rect x="113" y="62" width="61" height="60" rx="8" fill="#a2b8d6" stroke="#3b5074" stroke-width="3"/><path d="M65 62H103V122H65ZM184 62H222V122H184Z" fill="#315c9e"/><path d="M78 62V122M90 62V122M65 82H103M65 102H103M196 62V122M208 62V122M184 82H222M184 102H222" stroke="#8dcbdc"/><path d="M128 52Q144 22 160 52Z" fill="#e3ac4f"/><path d="M144 52V63" stroke="#3b5074" stroke-width="3"/>','A robot spacecraft with solar panels sends information from space')
diagram('u2-gravity','<path d="M0 150Q160 120 320 150V180H0" fill="#83b9a2"/><circle cx="160" cy="47" r="15" fill="#e49770"/><path d="M160 74V121M145 106L160 121L175 106" fill="none" stroke="#28538f" stroke-width="6"/>','An arrow points down as an object falls toward Earth')
diagram('u2-matter','<rect x="46" y="70" width="55" height="55" rx="6" fill="#8f9dbc"/><path d="M131 65H182L176 131H137Z" fill="#add2ed" stroke="#477697" stroke-width="3"/><path d="M136 88H178L175 128H138Z" fill="#73b0dc"/><path d="M230 123Q249 92 230 58M249 123Q269 92 249 58" fill="none" stroke="#9bacba" stroke-width="5"/>','A solid block, water and air are examples of matter')
diagram('u2-distance','<circle cx="65" cy="74" r="23" fill="#d8a24e"/><circle cx="260" cy="74" r="19" fill="#76a9c6"/><path d="M72 130H253M83 121L72 130L83 139M242 121L253 130L242 139" stroke="#355688" fill="none" stroke-width="4"/><path d="M65 102V147M260 99V147" stroke="#9daec7" stroke-width="2"/>','A two-headed arrow measures the space between two objects')
diagram('u2-diameter','<circle cx="160" cy="90" r="63" fill="#dce8f7" stroke="#477ba6" stroke-width="4"/><path d="M97 90H223" stroke="#ce7248" stroke-width="5"/><circle cx="160" cy="90" r="5" fill="#355688"/>','A line crosses a circle through its center from edge to edge')

def entry(word,pos,ipa,sound,meaning,vi,group,example):
    return dict(word=word,pos=pos,ipa=ipa,sound_out=sound,english_meaning=meaning,
                vietnamese_support=vi,concept_cluster=group,example=example)

v1 = [
entry('moon','n.','/muːn/','MOON','a round object in space that moves around a planet','mặt trăng','Space objects','The moon moves around Earth.'),
entry('asteroid','n.','/ˈæs.tə.rɔɪd/','AS-tuh-royd','a rocky object that travels around the Sun','tiểu hành tinh','Space objects','An asteroid is made of rock.'),
entry('comet','n.','/ˈkɑː.mɪt/','KAH-mit','an object of ice and dust that can have a bright tail','sao chổi','Space objects','The comet has a bright tail.'),
entry('meteorite','n.','/ˈmiː.t̬i.ə.raɪt/','MEE-tee-uh-ryte','a rock from space that reaches the ground','thiên thạch','Space objects','The scientist holds a meteorite.'),
entry('solar system','n.','/ˈsoʊ.lɚ ˌsɪs.təm/','SOH-ler sis-tum','the Sun and the objects that move around it','hệ mặt trời','Our place in space','Earth is in our solar system.'),
entry('stars','plural n.','/stɑːrz/','STARZ','huge balls of hot gas that give out light','các ngôi sao','Space objects','We can see stars at night.'),
entry('galaxy','n.','/ˈɡæl.ək.si/','GAL-uk-see','a huge group of stars, gas and dust','thiên hà','Our place in space','Our galaxy is the Milky Way.'),
entry('universe','n.','/ˈjuː.nə.vɝːs/','YOO-nuh-vers','all of space and everything in it','vũ trụ','Our place in space','There are many galaxies in the universe.'),
entry('spacecraft','n.','/ˈspeɪs.kræft/','SPACE-kraft','a vehicle made to travel in space','tàu vũ trụ','Exploring space','Bella imagines a journey in a spacecraft.'),
entry('telescope','n.','/ˈtel.ə.skoʊp/','TEL-uh-skohp','a tool that helps us see things far away','kính thiên văn','Exploring space','I use a telescope to look at the moon.'),
entry('observatory','n.','/əbˈzɝː.və.tɔːr.i/','ub-ZER-vuh-tor-ee','a place with tools for studying space','đài thiên văn','Exploring space','An observatory can have a large telescope.')]
v2 = [
entry('astronomer','n.','/əˈstrɑː.nə.mɚ/','uh-STRAH-nuh-mer','a scientist who studies stars, planets and space','nhà thiên văn học','Exploring space','An astronomer studies the planets.'),
entry('space probe','n.','/ˈspeɪs ˌproʊb/','SPACE prohb','a robot spacecraft that collects information','tàu thăm dò vũ trụ','Exploring space','A space probe collects information about Mars.'),
entry('core','n.','/kɔːr/','KOR','the center part of something','lõi','Planet parts','Earth has a core.'),
entry('gravity','n.','/ˈɡræv.ə.t̬i/','GRAV-uh-tee','the force that pulls things toward each other','lực hấp dẫn','How space works','Earth’s gravity pulls us toward the ground.'),
entry('orbit','n.','/ˈɔːr.bɪt/','OR-bit','the path of an object around another object in space','quỹ đạo','How space works','Earth’s orbit goes around the Sun.'),
entry('matter','n.','/ˈmæt̬.ɚ/','MAT-er','the stuff that things are made of','vật chất','How space works','Rock, water and air are matter.'),
entry('distance','n.','/ˈdɪs.təns/','DIS-tuns','the space between two things or places','khoảng cách','Measuring planets','The distance between planets can be huge.'),
entry('diameter','n.','/daɪˈæm.ə.t̬ɚ/','dye-AM-uh-ter','the distance across a circle through its center','đường kính','Measuring planets','We can measure a planet’s diameter.'),
entry('surface','n.','/ˈsɝː.fɪs/','SER-fis','the outside or top part of something','bề mặt','Planet parts','We can see craters on the moon’s surface.'),
entry('craters','plural n.','/ˈkreɪ.t̬ɚz/','KRAY-terz','large round hollows on a planet or moon','các hố trên bề mặt','Planet parts','The moon has many craters.'),
entry('unique','adj.','/juːˈniːk/','yoo-NEEK','different from all the others; one of a kind','độc đáo, duy nhất','Measuring planets','Earth is unique in our solar system because it has people.')]
v3 = [
entry('army','n.','/ˈɑːr.mi/','AR-mee','a large group of soldiers','quân đội','People','The emperor had an army.'),
entry('soldiers','plural n.','/ˈsoʊl.dʒɚz/','SOHL-jerz','people who serve in an army','những người lính','People','The clay soldiers look different from each other.'),
entry('uniform','n.','/ˈjuː.nə.fɔːrm/','YOO-nuh-form','special clothes worn by people in the same group','đồng phục','Things to wear','A soldier wears a uniform.'),
entry('emperor','n.','/ˈem.pɚ.ɚ/','EM-per-er','a ruler of an empire','hoàng đế','People','The emperor ruled ancient China.'),
entry('armor','n.','/ˈɑːr.mɚ/','AR-mer','a strong covering that protects the body','áo giáp','Things to wear','Armor protects a soldier’s body.'),
entry('treasure','n.','/ˈtreʒ.ɚ/','TREZH-er','valuable things, such as gold or jewels','kho báu','Clues from the past','They found treasure in the tomb.'),
entry('archaeologist','n.','/ˌɑːr.kiˈɑː.lə.dʒɪst/','ar-kee-AH-luh-jist','a scientist who studies old objects to learn about the past','nhà khảo cổ học','People','An archaeologist studies the clay soldiers.'),
entry('tomb','n.','/tuːm/','TOOM','a place where a dead person is buried','ngôi mộ','Clues from the past','The emperor’s tomb is still closed in the reading.'),
entry('jade','n.','/dʒeɪd/','JAYD','a hard stone, often green, used to make beautiful things','ngọc bích','Materials','People made beautiful things from jade.'),
entry('clay','n.','/kleɪ/','KLAY','soft earth that can be shaped and made hard','đất sét','Materials','The soldiers were made from clay.'),
entry('peasant','n.','/ˈpez.ənt/','PEZ-unt','a poor farmer, especially in the past','nông dân nghèo thời xưa','People','The peasant works in a field.')]

context = [
 [('vast','very large','rộng lớn'),('dwelled','lived in a place','đã sống'),('speck','a very small spot','đốm nhỏ'),('disk','a flat, round shape','hình đĩa')],
 [('bodies','objects in space, such as planets','các thiên thể'),('explore','travel or look carefully to learn more','khám phá'),('inner','closer to the center','phía trong'),('outer','farther from the center','phía ngoài')],
 [('battle','a fight between armies','trận chiến'),('generals','leaders in an army','các tướng lĩnh'),('varnish','a coating that protects a surface','lớp phủ bảo vệ'),('coffin','a box in which a dead person is buried','quan tài')]]

units = [
dict(id=1,title='Our place in space',subtitle='Imagine a journey beyond Earth.',big_question='Where are we in the universe?',color='#4961b6',hero='hero-space',vocabulary=v1,contexts=context[0],
     reading_title="Bella’s Home",genre='Science fiction · a poem',reading_strategy='Picture the changes in your mind.',reading_pages=[38,39,40],
     reading_chunks=[('At home','Bella lives in Nome, Alaska. Her father uses a poem to help her imagine her place in the universe.'),('Farther away','In her imagination, Bella travels in a spacecraft. Her home looks smaller. Then she sees Earth, the solar system and galaxies.'),('Home again','Bella’s imaginary journey ends. She is back in her bedroom. She wants to imagine visiting those places again.')],
     thinking_prompt='As Bella moves farther away, how does Earth look? Draw it near, then far.',thinking_frame='At first, I picture ___. Later, I picture ___.',
     grammar_title='Make a prediction',grammar_name='Predictions with will',grammar_page=41,grammar_pattern='I think + subject + will + base verb',grammar_example='I think we will learn more about space.',grammar_note='Use will to say what you think will happen. After will, use the base verb.',grammar_frame='I think I will ___ in the future.',
     grammar_checks=[('I think people ___ visit more planets.',['will','are','did'],0,'Use will for a prediction.'),('I will ___ the moon with a telescope.',['studying','study','studied'],1,'After will, use the base verb: study.')],
     word_study=dict(title='Words with ei',page=43,note='In these words, ei sounds like the long a in day.',words=['eighty','freight','reins','sleigh','veil','weigh']),
     listening_title='Looking at the Stars',listening_goal='Listen for reasons.',listening_page=214,listening_script='Andy and Jenny look at the stars at Grandpa’s farm. They can see the stars clearly because there are fewer bright city lights. Grandpa explains that the Milky Way is our galaxy. Its many stars look like a white belt in the sky.',listening_question='Why are the stars easier to see at the farm?',listening_answer='There is less light pollution: fewer bright city lights.',
     speaking_title='Talk about differences',speaking_frame='In the first picture, I see ___. In the second picture, I see ___.',speaking_page=42,writing_title='Write complete sentences',writing_tip='Give a statement a subject and a verb. Begin with a capital letter. End with a full stop. A command can have an understood subject: you.',writing_example='Earth moves around the Sun.',writing_page=43,
     express_frames=['Earth is in ___.','Our solar system is in ___.','I think I will ___.'],express_prompt='Tell someone where we are in the universe.',
     quiz=[('Which tool helps us see faraway space objects?',['a telescope','a uniform','a tomb'],0,'A telescope helps us see things far away.'),('Where is our solar system?',['in the Milky Way galaxy','inside the moon','inside an asteroid'],0,'Our solar system is in the Milky Way galaxy.'),('Bella’s journey in the poem is ___.',['an imaginary journey','a school bus trip','an ancient battle'],0,'She imagines the journey and ends in her bedroom.'),('A rock from space that reaches the ground is a ___.',['comet','meteorite','galaxy'],1,'A meteorite reaches the ground.'),('Choose a prediction.',['Earth is a planet.','I will visit an observatory someday.','The moon has craters.'],1,'Will shows what you think will happen.'),('When Bella travels farther away, Earth looks ___.',['smaller','larger','exactly the same size'],0,'Things look smaller when we move farther away.')]),
dict(id=2,title='Traveling around the Sun',subtitle='Compare planets. Find what makes Earth special.',big_question='Where are we in the universe?',color='#b76d2b',hero='hero-space',vocabulary=v2,contexts=context[1],
     reading_title='Traveling Together Around the Sun',genre='Science article · nonfiction',reading_strategy='Find what is the same and what is different.',reading_pages=[46,47,48],
     reading_chunks=[('Traveling together','The planets move around the Sun. Gravity keeps them in their orbits. The Sun gives Earth light and heat.'),('Compare two planets','Earth and Venus are almost the same size. Both have an iron and rock core. Venus is hotter and has thicker clouds.'),('Learning more','Astronomers study space. Space probes collect information. The article explains how Curiosity explored the surface of Mars.')],
     thinking_prompt='Compare Earth and Venus. Name one similarity and one difference.',thinking_frame='Both Earth and Venus ___. However, Venus ___.',
     grammar_title='Link a possibility and a result',grammar_name='Future real conditional',grammar_page=49,grammar_pattern='If + present simple, subject + will + base verb',grammar_example='If I get a telescope, I will look at the moon.',grammar_note='The if part gives a possible situation. The will part gives its future result.',grammar_frame='If I ___, I will ___.',
     grammar_checks=[('If I ___ a telescope, I will study the moon.',['will get','get','got'],1,'Use present simple after if: get.'),('If we study space, we ___ learn new things.',['will','were','did'],0,'Use will + base verb for the future result.')],
     word_study=dict(title='Words with -ance and -ant',page=51,note='Compare the noun and adjective in each pair.',words=['fragrance → fragrant','abundance → abundant','ignorance → ignorant']),
     listening_title='The Speed of Light',listening_goal='Listen for the main idea and numbers.',listening_page=214,listening_script='This report is about the speed of light. Light moves very fast: almost three hundred thousand kilometers in one second. Light from the Sun takes about eight minutes to reach Earth. A light-year is the distance light travels in one year.',listening_question='How long does light from the Sun take to reach Earth?',listening_answer='About eight minutes.',
     speaking_title='Ask about quantity',speaking_frame='How many ___ are there? How much ___ is there?',speaking_page=51,writing_title='Ask a choice question',writing_tip='Use or to offer choices. End your question with a question mark.',writing_example='Is Mars a moon or a planet?',writing_page=51,
     express_frames=['Both Earth and Venus ___.','However, Venus ___.','If I study space, I will ___.'],express_prompt='Compare Earth and Venus. Explain one similarity and one difference.',
     quiz=[('Earth and Venus are almost the same ___.',['size','temperature','color'],0,'The reading says they are almost the same size.'),('Which planet has thicker clouds in the reading?',['Earth','Venus','both have no clouds'],1,'Venus is covered in thick clouds.'),('A space probe is used to ___.',['collect information','make uniforms','bury treasure'],0,'A space probe collects information about space.'),('Choose the correct sentence.',['If I will study, I learn.','If I study, I will learn.','If I studying, I will learn.'],1,'Use present simple after if, then will + base verb.'),('A diameter goes across a circle through its ___.',['center','outside only','top only'],0,'A diameter passes through the center.'),('Which question asks about things we can count?',['How many planets are there?','How much water is there?','Why is Venus hot?'],0,'Use how many with countable things, such as planets.')]),
dict(id=3,title='Clues from long ago',subtitle='Look closely. What can old objects tell us?',big_question='How do we know what happened long ago?',color='#247e80',hero='hero-history',vocabulary=v3,contexts=context[2],
     reading_title='Hidden Army: Clay Soldiers of Ancient China',genre='Magazine article · nonfiction',reading_strategy='Ask why the author wrote each part.',reading_pages=[58,59,60],
     reading_chunks=[('An army made of clay','The article describes thousands of clay soldiers in ancient China. They were made more than two thousand years ago.'),('Look for clues','The soldiers do not all look the same. Their faces and uniforms give clues about real soldiers and their ranks.'),('Study and protect','Archaeologists study the soldiers. Scientists try to protect the remaining paint. In the reading, the emperor’s tomb has not been opened.')],
     thinking_prompt='Find a fact in the summary. How does it help the author inform us?',thinking_frame='The author informs us that ___. I know because ___.',
     grammar_title='Say what you plan or hope to do',grammar_name='Verbs followed by infinitives',grammar_page=61,grammar_pattern='want / plan / hope / decide / try + to + base verb',grammar_example='I want to learn about the clay soldiers.',grammar_note='An infinitive is to + a base verb. Some verbs are followed by an infinitive.',grammar_frame='I want to ___. I plan to ___.',
     grammar_checks=[('I want ___ an archaeologist.',['be','to be','being'],1,'Want is followed by an infinitive: to be.'),('They decided to ___ the old objects.',['study','studied','studying'],0,'After to, use the base verb: study.')],
     word_study=dict(title='Words with -ist',page=63,note='In these words, -ist names a person who does an activity or job.',words=['cyclist','cartoonist','dentist','florist','tourist','pianist']),
     listening_title='An Ancient Town',listening_goal='Listen for similarities and differences.',listening_page=214,listening_script='Children describe an ancient town in Bulgaria. People there used salt bricks for trade. Salt helped keep food fresh. Today we often use refrigerators. The ancient town had houses with two floors. Many houses today also have two floors.',listening_question='What is one similarity between the ancient town and towns today?',listening_answer='Both can have houses with two floors.',
     speaking_title='Give a reason',speaking_frame='I would like to visit ___. I want to see ___ because ___.',speaking_page=63,writing_title='Keep verb tenses consistent',writing_tip='When you describe a past event, use past-tense verbs together.',writing_example='The archaeologist studied the tomb and found old objects.',writing_page=63,
     express_frames=['The soldiers were made from ___.','We learn about the past by ___.','I want to ___ because ___.'],express_prompt='Explain how old objects help us learn about the past.',
     quiz=[('The ancient soldiers in the article were made from ___.',['clay','ice','paper'],0,'The terracotta soldiers were made from clay.'),('Who studies old objects to learn about the past?',['an astronomer','an archaeologist','a tourist'],1,'An archaeologist studies objects from the past.'),('Which sentence tells a fact?',['The soldiers were made of clay.','Please visit the museum!','Imagine a soldier waking up!'],0,'The material is a fact that informs us.'),('Choose the correct sentence.',['I want learn about China.','I want to learn about China.','I want to learning about China.'],1,'Use want + to + base verb.'),('Choose two past-tense verbs.',['studies and found','studied and finds','studied and found'],2,'Keep the past tense consistent: studied and found.'),('What can uniforms help us learn about?',['soldiers’ ranks','the speed of light','a planet’s diameter'],0,'The reading uses uniforms as clues about soldiers’ ranks.')])]

hybrid=json.loads((DATA/'hybrid.json').read_text(encoding='utf-8'))
units[0]['hero']='hero-bella'
for unit in units:
    unit['hybrid']=hybrid[str(unit['id'])]
    for v in unit['vocabulary']:
        key=f'u{unit["id"]}-{v["word"].replace(" ","-")}'
        asset=next(x for x in manifest if x['id']==key)
        v.update(id=key,visual=key,source_label='CORE-BOOK',source_pdf_page={1:36,2:44,3:56}[unit['id']],
                 student_book_page={1:8,2:16,3:28}[unit['id']],visual_role=asset['match_status'])
        if unit['id']==2:
            v['recall_hint']={
                'astronomer':'Name the scientist who studies space.',
                'space probe':'Name this robot spacecraft.',
                'core':'Name the center part of Earth.',
                'gravity':'What force pulls this object down?',
                'orbit':'Name the path around the Sun.',
                'matter':'What are rock, water and air examples of?',
                'distance':'What do we measure between these objects?',
                'diameter':'Name the line across a circle through its center.',
                'surface':'Name the outside part we can see.',
                'craters':'Name the large hollows on the Moon.',
                'unique':'Which word means different from all the others?'
            }[v['word']]
    unit['source_pages'] = dict(vocabulary={1:36,2:44,3:56}[unit['id']],scope=[2,3],
                                reading=unit['reading_pages'],grammar=unit['grammar_page'],
                                word_study=unit['word_study']['page'],listening=unit['listening_page'],
                                speaking=unit['speaking_page'],writing=unit['writing_page'])

review_path=ROOT/'qa'/'visual-review.json'
if review_path.exists():
    reviewed=json.loads(review_path.read_text(encoding='utf-8'))
    for asset in manifest:
        record=reviewed.get(asset['id'],{})
        if record.get('sha256')==hashlib.sha256((ROOT/asset['asset_path']).read_bytes()).hexdigest():
            asset['review_status']='visually-reviewed'

payload=dict(source=dict(file=PDF.name,sha256=hashlib.sha256(PDF.read_bytes()).hexdigest(),edition='Oxford Discover 4, Second Edition, Teacher’s Guide (2019)',
                        scope='Book-based Units 1-3 with class diary supplements; Unit 4 entries excluded from core scope',pronunciation='American-English learning transcription; sound-it-out is approximate; audio uses browser TTS, not book recordings.'),
             units=units,assets=manifest,classwork=json.loads((DATA/'classwork.json').read_text(encoding='utf-8')))
(DATA/'review.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
(DATA/'image-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
template=(ROOT/'web'/'review.template.html').read_text(encoding='utf-8')
packed=dict(**payload,images=images)
serialized=json.dumps(packed,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
template=template.replace('__V2_STYLES__',(ROOT/'web/v2.css').read_text(encoding='utf-8'))
template=template.replace('__V2_SCRIPT__',(ROOT/'web/v2.js').read_text(encoding='utf-8'))
(ROOT/'index.html').write_text(template.replace('__REVIEW_DATA__',serialized),encoding='utf-8')
print(f'Built index.html: {(ROOT/"index.html").stat().st_size:,} bytes, {len(manifest)} visuals, {sum(len(u["vocabulary"]) for u in units)} core words.')

# Contact sheet uses existing book crops without editing their content.
book=[x for x in manifest if x['source_file']]
sheet=Image.new('RGB',(720,((len(book)+5)//6)*150),'#ffffff')
draw=ImageDraw.Draw(sheet)
for n,asset in enumerate(book):
    im=Image.open(ROOT/asset['asset_path']).convert('RGB'); im.thumbnail((110,112))
    x=(n%6)*120; y=(n//6)*150
    sheet.paste(im,(x+(120-im.width)//2,y+5)); draw.text((x+4,y+120),asset['id'],fill='#222222')
(ROOT/'qa').mkdir(exist_ok=True)
sheet.save(ROOT/'qa'/'book-image-contact-sheet.jpg')
