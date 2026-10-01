const {chromium,launchOptions}=require('./runtime.cjs');
const fs=require('fs');
const path=require('path');
const {pathToFileURL}=require('url');
const assert=require('assert/strict');
let browser;
(async()=>{
 browser=await chromium.launch(launchOptions({args:['--no-first-run','--disable-gpu']}));
 const context=await browser.newContext({viewport:{width:1440,height:1000}});
 await context.addInitScript(()=>{window.OXFORD_AUDIO={enabled:false}});
 const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const capture=async filename=>{await page.evaluate(()=>{window.scrollTo({top:0,behavior:'instant'});document.querySelector('#toast').hidden=true});await page.screenshot({path:filename,fullPage:true})};
 const results=[];const check=(name,value,detail='')=>{results.push({name,status:value?'PASS':'FAIL',detail});assert.ok(value,name+': '+detail)};
 const url=pathToFileURL(path.resolve('index.html')).href;
 await page.goto(url);
 check('Opening the file starts Unit 1 immediately',await page.evaluate(()=>state.unit===1&&state.tab==='map'));
 check('Default screen has working learning activities',await page.locator('.tabs [data-action="tab"]').count()===6);
 check('Unit heading uses the correct name',await page.locator('.unit-hero .eyebrow').innerText().then(t=>t.startsWith('UNIT 1')));
 await page.locator('[data-action="home"]').click();
 check('Overview has no Chapter labels',await page.locator('#main').innerText().then(t=>! /chapter/i.test(t)));
 check('Hybrid is the default',await page.evaluate(()=>progress.learningMode==='hybrid'));
 check('Unit rail visible on desktop',await page.locator('.sidebar').evaluate(e=>getComputedStyle(e).height==='1000px'));
 check('Grammar has three home shortcuts',await page.locator('.grammar-shortcut').count()===3);
 await capture('qa/v2-desktop-home.png');
 await page.locator('[data-action="grammar-shortcut"][data-unit="1"]').click();
 check('Grammar shortcut opens Understand',await page.locator('[data-step="understand"]').getAttribute('aria-pressed')==='true');
 check('Grammar has three worked examples',await page.locator('.worked-example').count()===3);
 check('Grammar marks will and base verbs separately',await page.locator('.worked-example .marker').count()===3&&await page.locator('.worked-example .verb').count()===3);
 check('Hybrid grammar has Vietnamese explanations',await page.locator('.grammar-stage [lang="vi"]').count()>3);
 await capture('qa/v2-grammar-unit1.png');
 await page.locator('[data-action="learning-mode"][data-mode="english"]').click();
 check('English mode removes grammar Vietnamese scaffolding',await page.locator('.grammar-stage [lang="vi"]').count()===0);
 await page.reload();check('Language choice survives reload',await page.evaluate(()=>progress.learningMode==='english'));
 await page.locator('[data-action="learning-mode"][data-mode="hybrid"]').click();
 await page.locator('[data-action="tab"][data-tab="words"]').click();
 check('Hybrid vocab displays secondary Vietnamese meanings',await page.locator('.meaning-vi').count()===11);
 await capture('qa/v2-vocabulary.png');
 await page.locator('[data-action="study-mode"][data-mode="recall"]').click();
 check('Hybrid recall hides Vietnamese answers',await page.locator('#activity .meaning-vi').count()===0);
 await page.locator('[data-action="tab"][data-tab="reading"]').click();
 check('Reading has three faithful translated recaps',await page.locator('.reading-chunk .vi-support').count()===3);
 await page.locator('[data-action="unit"][data-unit="1"]').first().click();await page.locator('[data-action="tab"][data-tab="language"]').click();
 await page.locator('[data-action="grammar-step"][data-step="build"]').first().click();
 await page.locator('#idea-select').selectOption('1');
 check('Will builder produces a base verb sentence',await page.locator('#builder-result .sentence-parts').innerText().then(t=>t==='I will study the stars in the future.'));
 check('Will builder translation tracks choice',await page.locator('#builder-result [lang="vi"]').innerText().then(t=>t.includes('nghiên cứu các ngôi sao')));
 await page.evaluate(()=>{window.__spoken=[];window.SpeechSynthesisUtterance=class{constructor(text){this.text=text}};Object.defineProperty(window,'speechSynthesis',{configurable:true,value:{getVoices:()=>[{name:'English QA',lang:'en-US',voiceURI:'qa-en'}],cancel(){},addEventListener(){},removeEventListener(){},speak(u){window.__spoken.push(u.text)}}})});
 await page.locator('[data-action="speak-builder"]').click();check('Builder audio speaks exact constructed English',await page.evaluate(()=>__spoken.at(-1)==='I will study the stars in the future.'));
 await page.locator('[data-action="save-builder"]').click();check('Built sentence transfers to saved writing',await page.locator('[data-answer="u1-grammar"]').inputValue()==='I will study the stars in the future.');
 await page.locator('[data-question="0"][data-option="1"]').click();check('Wrong choice gives bilingual rule feedback',await page.locator('#grammar-feedback-0 .hybrid-check').innerText().then(t=>t.includes('Dùng will')));
 await page.locator('[data-question="0"][data-option="0"]').click();check('Retry replaces feedback without duplication',await page.locator('#grammar-feedback-0 .hybrid-check').count()===1);
 check('Error model is hidden before request',await page.locator('#error-model').isHidden());
 await page.locator('[data-answer="u1-error"]').fill('I will visit an observatory.');await page.locator('[data-action="error-model"]').click();check('Requested correction explains the rule',await page.locator('#error-model').isVisible()&&await page.locator('#error-model').innerText().then(t=>t.includes('visit, không phải visited')));
 for(const id of [2,3]){
  await page.locator(`[data-action="unit"][data-unit="${id}"]`).first().click();await page.locator('[data-action="tab"][data-tab="language"]').click();
  check(`Unit ${id}: grammar starts at Understand`,await page.locator('[data-step="understand"]').getAttribute('aria-pressed')==='true');
  check(`Unit ${id}: examples match source grammar`,await page.locator('.worked-example').count()===3);
  await capture(`qa/v2-grammar-unit${id}.png`);
  await page.locator('[data-action="grammar-step"][data-step="build"]').first().click();
  if(id===2){for(let i=0;i<3;i++){await page.locator('#idea-select').selectOption(String(i));const s=await page.locator('#builder-result .sentence-parts').innerText();check(`If builder ${i}: present if part, will result`,s.startsWith('If ')&&!s.split(',')[0].includes('will')&&s.split(',')[1].includes('will'));check(`If builder ${i}: translation present`,await page.locator('#builder-result [lang="vi"]').innerText().then(t=>t.startsWith('Nếu')))}}
  else{await page.locator('#idea-select').selectOption('1');await page.locator('#intent-select').selectOption('plan');check('Infinitive builder uses plan to visit',await page.locator('#builder-result .sentence-parts').innerText().then(t=>t==='I plan to visit a museum.'));check('Infinitive translation reflects plan',await page.locator('#builder-result [lang="vi"]').innerText().then(t=>t==='Em dự định đến thăm một bảo tàng.'));await page.locator('#intent-select').selectOption('hope');check('Changing intention preserves to + base verb',await page.locator('#builder-result .sentence-parts').innerText().then(t=>t==='I hope to visit a museum.'))}
 }
 for(const width of [390,768,1024]){
  await page.setViewportSize({width,height:844});
  await page.locator('[data-action="home"]').click();check(`${width}: home no overflow`,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  if(width===390)await capture('qa/v2-mobile-home.png');
  for(const id of [1,2,3]){
   await page.locator(`[data-action="unit"][data-unit="${id}"]`).first().click();await page.locator('[data-action="tab"][data-tab="language"]').click();
   for(const step of ['understand','build','try']){await page.locator(`[data-action="grammar-step"][data-step="${step}"]`).first().click();check(`${width}: Unit ${id} ${step} no overflow`,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));if(width===390&&id===2&&step==='understand')await capture('qa/v2-mobile-grammar.png')}
  }
 }
 await page.setViewportSize({width:1440,height:1000});await page.emulateMedia({media:'print'});await page.evaluate(()=>buildPrint());
 check('Print contains bilingual grammar scaffold for three units',await page.locator('.print-grammar-v2').count()===3);
 check('Print hides the chapter rail',await page.locator('.app-layout').evaluate(e=>getComputedStyle(e).display==='none'));
 await page.pdf({path:'qa/v2-print-review.pdf',format:'A4',printBackground:true,preferCSSPageSize:true});
 check('Bilingual grammar survives the beforeprint event',await page.locator('.print-grammar-v2').count()===3);
 check('No v2 JavaScript errors',errors.length===0,JSON.stringify(errors));
 const report={summary:{passed:results.filter(r=>r.status==='PASS').length,failed:results.filter(r=>r.status==='FAIL').length},checks:results,runtimeErrors:errors};fs.writeFileSync('qa/v2-results.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report.summary));await browser.close();
})().catch(async e=>{console.error(e);if(browser)await browser.close();process.exit(1)});
