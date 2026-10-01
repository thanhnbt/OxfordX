const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 960, height: 540 },
    deviceScaleFactor: 1
  });

  const htmlPath = path.resolve('../hybrid_export/presentation.html');
  
  async function snapSlide(slideIdx, name) {
      await page.goto(`file://${htmlPath}`);
      await page.evaluate((idx) => {
          currentSlideIdx = idx;
          const slide = slides[idx];
          currentStep = parseInt(slide.getAttribute('data-max-step') || 0);
          updateView();
      }, slideIdx);
      await page.waitForTimeout(500);
      await page.screenshot({ path: path.join(__dirname, name) });
      console.log(`Saved ${name}`);
  }

  await snapSlide(0, 'true_slide_1.png');
  await snapSlide(3, 'true_slide_4.png');
  await snapSlide(6, 'true_slide_7.png');
  await snapSlide(7, 'true_slide_8.png');

  await browser.close();
})();
