export const GOOGLE_REVIEWS_URL = 'https://maps.app.goo.gl/5ryaFnYVhQeCcHWGA';

export type LiveReviews = {
  rating: number | null;
  count: number | null;
  fetchedAt: string;
  reviews: { author: string; stars: number; excerpt: string }[];
};

/** Where the live reviews come from: an explicit URL, else the Supabase function, else none (static snapshot is used). */
export function liveReviewsEndpoint(env: Record<string, string | undefined> = import.meta.env) {
  if (env.VITE_GOOGLE_REVIEWS_URL) return { url: env.VITE_GOOGLE_REVIEWS_URL, key: undefined };
  if (env.VITE_SUPABASE_URL) return { url: `${env.VITE_SUPABASE_URL}/functions/v1/google-reviews`, key: env.VITE_SUPABASE_PUBLISHABLE_KEY };
  return null;
}

/** Null on any failure or odd shape, so the page keeps showing the snapshot. */
export async function fetchLiveReviews(signal?: AbortSignal): Promise<LiveReviews | null> {
  const endpoint = liveReviewsEndpoint();
  if (!endpoint) return null;
  try {
    const response = await fetch(endpoint.url, { signal, headers: endpoint.key ? { apikey: endpoint.key, Authorization: `Bearer ${endpoint.key}` } : undefined });
    if (!response.ok) return null;
    const data = await response.json();
    if (!Array.isArray(data?.reviews) || data.reviews.length === 0) return null;
    return {
      rating: typeof data.rating === 'number' ? data.rating : null,
      count: typeof data.count === 'number' ? data.count : null,
      fetchedAt: String(data.fetchedAt ?? ''),
      reviews: data.reviews.map((r: any) => ({ author: String(r.author ?? 'Google user'), stars: Math.max(1, Math.min(5, Number(r.stars) || 5)), excerpt: String(r.excerpt ?? '') })).filter((r: { excerpt: string }) => r.excerpt),
    };
  } catch {
    return null;
  }
}
