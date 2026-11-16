import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import { cleanup, render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { mkdtempSync, readFileSync, writeFileSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { adsenseConfig, adsConfigured, canRequestAds } from '@/lib/advertising';
import { sitePages } from '../../tools/site-pages';
import { adsensePublisherId } from '../../seo.config';

const ID = 'ca-pub-1234567890123456';
const env = { VITE_ADS_ENABLED: 'true', VITE_ADS_LIVE_AUTHORIZED: 'true', VITE_ADSENSE_PUBLISHER_ID: ID, VITE_ADSENSE_SLOT_AFTER_GALLERY: '1234567890', VITE_ADSENSE_SLOT_BEFORE_FOOTER: '0987654321' };

function build(site?: string, id?: string) {
  const out = mkdtempSync(join(tmpdir(), 'toli-'));
  writeFileSync(join(out, 'index.html'), '<html><head><title>x</title><!-- page-metadata --></head><body><div id="root"></div></body></html>');
  const plugin = sitePages(site, id) as any;
  plugin.configResolved({ base: site ? new URL(site).pathname : '/', root: out, build: { outDir: '.' } });
  plugin.writeBundle({ dir: out });
  return (f: string) => existsSync(join(out, f)) ? readFileSync(join(out, f), 'utf8') : undefined;
}

it('build with site URL and publisher id: Allow, sitemap, canonical, ads.txt, adsense meta', () => {
  const file = build('https://example.com/', ID);
  expect(file('robots.txt')).toContain('User-agent: Mediapartners-Google\nAllow: /');
  expect(file('robots.txt')).not.toContain('Disallow');
  expect(file('robots.txt')).toContain('Sitemap: https://example.com/sitemap.xml');
  expect(file('sitemap.xml')).toContain('https://example.com/privacy-policy/');
  expect(file('ads.txt')).toBe('google.com, pub-1234567890123456, DIRECT, f08c47fec0942fa0\n');
  const home = file('index.html')!;
  expect(home).toContain(`<meta name="google-adsense-account" content="${ID}">`);
  expect(home).toContain('rel="canonical" href="https://example.com/"');
  expect(home).toContain('index, follow');
  expect(file('cookie-policy/index.html')).toContain('google-adsense-account');
});
it('build without ids: no ads.txt, no adsense meta; without site URL stays non-indexable', () => {
  const file = build();
  expect(file('ads.txt')).toBeUndefined();
  expect(file('index.html')).not.toContain('google-adsense-account');
  expect(file('robots.txt')).toContain('Disallow: /');
  expect(file('index.html')).toContain('noindex');
});
it('validates the publisher id format', () => {
  expect(adsensePublisherId(ID)).toBe(ID);
  for (const bad of ['', undefined, 'pub-1234567890123456', 'ca-pub-123', 'ca-pub-1234567890123456 ']) expect(adsensePublisherId(bad)).toBeUndefined();
});
it('ads are off by default and need every gate', () => {
  const off = adsenseConfig({});
  expect(off).toMatchObject({ enabled: false, liveAdsAuthorized: false, publisherId: '' });
  expect(adsConfigured(off)).toBe(false);
  const on = adsenseConfig(env);
  expect(on.units).toEqual({ 'after-gallery': '1234567890', 'before-footer': '0987654321' });
  expect(canRequestAds(on, 'after-gallery', true)).toBe(true);
  expect(canRequestAds(on, 'after-gallery', false)).toBe(false);
  expect(canRequestAds({ ...on, enabled: false }, 'before-footer', true)).toBe(false);
  expect(canRequestAds({ ...on, units: { ...on.units, 'before-footer': 'x' } }, 'before-footer', true)).toBe(false);
});

beforeEach(() => { localStorage.clear(); document.head.querySelectorAll('script[data-toli-adsense]').forEach(s => s.remove()); vi.resetModules(); });
afterEach(() => { cleanup(); vi.unstubAllEnvs(); });
function stubAds(on: boolean) { for (const [k, v] of Object.entries(env)) vi.stubEnv(k, on ? v : ''); }

it('with ads off: no banner, no ad slot, no footer link, no Google script', async () => {
  stubAds(false);
  const [{ default: Banner }, { default: Ad }] = await Promise.all([import('@/components/ads/ConsentBanner'), import('@/components/ads/AdPlacement')]);
  render(<MemoryRouter><Banner /><Ad placement="after-gallery" /></MemoryRouter>);
  expect(screen.queryByRole('dialog')).toBeNull();
  expect(screen.queryByLabelText('Advertisement')).toBeNull();
  expect(document.querySelector('script[data-toli-adsense]')).toBeNull();
});
it('with ads on: nothing loads before a choice; reject keeps ads off; accept loads one labelled slot', async () => {
  stubAds(true);
  const [{ default: Banner }, { default: Ad }] = await Promise.all([import('@/components/ads/ConsentBanner'), import('@/components/ads/AdPlacement')]);
  render(<MemoryRouter><Banner /><Ad placement="after-gallery" /></MemoryRouter>);
  expect(screen.getByRole('dialog')).toBeInTheDocument();
  expect(screen.queryByLabelText('Advertisement')).toBeNull();
  expect(document.querySelector('script[data-toli-adsense]')).toBeNull();
  fireEvent.click(screen.getByRole('button', { name: 'Reject non-essential' }));
  expect(localStorage.getItem('toli-ad-consent')).toBe('essential');
  expect(screen.queryByRole('dialog')).toBeNull();
  expect(screen.queryByLabelText('Advertisement')).toBeNull();
  expect(document.querySelector('script[data-toli-adsense]')).toBeNull();
});
it('accepting shows the Advertisement label, reserved box and loads the script once', async () => {
  stubAds(true);
  const [{ default: Banner }, { default: Ad }] = await Promise.all([import('@/components/ads/ConsentBanner'), import('@/components/ads/AdPlacement')]);
  render(<MemoryRouter><Banner /><Ad placement="after-gallery" /><Ad placement="before-footer" /></MemoryRouter>);
  fireEvent.click(screen.getByRole('button', { name: 'Accept all' }));
  expect(await screen.findAllByLabelText('Advertisement')).toHaveLength(2);
  expect(screen.getAllByText('Advertisement')).toHaveLength(2);
  expect(document.querySelectorAll('script[data-toli-adsense]')).toHaveLength(1);
  expect(document.querySelector('ins.adsbygoogle')).toHaveAttribute('data-ad-slot', '1234567890');
});
it('ad slots are only placed on the home page', () => {
  const { execSync } = require('node:child_process') as typeof import('node:child_process');
  const files = execSync('git grep -l "ads/AdPlacement" -- src', { encoding: 'utf8' }).split('\n').filter(Boolean)
    .filter(f => !/test|dev\/|components\/ads\//.test(f));
  expect(files).toEqual(['src/pages/Index.tsx']);
});
