import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import type { Plugin, ResolvedConfig } from 'vite';
import { adsenseMeta, adsTxt, escapeHtml, pageHref, pageInfo, pageMetadata, pagePath, pages, type PagePath } from '../seo.config';

export function sitePages(site?: string, adsenseId?: string): Plugin {
  let config: ResolvedConfig;

  function render(html: string, path?: PagePath) {
    const { title, heading, description } = pageInfo(path);
    const links = [
      ['Home', config.base], ['Workshop services', config.base + '#services'],
      ['Request service', pageHref(config.base, '/enquire-now')], ['Contact', config.base + '#contact'],
    ];
    const trail = path === '/' ? '' : `<nav aria-label="Breadcrumb"><a href="${config.base}">Home</a> / <span aria-current="page">${escapeHtml(pageInfo(path).label)}</span></nav>`;
    const body = `<main class="toli-content-page mx-auto max-w-3xl px-6 py-12">
      ${trail}
      <h1 class="my-5 text-4xl font-bold">${escapeHtml(heading)}</h1>
      <p class="mb-5">${escapeHtml(description)}</p>
      <nav aria-label="Workshop links" class="flex flex-wrap gap-4 underline">${links.map(([label, href]) => `<a href="${href}">${label}</a>`).join('')}</nav>
    </main>`;
    return html.replace(/<title>[^<]*<\/title>/, `<title>${escapeHtml(title)}</title>`)
      .replace('<!-- page-metadata -->', () => [pageMetadata(path, site), adsenseMeta(adsenseId)].filter(Boolean).join('\n'))
      .replace('<div id="root"></div>', () => `<div id="root">${body}</div>`);
  }

  return {
    name: 'toli-site-pages',
    configResolved(resolved) {
      config = resolved;
      if (site && config.base !== new URL(site).pathname) throw new Error('VITE_SITE_URL and the Vite base must use the same path.');
    },
    configurePreviewServer(server) {
      server.middlewares.use((req, res, next) => {
        const url = new URL(req.url ?? '/', 'http://localhost');
        if ((req.method !== 'GET' && req.method !== 'HEAD') || !req.headers.accept?.includes('text/html') ||
            !url.pathname.startsWith(config.base) || url.pathname === config.base + '404.html') return next();
        const localPath = '/' + url.pathname.slice(config.base.length);
        const route = pagePath(localPath.replace(/\/index\.html$/, '/'));
        if (route) {
          const href = pageHref(config.base, route);
          if (url.pathname === href) return next();
          res.statusCode = 308;
          res.setHeader('Location', href + url.search);
          res.end();
          return;
        }
        res.statusCode = 404;
        res.setHeader('Content-Type', 'text/html; charset=utf-8');
        res.end(req.method === 'HEAD' ? undefined : readFileSync(join(config.root, config.build.outDir, '404.html')));
      });
    },
    writeBundle(options) {
      const out = options.dir ?? join(config.root, config.build.outDir);
      const template = readFileSync(join(out, 'index.html'), 'utf8');
      const routes = Object.keys(pages) as PagePath[];
      for (const route of routes) {
        const dir = join(out, route.slice(1));
        mkdirSync(dir, { recursive: true });
        writeFileSync(join(dir, 'index.html'), render(template, route));
      }
      writeFileSync(join(out, '404.html'), render(template));
      const sitemap = site && `Sitemap: ${site}sitemap.xml\n`;
      writeFileSync(join(out, 'robots.txt'), site ? `User-agent: Mediapartners-Google\nAllow: /\n\nUser-agent: *\nAllow: /\n\n${sitemap}` : 'User-agent: *\nDisallow: /\n');
      if (adsenseId) writeFileSync(join(out, 'ads.txt'), adsTxt(adsenseId));
      if (site) {
        const urls = routes.map(route => `  <url><loc>${escapeHtml(pageHref(site, route))}</loc></url>`);
        writeFileSync(join(out, 'sitemap.xml'), ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">', ...urls, '</urlset>', ''].join('\n'));
      }
      const links = routes.map(route => `- [${pages[route].label}](${pageHref(site ?? config.base, route)}): ${pages[route].description}`);
      const summary = ['# Toli Motors', '', '> Multi-brand car workshop in Anantapur, Andhra Pradesh, India.', '',
        '6-2-806, Ram Nagar, Kovur Nagar, opposite DMart, Anantapur 515004. Phone +91-8074946335. Email tolimotorsatp@gmail.com.',
        '', '## Pages', '', ...links, ''].join('\n');
      for (const name of ['llms.txt', 'lms.txt']) writeFileSync(join(out, name), summary);
    },
  };
}
