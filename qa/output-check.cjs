const {chromium,launchOptions}=require('./runtime.cjs');
const path=require('path');
const {pathToFileURL}=require('url');
const assert=require('assert/strict');

(async()=>{
 let passed=0;
 const check=(condition,message)=>{assert.ok(condition,message);passed++};
 const browser=await chromium.launch(launchOptions());
 const page=await browser.newPage({viewport:{width:1280,height:900}});
 const menuUrl=pathToFileURL(path.resolve('index.html')).href;
 await page.goto(menuUrl);
 check(await page.locator('.unit-link').count()===3,'main menu should link to three Units');
 check(await page.locator('script').count()===0,'main menu should not contain the learning app runtime');
 check(await page.locator('.unit-visual').evaluateAll(images=>images.length===3&&images.every(image=>image.complete&&image.naturalWidth>0)),'main menu book visuals should decode');
 for(const id of [1,2,3]){
  const unitPage=await browser.newPage({viewport:{width:1280,height:900}});
  const unitUrl=pathToFileURL(path.resolve(`output/unit-${id}.html`)).href;
  await unitPage.goto(unitUrl);
  await unitPage.waitForSelector('.unit-hero');
  check(JSON.stringify(await unitPage.evaluate(()=>DATA.units.map(unit=>unit.id)))===JSON.stringify([id]),`Unit ${id} should bundle only its own data`);
  check(await unitPage.locator('.unit-hero h1').count()===1,`Unit ${id} should open directly`);
  check(await unitPage.evaluate(()=>{const rail=document.querySelector('.sidebar').getBoundingClientRect(),workspace=document.querySelector('.workspace').getBoundingClientRect();return Math.abs(rail.right-workspace.left)<1}),`Unit ${id} visible activity rail should meet the workspace without a gap`);
  await unitPage.locator('#nav [data-tab="words"]').click();
  check(await unitPage.evaluate(()=>{const hero=document.querySelector('.unit-hero').getBoundingClientRect(),question=document.querySelector('.question').getBoundingClientRect(),activity=document.querySelector('#activity').getBoundingClientRect();return Math.abs(hero.left-question.left)<1&&Math.abs(hero.left-activity.left)<1&&document.documentElement.scrollWidth<=innerWidth}),`Unit ${id} heading, question and activity should align without a phantom column`);
  check(await unitPage.locator('#nav.activity-menu .activity-menu-item').count()===6,`Unit ${id} should show all six activities in the sidebar`);
  check(await unitPage.locator('#main>.tabs').count()===0,`Unit ${id} should not repeat the menu horizontally`);
  check(await unitPage.locator('.breadcrumb .main-menu-link').getAttribute('href')==='../index.html',`Unit ${id} should link back to the main menu`);
  for(const [tab,label] of [['map','Connect'],['words','Picture words'],['reading','Read & think'],['language','Grammar Lab'],['express','Tell it'],['check','Remember']]){
   await unitPage.locator(`#nav [data-tab="${tab}"]`).click();
   check(await unitPage.evaluate(()=>state.tab===document.querySelector('#nav .active')?.dataset.tab),`Unit ${id} sidebar item ${label} should control its activity`);
  }
  await unitPage.getByRole('button',{name:'Read & think',exact:true}).click();
  if(id===3){
   const lesson=unitPage.frameLocator('iframe[title="Unit 3 full reading lesson"]');
    check(await lesson.locator('#audio').count()===1,'embedded lesson audio must remain present');
    check(await lesson.locator('.word[data-g][data-w]').count()>0,'thought-group word markers must remain present');
    check(await lesson.locator('.book-spread').count()===1&&await lesson.locator('#scan').count()===0,'reading must use one HTML spread without a duplicate page scan');
    check(await lesson.locator('.book-spread img').evaluateAll(images=>images.length===4&&images.every(image=>image.complete&&image.naturalWidth>0)),'all four original illustration crops must decode');
    for(const control of ['#startBtn','#prevBtn','#playBtn','#nextBtn','#repeatBtn'])check(await lesson.locator(control).count()===1,`original ${control} audio control must remain present`);
    await lesson.locator('#audio').evaluate(audio=>{window.AudioContext=undefined;window.webkitAudioContext=undefined;audio.play=()=>{window.__lessonPlayRequested=true;return Promise.resolve()}});
    const previousTime=await lesson.locator('#audio').evaluate(audio=>audio.currentTime);
    await lesson.locator('.thought').nth(2).click();
    check(await lesson.locator('#audio').evaluate(audio=>window.__lessonPlayRequested===true),'clicking a thought group must seek and request audio playback');
    check(await lesson.locator('#audio').evaluate((audio,time)=>audio.currentTime>time,previousTime),'clicking a thought group must seek forward on the original audio timeline');
  }else{
    check(await unitPage.locator('iframe[title="Unit 3 full reading lesson"]').count()===0,`Unit ${id} should not contain Unit 3 lesson data`);
  }
  await unitPage.setViewportSize({width:390,height:844});
  check(await unitPage.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`Unit ${id} sidebar menu should not overflow on mobile`);
  await unitPage.locator('.breadcrumb .main-menu-link').click();
  check(await unitPage.locator('.unit-link').count()===3,`Unit ${id} breadcrumb should return to index.html`);
  await unitPage.close();
 }
 await browser.close();
 console.log(JSON.stringify({passed,failed:0}));
})().catch(error=>{console.error(error);process.exit(1)});
