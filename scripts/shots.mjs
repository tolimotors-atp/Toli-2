import fs from 'node:fs';
import { chromium } from 'playwright';
import sharp from 'sharp';

const CHROME = `${process.env.HOME}/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome`;
const BASE = 'http://127.0.0.1:8190/Toli-2';
const OUT = 'screenshots';
fs.mkdirSync(OUT, { recursive: true });

const pages = [
  { slug: 'home', path: '/' },
  { slug: 'enquire', path: '/enquire-now/' },
  { slug: 'legal', path: '/privacy-policy/' },
];

const browser = await chromium.launch({ executablePath: CHROME });

for (const theme of ['dark', 'light']) {
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 950 }, colorScheme: theme });
  await ctx.addInitScript((t) => { try { localStorage.setItem('toli-theme', t); } catch {} }, theme);

  for (const p of pages) {
    const page = await ctx.newPage();
    await page.goto(BASE + p.path, { waitUntil: 'load', timeout: 60000 });
    await page.waitForTimeout(900);
    const total = await page.evaluate(() => document.body.scrollHeight);

    // Walk once so mounted content settles, then capture three viewports.
    for (let y = 0; y < total; y += 800) {
      await page.evaluate((v) => scrollTo(0, v), y);
      await page.waitForTimeout(110);
    }
    const stops = [0, Math.round((total - 950) * 0.5), Math.max(0, total - 950)];
    const parts = [];
    for (const y of stops) {
      await page.evaluate((v) => scrollTo(0, v), y);
      await page.waitForTimeout(600);
      const buf = await page.screenshot();
      parts.push(await sharp(buf).resize({ width: 1000 }).toBuffer());
    }
    const metas = await Promise.all(parts.map((b) => sharp(b).metadata()));
    const h = metas.reduce((sum, m) => sum + m.height, 0);
    await sharp({ create: { width: 1000, height: h, channels: 3, background: theme === 'dark' ? '#101114' : '#f5f4f2' } })
      .composite(parts.map((input, i) => ({ input, top: metas.slice(0, i).reduce((s, m) => s + m.height, 0), left: 0 })))
      .jpeg({ quality: 78, mozjpeg: true })
      .toFile(`${OUT}/${p.slug}-${theme}.jpg`);
    console.log(`${OUT}/${p.slug}-${theme}.jpg`, Math.round(fs.statSync(`${OUT}/${p.slug}-${theme}.jpg`).size / 1024) + 'KB');
    await page.close();
  }
  await ctx.close();
}
await browser.close();
