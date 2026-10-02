const {chromium,launchOptions}=require('./runtime.cjs');
const fs=require('fs'),path=require('path'),assert=require('assert/strict');
const {pathToFileURL}=require('url');
(async()=>{
 let passed=0;const check=(ok,msg)=>{assert(ok,msg);passed++};
 const original=fs.readFileSync('inputdata/Unit3/lesson.html','utf8');
 const b=await chromium.launch(launchOptions());const p=await b.newPage();
 for(const width of [390,768,1440]){
  await p.setViewportSize({width,height:1000});await p.goto(pathToFileURL(path.resolve('output/unit-3.html')).href+'#unit-3-reading');
  const f=p.frameLocator('iframe');await f.locator('.book-spread').waitFor();
  check(await p.locator('#activity .reading-text').count()===1,'original bilingual reading review preserved');
  check(await p.locator('#answer-u3-thinking').count()===1&&await p.locator('#answer-u3-listening').count()===1,'existing learner answer fields preserved');
  if(width===390)check(await f.locator('.left-copy').evaluate(e=>e.getBoundingClientRect().width>=innerWidth*.85),'mobile reading uses full width instead of a narrow column beside the image');
  const result=await f.locator('body').evaluate(()=>({
   groups:[...document.querySelectorAll('.book-spread .thought')].map(e=>e.dataset.id),
   words:[...document.querySelectorAll('.book-spread .word')].map(e=>[e.dataset.g,e.dataset.w,e.textContent]),
   script:document.querySelector('script').textContent,
   scans:document.querySelectorAll('#scan,.side,.layout').length,
   decode:[...document.querySelectorAll('.book-spread img')].every(i=>i.complete&&i.naturalWidth),
   top:document.querySelector('.player').getBoundingClientRect().bottom<=document.querySelector('.book-scroll').getBoundingClientRect().top,
   overflow:document.documentElement.scrollWidth>innerWidth,
   recap:document.querySelectorAll('.book-spread').length,
  }));
  check(result.groups.length===90&&new Set(result.groups).size===90,'each timed thought appears once');
  const expected=[...original.matchAll(/class="word" data-g="(\d+)" data-w="(\d+)">([^<]*)/g)].map(m=>[m[1],m[2],m[3].replace(/&#x27;/g,"'").replace(/&amp;/g,'&')]);
  check(JSON.stringify(result.words)===JSON.stringify(expected),'all words retain exact source order and timing keys');
  check(result.scans===0&&result.recap===1,'only one live HTML spread');
  check(result.decode,'four original illustrations decode');check(result.top,'player sits above reading');check(!result.overflow,'responsive page has no horizontal overflow');
  check(result.script.match(/AB64="([^"]+)"/)[1]===original.match(/AB64="([^"]+)"/)[1],'audio bytes unchanged');
  check(result.script.split('const G=')[1].split('IMGS=')[0]===original.split('const G=')[1].split('IMGS=')[0],'audio timing unchanged');
  await f.locator('#audio').evaluate(a=>{window.AudioContext=undefined;window.webkitAudioContext=undefined;a.play=()=>Promise.resolve()});
  for(const id of [2,44,89]){await f.locator(`.thought[data-id="${id}"]`).click();check(await f.locator('.thought.active').getAttribute('data-id')===String(id),'click highlights requested thought');check(await f.locator('#audio').evaluate(a=>a.currentTime>48),'click seeks original audio');}
  await f.locator('#repeatBtn').click();check(await f.locator('.thought.active').getAttribute('data-id')==='89','repeat retains selected thought');
  check(await f.locator('.player').evaluate(e=>e.getBoundingClientRect().top>=0&&e.getBoundingClientRect().bottom<=innerHeight),'audio controls stay visible after jumping through the reading');
 }
 await b.close();console.log(JSON.stringify({passed,failed:0}));
})().catch(e=>{console.error(e);process.exit(1)});
