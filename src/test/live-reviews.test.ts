import { afterEach, expect, it, vi } from 'vitest';
import { fetchLiveReviews, liveReviewsEndpoint } from '@/lib/google-reviews';

afterEach(() => { vi.unstubAllEnvs(); vi.unstubAllGlobals(); });

it('chooses the endpoint from env and is off when nothing is configured', () => {
  expect(liveReviewsEndpoint({})).toBeNull();
  expect(liveReviewsEndpoint({ VITE_SUPABASE_URL: 'https://x.supabase.co', VITE_SUPABASE_PUBLISHABLE_KEY: 'k' })).toEqual({ url: 'https://x.supabase.co/functions/v1/google-reviews', key: 'k' });
  expect(liveReviewsEndpoint({ VITE_GOOGLE_REVIEWS_URL: 'https://example.test/r' })?.url).toBe('https://example.test/r');
});

it('returns clean reviews, and null on failures or empty answers', async () => {
  vi.stubEnv('VITE_GOOGLE_REVIEWS_URL', 'https://example.test/r');
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true, json: async () => ({ rating: 4.2, count: 90, fetchedAt: '2026-11-16T00:00:00Z', reviews: [{ author: 'A', stars: 9, excerpt: 'Great' }, { author: 'B', stars: 4, excerpt: '' }] }) }));
  expect(await fetchLiveReviews()).toEqual({ rating: 4.2, count: 90, fetchedAt: '2026-11-16T00:00:00Z', reviews: [{ author: 'A', stars: 5, excerpt: 'Great' }] });
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false }));
  expect(await fetchLiveReviews()).toBeNull();
  vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('offline')));
  expect(await fetchLiveReviews()).toBeNull();
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true, json: async () => ({ reviews: [] }) }));
  expect(await fetchLiveReviews()).toBeNull();
});
