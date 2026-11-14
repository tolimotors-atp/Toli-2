import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';
import sharp from 'sharp';

const BASE = 'http://127.0.0.1:8190/Toli-2';
const OUT = 'screenshots';
const CHROME = `${process.env.HOME}/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome`;

const ROUTES = [
  { slug: 'home', path: '/' },
  { slug: 'enquire', path: '/enquire-now/' },
  { slug: 'legal', path: '/privacy-policy/' },
];
const THEMES = ['dark', 'light'];

const srgb = (c) => (c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
const lum = (r, g, b) => 0.2126 * srgb(r / 255) + 0.7152 * srgb(g / 255) + 0.0722 * srgb(b / 255);
const ratio = (l1, l2) => (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);

fs.mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({ executablePath: CHROME });
const report = [];

for (const theme of THEMES) {
  for (const route of ROUTES) {
    const context = await browser.newContext({
      viewport: { width: 1440, height: 900 },
      deviceScaleFactor: 1,
      colorScheme: theme,
    });
    await context.addInitScript((t) => {
      try { window.localStorage.setItem('toli-theme', t); } catch {}
    }, theme);

    const page = await context.newPage();
    await page.goto(BASE + route.path, { waitUntil: 'load', timeout: 60000 });
    await page.waitForTimeout(900);
    const height = await page.evaluate(() => document.body.scrollHeight);

    const failures = [];
    const seen = new Set();
    let checked = 0;

    for (let y = 0; y < height; y += 700) {
      await page.evaluate((v) => window.scrollTo(0, v), y);
      await page.waitForTimeout(320);

      const els = await page.evaluate(() => {
        const out = [];
        const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let node;
        while ((node = walk.nextNode())) {
          const text = node.textContent.replace(/\s+/g, ' ').trim();
          if (text.length < 2) continue;
          const parent = node.parentElement;
          if (!parent) continue;
          if (parent.closest('svg,script,style,noscript,option,.sr-only')) continue;
          const cs = getComputedStyle(parent);
          if (cs.visibility === 'hidden' || cs.display === 'none') continue;
          if (parseFloat(cs.opacity) < 0.3) continue;
          const range = document.createRange();
          range.selectNodeContents(node);
          const rects = [...range.getClientRects()]
            .filter(
              (r) =>
                r.width > 4 && r.height > 4 &&
                r.bottom > 2 && r.top < window.innerHeight - 2 &&
                r.right > 2 && r.left < window.innerWidth - 2,
            )
            .map((r) => ({ x: r.left, y: r.top, w: r.width, h: r.height }));
          if (!rects.length) continue;
          const mid = rects[0];
          const hit = document.elementFromPoint(mid.x + mid.w / 2, mid.y + mid.h / 2);
          if (!hit) continue;
          if (hit !== parent && !parent.contains(hit) && !hit.contains(parent)) continue;
          const chain = [];
          let anc = parent;
          for (let i = 0; i < 4 && anc; i += 1) {
            const cls = typeof anc.className === 'string'
              ? anc.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
            chain.push(anc.tagName.toLowerCase() + (cls ? '.' + cls : ''));
            anc = anc.parentElement;
          }
          out.push({ chain, ident: chain[0], text: text.slice(0, 60), color: cs.color,
            size: parseFloat(cs.fontSize), weight: parseInt(cs.fontWeight, 10) || 400, rects });
        }
        return out;
      });
      if (!els.length) continue;

      const bgBuf = await page.screenshot();
      await page.addStyleTag({ content: '#__audit_hide{}' });
      await page.evaluate(() => {
        const s = document.createElement('style');
        s.id = '__audit_hide';
        s.textContent = '*{color:transparent!important;text-shadow:none!important;}';
        document.head.appendChild(s);
      });
      await page.waitForTimeout(120);
      const plainBuf = await page.screenshot();
      await page.evaluate(() => document.getElementById('__audit_hide')?.remove());
      await page.waitForTimeout(120);

      const { data, info } = await sharp(plainBuf).raw().toBuffer({ resolveWithObject: true });
      const px = (x, yy) => {
        const ix = Math.max(0, Math.min(info.width - 1, Math.round(x)));
        const iy = Math.max(0, Math.min(info.height - 1, Math.round(yy)));
        const o = (iy * info.width + ix) * info.channels;
        return [data[o], data[o + 1], data[o + 2]];
      };
      void bgBuf;

      for (const el of els) {
        const m = el.color.match(/[\d.]+/g);
        if (!m) continue;
        const [r, g, b, a = 1] = m.map(Number);
        const key = `${el.ident}|${el.text}|${el.color}`;
        if (seen.has(key)) continue;
        seen.add(key);
        checked += 1;

        let worst = null;
        for (const rc of el.rects) {
          const stepX = Math.max(2, rc.w / 40);
          const stepY = Math.max(2, rc.h / 10);
          const buckets = new Map();
          for (let py = rc.y + 1; py < rc.y + rc.h; py += stepY) {
            for (let pxx = rc.x + 1; pxx < rc.x + rc.w; pxx += stepX) {
              const [br, bg, bb] = px(pxx, py);
              const k = `${br >> 4},${bg >> 4},${bb >> 4}`;
              const cur = buckets.get(k) || { n: 0, r: 0, g: 0, b: 0 };
              cur.n += 1; cur.r += br; cur.g += bg; cur.b += bb;
              buckets.set(k, cur);
            }
          }
          let best = null;
          for (const cur of buckets.values()) if (!best || cur.n > best.n) best = cur;
          if (!best) continue;
          const bgc = [best.r / best.n, best.g / best.n, best.b / best.n].map(Math.round);
          const bl = lum(bgc[0], bgc[1], bgc[2]);
          const t = lum(r * a + bgc[0] * (1 - a), g * a + bgc[1] * (1 - a), b * a + bgc[2] * (1 - a));
          const c = ratio(t, bl);
          if (!worst || c < worst.c) worst = { c, bg: bgc };
        }
        if (!worst) continue;
        const large = el.size >= 24 || (el.size >= 18.66 && el.weight >= 700);
        const need = large ? 3 : 4.5;
        if (worst.c < need) {
          failures.push({ chain: el.chain, ident: el.ident, text: el.text, color: el.color,
            size: el.size, need, ratio: Math.round(worst.c * 100) / 100, bg: worst.bg, atY: y });
        }
      }
    }

    failures.sort((x, z) => x.ratio - z.ratio);
    report.push({ theme, route: route.path, checked, failures });
    console.log(`\n=== ${theme} ${route.path} — ${checked} text runs, ${failures.length} below AA ===`);
    for (const f of failures.slice(0, 14)) {
      console.log(`  ${f.ratio.toFixed(2)} ${f.size}px ${f.ident} :: ${f.chain.slice(1, 4).join(' < ')} @${f.atY} — "${f.text}"`);
    }
    await context.close();
  }
}

await browser.close();
fs.writeFileSync(path.join(OUT, 'contrast-report.json'), JSON.stringify(report, null, 2));
console.log('\nwrote screenshots/contrast-report.json');
