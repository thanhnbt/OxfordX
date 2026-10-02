const {chromium,launchOptions}=require('./runtime.cjs');
const fs=require('fs');
const path=require('path');
const {pathToFileURL}=require('url');
const assert=require('assert/strict');
const http=require('http');

(async()=>{
 const browser=await chromium.launch(launchOptions({args:['--no-first-run','--disable-gpu']}));
 const context=await browser.newContext({viewport:{width:1440,height:1000}});
 await context.addInitScript(()=>{window.OXFORD_AUDIO={enabled:false}});
 const page=await context.newPage();
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const results=[];
 const check=(name,pass,detail='')=>{results.push({name,status:pass?'PASS':'FAIL',detail});assert.ok(pass,name+': '+detail)};
 const url=pathToFileURL(path.resolve('tmp/qa/full-review.html')).href;
 await page.goto(url+'#home');await page.waitForSelector('.unit-card');
 check('Home has three units',await page.locator('.unit-card').count()===3);
 check('No horizontal overflow desktop',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 await page.screenshot({path:'qa/desktop-home.png',fullPage:true});
 const images=await page.evaluate(()=>Array.from(document.images).filter(i=>!i.complete||!i.naturalWidth).map(i=>i.alt));
 check('All embedded images decode',images.length===0,JSON.stringify(images));
 await page.getByRole('button',{name:'Explore Unit 1'}).click();
 await page.getByRole('button',{name:'2 · Build'}).click();
 check('Map shows relations',await page.locator('.map-arrow').count()===3);
 await page.getByRole('button',{name:'4 · Recall'}).click();
 check('Map recall hides labels',await page.locator('.map-node strong').allTextContents().then(x=>x.every(t=>t==='?')));
 await page.getByRole('button',{name:'Picture words',exact:true}).click();
 check('All 11 words appear on one page',await page.locator('.vocab-card').count()===11);
 await page.screenshot({path:'qa/desktop-unit1-words.png',fullPage:true});
 await page.getByRole('button',{name:'Hide & remember',exact:true}).click();
 check('Recall hides answers and pronunciation',await page.locator('#activity .vocab-title,#activity .phonetic,#activity .sound-out,#activity .definition').count()===0);
 check('Recall alt text does not disclose headword',await page.locator('.vocab-picture img').evaluateAll(imgs=>imgs.every(i=>i.alt==='Picture clue. Say the word before revealing it.')));
 await page.getByRole('button',{name:'Reveal the word',exact:true}).first().click();
 check('Reveal opens one word',await page.locator('.vocab-title').count()===1);
 await page.getByRole('button',{name:'My sentence',exact:true}).click();
 await page.locator('[data-note="u1-moon"]').fill('I can see the moon.');
 await page.getByRole('button',{name:'Mark as practised'}).click();
 await page.reload();await page.getByRole('button',{name:'My sentence',exact:true}).first().click();
 check('Notes survive reload',await page.locator('[data-note="u1-moon"]').inputValue()==='I can see the moon.');
 check('Practised flag survives reload',await page.locator('[data-action="practise"][data-id="u1-moon"]').getAttribute('aria-pressed')==='true');
 await page.locator('#word-search').fill('telescope');
 check('Search filters cards',await page.locator('.vocab-card').count()===1&&await page.locator('.vocab-title').innerText().then(t=>t.includes('telescope')));
 await page.locator('#word-search').fill('');
 await page.getByRole('button',{name:'Read & think',exact:true}).click();
 await page.locator('[data-answer="u1-thinking"]').fill('Earth looks smaller when Bella moves away.');
 await page.getByRole('button',{name:'Grammar Lab',exact:true}).click();
 await page.locator('[data-action="grammar-step"][data-step="try"]').first().click();
 await page.locator('[data-action="grammar-answer"][data-question="0"][data-option="1"]').click();
 check('Grammar gives retry feedback',await page.locator('#grammar-feedback-0').innerText().then(t=>t.startsWith('Try again.')));
 await page.locator('[data-action="grammar-answer"][data-question="0"][data-option="0"]').click();
 check('Grammar correct response',await page.locator('#grammar-feedback-0').innerText().then(t=>t.startsWith('Yes!')));
 await page.getByRole('button',{name:'Tell it',exact:true}).click();
 await page.getByRole('button',{name:'Write it',exact:false}).click();
 await page.locator('[data-answer="u1-expression"]').fill('Earth is in our solar system.');
 await page.locator('#check-u1-words').check();
 await page.reload();
 check('Open response survives reload',await page.locator('[data-answer="u1-expression"]').inputValue()==='Earth is in our solar system.');
 check('Self-check survives reload',await page.locator('#check-u1-words').isChecked());

 // Speech API contract test: deterministic mock, exact target and chosen English voice.
 await page.evaluate(()=>{window.__spoken=[];window.SpeechSynthesisUtterance=class{constructor(text){this.text=text}};Object.defineProperty(window,'speechSynthesis',{configurable:true,value:{getVoices:()=>[{name:'QA English',lang:'en-US',voiceURI:'qa-en'}],cancel(){},addEventListener(){},removeEventListener(){},speak(u){window.__spoken.push({text:u.text,lang:u.lang,rate:u.rate})}}})});
 await page.getByRole('button',{name:'Picture words',exact:true}).click();
 await page.getByRole('button',{name:'Hear stars',exact:true}).click();
 await page.waitForFunction(()=>window.__spoken.length>0);
 check('Audio requests exact plural target',await page.evaluate(()=>window.__spoken.at(-1).text==='stars'&&window.__spoken.at(-1).lang==='en-US'));
 await page.getByRole('button',{name:'Open audio settings',exact:true}).click();
 await page.locator('#rate-select').selectOption('0.65');
 await page.getByRole('button',{name:'Try the voice',exact:true}).click();
 check('Audio speed setting applied',await page.evaluate(()=>window.__spoken.at(-1).rate===.65));
 await page.getByRole('button',{name:'Close audio settings',exact:true}).click();

 for(const unit of [1,2,3]){
  await page.locator(`[data-action="unit"][data-unit="${unit}"]`).first().click();
  for(const tab of ['map','words','reading','language','express']){
   await page.locator(`[data-action="tab"][data-tab="${tab}"]`).first().click();
   check(`Unit ${unit}: ${tab} renders`,await page.locator('#activity').innerText().then(t=>t.length>30));
  }
  await page.locator('[data-action="tab"][data-tab="check"]').first().click();
  const qdata=await page.evaluate(id=>DATA.units.find(u=>u.id===id).quiz,unit);
  for(let i=0;i<qdata.length;i++){
   check(`Unit ${unit} question ${i+1}: feedback hidden before answer`,await page.locator('.quiz-feedback').count()===0);
   await page.locator(`[data-action="quiz-answer"][data-option="${i===0?(qdata[i][2]+1)%3:qdata[i][2]}"]`).click();
   await page.locator('[data-action="next-question"]').click();
  }
  check(`Unit ${unit}: score reflects answers`,await page.locator('.score-circle').innerText()==='5/6');
  check(`Unit ${unit}: mistakes have review`,await page.locator('.review-mistake').count()===1);
 }
 await page.locator('#nav [data-action="mixed"]').click();
 const balance=await page.evaluate(()=>state.quiz.list.reduce((x,q)=>(x[q.unit]=(x[q.unit]||0)+1,x),{}));
 check('Mixed quiz has three questions from each unit',JSON.stringify(balance)===JSON.stringify({1:3,2:3,3:3}));
 for(let i=0;i<9;i++){const correct=await page.evaluate(()=>state.quiz.list[state.quiz.position].q[2]);await page.locator(`[data-action="quiz-answer"][data-option="${correct}"]`).click();await page.locator('[data-action="next-question"]').click()}
 check('Mixed quiz completes',await page.locator('.score-circle').innerText()==='9/9');
 await page.getByRole('button',{name:'For grown-ups',exact:true}).click();
 check('Parent mode is a labelled modal',await page.locator('#parent-dialog').evaluate(d=>d.open));
 await page.keyboard.press('Escape');
 check('Escape closes parent mode',await page.locator('#parent-dialog').evaluate(d=>!d.open));
 await page.locator('[data-action="unit"][data-unit="2"]').click();
 await page.getByRole('button',{name:'Picture words',exact:true}).click();
 await page.screenshot({path:'qa/desktop-unit2-words.png',fullPage:true});
 for(const width of [390,768]){
  await page.setViewportSize({width,height:844});
  for(const unit of [0,1,2,3]){
   if(!unit)await page.locator('[data-action="home"]').first().click();else await page.locator(`[data-action="unit"][data-unit="${unit}"]`).first().click();
   const list=unit?['map','words','reading','language','express','check']:['home'];
   for(const tab of list){if(unit)await page.locator(`[data-action="tab"][data-tab="${tab}"]`).first().click();check(`${width}px Unit ${unit} ${tab}: no overflow`,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),String(await page.evaluate(()=>document.documentElement.scrollWidth)))}
  }
 }
 await page.setViewportSize({width:390,height:844});await page.locator('[data-action="unit"][data-unit="3"]').click();await page.getByRole('button',{name:'Picture words',exact:true}).click();
 await page.screenshot({path:'qa/mobile-unit3-words.png',fullPage:true});
 await page.locator('[data-action="home"]').click();await page.screenshot({path:'qa/mobile-home.png',fullPage:true});
 await page.setViewportSize({width:1440,height:1000});
 await page.emulateMedia({media:'print'});
 check('Print pack has all 33 words',await page.locator('.print-word').count()===33);
 check('Print hides interactive main',await page.locator('#main').evaluate(e=>getComputedStyle(e).display==='none'));
 await page.pdf({path:'qa/print-review.pdf',format:'A4',printBackground:true,preferCSSPageSize:true});
 check('No JavaScript runtime errors',errors.length===0,JSON.stringify(errors));

 // Storage-disabled path must keep the app usable and report failed persistence.
 const blocked=await context.newPage();await blocked.addInitScript(()=>Object.defineProperty(window,'localStorage',{get(){throw new Error('storage blocked')}}));
 await blocked.goto(url+'#unit-1-reading');await blocked.locator('[data-answer="u1-thinking"]').fill('My idea');
 check('Storage-disabled path reports visit-only saving',await blocked.locator('[data-save-status="u1-thinking"]').innerText().then(t=>t.includes('Kept for this visit')));
 const noAudio=await context.newPage();await noAudio.addInitScript(()=>Object.defineProperty(window,'speechSynthesis',{configurable:true,value:undefined}));
 await noAudio.goto(url+'#unit-1-words');
 await noAudio.getByRole('button',{name:'Hear moon',exact:true}).click();
 check('Absent speech API gives useful fallback',await noAudio.locator('#toast').innerText().then(t=>t.includes('Voice is not available')));
 await noAudio.close();
 const noEnglish=await context.newPage();await noEnglish.addInitScript(()=>{window.SpeechSynthesisUtterance=class{constructor(text){this.text=text}};Object.defineProperty(window,'speechSynthesis',{configurable:true,value:{getVoices:()=>[{name:'Other language',lang:'vi-VN',voiceURI:'qa-vi'}],cancel(){},addEventListener(){},removeEventListener(){},speak(){throw new Error('Should not use unrelated language')}}})});
 await noEnglish.goto(url+'#unit-1-words');await noEnglish.getByRole('button',{name:'Hear moon',exact:true}).click();await noEnglish.waitForFunction(()=>document.querySelector('#toast').textContent.includes('No English voice'));
 check('Non-English voice is not substituted',await noEnglish.locator('#toast').innerText().then(t=>t.includes('No English voice')));await noEnglish.close();
 const server=http.createServer((req,res)=>{if(req.url==='/favicon.ico'){res.writeHead(204);res.end();return}res.writeHead(200,{'Content-Type':'text/html; charset=utf-8'});res.end(fs.readFileSync('tmp/qa/full-review.html'))});
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const hosted=await context.newPage();await hosted.goto(`http://127.0.0.1:${server.address().port}/`);await hosted.waitForSelector('.unit-hero');
 check('Static HTTP hosting starts Unit 1 directly',await hosted.evaluate(()=>state.unit===1)&&await hosted.locator('#nav [data-action="unit"]').count()===3);
 check('Hosted images decode without asset folder',await hosted.evaluate(()=>Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)));
 await hosted.locator('[data-action="unit"][data-unit="2"]').first().click();await hosted.getByRole('button',{name:'Read & think',exact:true}).click();await hosted.locator('[data-answer="u2-thinking"]').fill('Both have a core.');await hosted.reload();
 check('Hosted origin persists notes',await hosted.locator('[data-answer="u2-thinking"]').inputValue()==='Both have a core.');
 await hosted.close();await new Promise(resolve=>server.close(resolve));
 const report={checks:results,summary:{passed:results.filter(x=>x.status==='PASS').length,failed:results.filter(x=>x.status==='FAIL').length},runtimeErrors:errors,limitations:['Speech assertions use a mock; audible voice quality must be checked on the learner device.','No observation with the learner yet.']};
 fs.writeFileSync('qa/browser-results.json',JSON.stringify(report,null,2));
 await browser.close();console.log(JSON.stringify(report.summary));
})().catch(e=>{console.error(e);process.exit(1)});
