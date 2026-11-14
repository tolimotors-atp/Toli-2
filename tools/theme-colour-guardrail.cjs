#!/usr/bin/env node
/**
 * Dark-theme colour-share guardrail.
 *
 * The dark theme is composed to read roughly 50% red-family, 40% graphite and
 * 10% gold by visual weight. Gold is deliberately a micro-accent, so its pixel
 * share is smaller than the visual brief; the bands below encode the values
 * this project actually accepts.
 *
 * Run against a built preview:
 *   npm run guardrail:theme
 *
 * Or against a running dev server:
 *   THEME_GUARDRAIL_URL=http://127.0.0.1:8190/Toli-2/ node tools/theme-colour-guardrail.cjs
 */
const { chromium } = require('playwright');
const sharp = require('sharp');
const { spawn } = require('node:child_process');
const fs = require('node:fs');
const http = require('node:http');
const os = require('node:os');
const path = require('node:path');

const ROOT = path.resolve(__dirname, '..');
const DEFAULT_URL = 'http://127.0.0.1:8200/Toli-2/';
const PAGE_URL = process.env.THEME_GUARDRAIL_URL || DEFAULT_URL;
const OWNS_SERVER = !process.env.THEME_GUARDRAIL_URL;

const BANDS = {
  desktop: {
    red: [47, 54],
    graphite: [38, 48],
    gold: [3, 8],
  },
  mobile: {
    red: [46, 54],
    graphite: [41, 52],
    gold: [1, 5],
  },
  sectionRed: [42, 68],
};

const SECTIONS = [
  ['services', '.journey-services'],
  ['component', '.component-chapter'],
  ['process', '.journey-process'],
  ['about', '.trust-chapter'],
  ['gallery', '.editorial-gallery'],
  ['reviews', '.customer-stories'],
  ['booking', '.journey-booking'],
  ['contact', '.experience-connect'],
  ['footer', '.journey-footer'],
];

function findChromium() {
  if (process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE) return process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE;
  const bundled = chromium.executablePath();
  if (fs.existsSync(bundled)) return bundled;
  const cache = path.join(os.homedir(), '.cache', 'ms-playwright');
  if (!fs.existsSync(cache)) return undefined;
  const builds = fs.readdirSync(cache).filter((name) => name.startsWith('chromium-')).sort().reverse();
  for (const build of builds) {
    for (const suffix of ['chrome-linux64/chrome', 'chrome-linux/chrome']) {
      const candidate = path.join(cache, build, suffix);
      if (fs.existsSync(candidate)) return candidate;
    }
  }
  return undefined;
}

function waitForServer(url, timeoutMs = 30000) {
  const started = Date.now();
  return new Promise((resolve, reject) => {
    const poll = () => {
      const request = http.get(url, (response) => {
        response.resume();
        if (response.statusCode && response.statusCode < 500) return resolve();
        retry();
      });
      request.on('error', retry);
      request.setTimeout(1500, () => request.destroy());
    };
    const retry = () => {
      if (Date.now() - started > timeoutMs) return reject(new Error(`Preview server did not answer at ${url}`));
      setTimeout(poll, 400);
    };
    poll();
  });
}

async function startPreview() {
  const dist = path.join(ROOT, 'dist', 'index.html');
  if (!fs.existsSync(dist)) {
    throw new Error('dist/index.html is missing. Run `npm run build` first, or set THEME_GUARDRAIL_URL.');
  }
  const child = spawn(
    path.join(ROOT, 'node_modules', '.bin', 'vite'),
    ['preview', '--host', '127.0.0.1', '--port', '8200', '--strictPort'],
    { cwd: ROOT, stdio: 'ignore' },
  );
  child.on('exit', (code) => {
    if (code && code !== 0) console.error(`vite preview exited with code ${code}`);
  });
  await waitForServer(PAGE_URL);
  return child;
}

function classify(r, g, b) {
  const max = Math.max(r, g, b);
  if (max < 34) return 'black';
  if (r >= 45 && r >= g * 1.35 && r >= b * 1.2) return 'red';
  if (r >= 70 && r > g * 1.08 && g > b * 1.18 && r < 245) return 'gold';
  return 'graphite';
}

function share(buffer, width, channels, top, bottom) {
  const counts = { red: 0, graphite: 0, gold: 0, black: 0 };
  let total = 0;
  for (let y = Math.max(0, top); y < bottom; y += 1) {
    for (let x = 0; x < width; x += 1) {
      const i = (y * width + x) * channels;
      counts[classify(buffer[i], buffer[i + 1], buffer[i + 2])] += 1;
      total += 1;
    }
  }
  const pct = (n) => Number(((n / total) * 100).toFixed(1));
  return {
    red: pct(counts.red),
    graphite: pct(counts.graphite + counts.black),
    gold: pct(counts.gold),
  };
}

