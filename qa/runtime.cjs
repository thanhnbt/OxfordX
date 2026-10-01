const { chromium } = require('playwright');
const fs = require('fs');
function launchOptions(extra = {}) {
  const options = { headless: true, ...extra };
  const override = process.env.OXFORD_BROWSER_PATH;
  const edge = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
  if (override) options.executablePath = override;
  else if (process.platform === 'win32' && fs.existsSync(edge)) options.executablePath = edge;
  return options;
}
module.exports = { chromium, launchOptions };
