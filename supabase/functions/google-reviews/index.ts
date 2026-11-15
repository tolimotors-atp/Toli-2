// Live Google reviews for the website. Keeps the Places API key on the server.
// Secrets: GOOGLE_PLACES_API_KEY (Places API (New) enabled) and GOOGLE_PLACE_ID.
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};
const TTL_MS = 60 * 60 * 1000; // one upstream call per hour per instance
let cache: { at: number; body: string } | null = null;

const reply = (body: string, status = 200, extra: Record<string, string> = {}) =>
  new Response(body, { status, headers: { ...corsHeaders, "content-type": "application/json", ...extra } });

serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { headers: corsHeaders });
  if (req.method !== "GET") return reply(JSON.stringify({ error: "Method not allowed" }), 405);

  const key = Deno.env.get("GOOGLE_PLACES_API_KEY");
  const placeId = Deno.env.get("GOOGLE_PLACE_ID");
  if (!key || !placeId) return reply(JSON.stringify({ error: "Not configured" }), 503);

  if (cache && Date.now() - cache.at < TTL_MS) return reply(cache.body, 200, { "cache-control": "public, max-age=900" });

  const upstream = await fetch(`https://places.googleapis.com/v1/places/${encodeURIComponent(placeId)}`, {
    headers: {
      "X-Goog-Api-Key": key,
      "X-Goog-FieldMask": "rating,userRatingCount,reviews.rating,reviews.text,reviews.relativePublishTimeDescription,reviews.authorAttribution.displayName",
    },
  });
  if (!upstream.ok) return reply(JSON.stringify({ error: "Google request failed" }), 502);

  const place = await upstream.json();
  const body = JSON.stringify({
    rating: place.rating ?? null,
    count: place.userRatingCount ?? null,
    fetchedAt: new Date().toISOString(),
    reviews: (place.reviews ?? [])
      .map((r: any) => ({
        author: r.authorAttribution?.displayName ?? "Google user",
        stars: Math.max(1, Math.min(5, Math.round(r.rating ?? 5))),
        excerpt: String(r.text?.text ?? "").slice(0, 160),
        when: r.relativePublishTimeDescription ?? "",
      }))
      .filter((r: { excerpt: string }) => r.excerpt),
  });
  cache = { at: Date.now(), body };
  return reply(body, 200, { "cache-control": "public, max-age=900" });
});