async function capture(browser, viewport, label) {
  const context = await browser.newContext({ viewport, colorScheme: 'dark', deviceScaleFactor: 1 });
  const tab = await context.newPage();
  tab.setDefaultTimeout(120000);
  await tab.route('**/*', (route) => {
    const url = route.request().url();
    if (url.startsWith(new URL(PAGE_URL).origin) || url.startsWith('data:') || url.startsWith('blob:')) return route.continue();
    return route.abort();
  });
  await tab.goto(PAGE_URL, { waitUntil: 'commit', timeout: 120000 });
  await tab.waitForSelector('.reference-hero', { timeout: 120000 });
  await tab.waitForSelector('.journey-footer', { timeout: 120000 });
  await tab.waitForTimeout(2200);
  await tab.evaluate(() => { document.documentElement.dataset.theme = 'dark'; });

  for (const [, selector] of SECTIONS) {
    const element = tab.locator(selector).first();
    if (await element.count()) {
      await element.scrollIntoViewIfNeeded().catch(() => {});
      await tab.waitForTimeout(450);
    }
  }
  await tab.evaluate(() => {
    document.querySelectorAll('img[loading="lazy"]').forEach((img) => { img.loading = 'eager'; });
  });
  await tab.evaluate(async () => {
    const height = document.body.scrollHeight;
    for (let y = 0; y < height; y += 600) {
      window.scrollTo(0, y);
      await new Promise((resolve) => setTimeout(resolve, 70));
    }
    window.scrollTo(0, 0);
  });
  await tab.waitForFunction(
    () => [...document.images].every((img) => img.complete && img.naturalWidth > 0),
    null,
    { timeout: 60000 },
  ).catch(() => {});
  await tab.waitForTimeout(900);
  await tab.addStyleTag({
    content: '*,*::before,*::after{animation:none!important;transition:none!important;} canvas,video,iframe{visibility:hidden!important;}',
  });
  await tab.evaluate(() => {
    [...document.querySelectorAll('[data-motion],.reveal-section,.stagger-child')].forEach((el) => {
      el.classList.add('motion-visible', 'reveal-visible');
      el.style.opacity = '1';
      el.style.transform = 'none';
      el.style.clipPath = 'none';
    });
  });

  const boxes = await tab.evaluate((sectionSelectors) => {
    const rect = (selector) => {
      const element = document.querySelector(selector);
      if (!element) return null;
      const box = element.getBoundingClientRect();
      return { top: Math.round(box.top + window.scrollY), height: Math.round(box.height) };
    };
    return {
      heroBottom: rect('.reference-hero')?.top + rect('.reference-hero')?.height,
      sections: sectionSelectors.map(([name, selector]) => ({ name, ...rect(selector) })),
      height: document.body.scrollHeight,
    };
  }, SECTIONS);

  const png = await tab.screenshot({ fullPage: true, animations: 'disabled', timeout: 120000 });
  await context.close();
  const image = sharp(png);
  const { data, info } = await image.removeAlpha().raw().toBuffer({ resolveWithObject: true });
  if (info.height < 2000) throw new Error(`${label}: full-page capture failed (${info.width}x${info.height})`);

  const result = {
    label,
    viewport: `${viewport.width}x${viewport.height}`,
    height: info.height,
    overall: share(data, info.width, info.channels, boxes.heroBottom, info.height),
    sections: {},
  };
  for (const section of boxes.sections) {
    if (!section.top || !section.height) continue;
    result.sections[section.name] = share(data, info.width, info.channels, section.top, Math.min(info.height, section.top + section.height));
  }
  return result;
}

function check(label, value, [min, max]) {
  return value >= min && value <= max ? null : `${label} ${value}% outside ${min}-${max}%`;
}

function report(results) {
  const failures = [];
  console.log('\nDark theme colour-share guardrail');
  for (const result of results) {
    const band = result.label === 'desktop' ? BANDS.desktop : BANDS.mobile;
    console.log(`\n${result.label} ${result.viewport}`);
    for (const key of ['red', 'graphite', 'gold']) {
      const [min, max] = band[key];
      const value = result.overall[key];
      const problem = check(key, value, band[key]);
      console.log(`  ${key.padEnd(9)} ${String(value).padStart(5)}%  band ${min}-${max}%  ${problem ? 'FAIL' : 'PASS'}`);
      if (problem) failures.push(`${result.label}: ${problem}`);
    }
  }
  const desktop = results.find((result) => result.label === 'desktop');
  if (desktop) {
    console.log(`\nSection red share (band ${BANDS.sectionRed[0]}-${BANDS.sectionRed[1]}%)`);
    for (const [name, value] of Object.entries(desktop.sections)) {
      const problem = check(name, value.red, BANDS.sectionRed);
      console.log(`  ${name.padEnd(10)} ${String(value.red).padStart(5)}%  (graphite ${value.graphite}%, gold ${value.gold}%)  ${problem ? 'FAIL' : 'PASS'}`);
      if (problem) failures.push(`section: ${problem}`);
    }
  }
  if (failures.length) {
    console.error(`\nGuardrail failed:\n- ${failures.join('\n- ')}`);
    process.exitCode = 1;
  } else {
    console.log('\nGuardrail passed.');
  }
}

(async () => {
  let server;
  let browser;
  try {
    if (OWNS_SERVER) server = await startPreview();
    browser = await chromium.launch({ executablePath: findChromium(), headless: true });
    const desktop = await capture(browser, { width: 1366, height: 900 }, 'desktop');
    const mobile = await capture(browser, { width: 390, height: 844 }, 'mobile');
    const mobileSmall = await capture(browser, { width: 360, height: 800 }, 'mobile-small');
    report([desktop, mobile, mobileSmall]);
  } catch (error) {
    console.error(`Guardrail error: ${error.message}`);
    process.exitCode = 1;
  } finally {
    if (browser) await browser.close().catch(() => {});
    if (server) server.kill('SIGTERM');
  }
})();
