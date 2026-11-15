import { useEffect, useRef, useState } from 'react';
import { ChevronLeft, ChevronRight, ExternalLink, Star } from 'lucide-react';
import { GOOGLE_REVIEWS_URL, fetchLiveReviews, type LiveReviews } from '@/lib/google-reviews';
import './testimonials.css';

const verifiedStories = [
  { author: 'Ravalchuru Mahaboob Basha', stars: 5, excerpt: 'I came for fullbody painting' },
  { author: 'mandli raja', stars: 4, excerpt: 'Thank you Toli for your service' },
  { author: 'Naveen Teja', stars: 5, excerpt: 'supportive staff who respond promptly' },
  { author: 'Penumala Raja sekhar', stars: 5, excerpt: 'They did awesome work' },
  { author: 'Kumar Kumar Kumar', stars: 5, excerpt: 'They did excellent service' },
  { author: 'Jagadeeswara Reddy Pothireddy', stars: 5, excerpt: 'I am very happy abt there response' },
  { author: 'Ravi Varma', stars: 5, excerpt: 'I gave my vehicle to regular service' },
];

export default function Testimonials({
  stories: storiesProp,
  reviewUrl = GOOGLE_REVIEWS_URL,
}: { stories?: typeof verifiedStories; reviewUrl?: string | null } = {}) {
  const rail = useRef<HTMLUListElement>(null);
  const [live, setLive] = useState<LiveReviews | null>(null);
  // Live Google data replaces the saved snapshot when the review endpoint is configured and answers.
  useEffect(() => {
    if (storiesProp) return;
    const controller = new AbortController();
    fetchLiveReviews(controller.signal).then(setLive);
    return () => controller.abort();
  }, [storiesProp]);
  const stories = live?.reviews ?? storiesProp ?? verifiedStories;
  const scrollReviews = (direction: number) => {
    const list = rail.current;
    if (!list) return;
    const [first, second] = Array.from(list.children);
    if (!first || !second) return;
    const stride = second.getBoundingClientRect().left - first.getBoundingClientRect().left;
    list.scrollBy({ left: direction * stride, behavior: 'auto' });
  };

  return (
    <section id="customer-stories" className="customer-stories" aria-labelledby="reviews-heading">
      <header className="customer-stories-heading">
        <h2 id="reviews-heading">Customer stories</h2>
        <div className="customer-rating-summary">
          <h3>Google Reviews</h3>
          {stories.length > 0 && <>
            {live ? <>
              {live.rating !== null && <p className="customer-rating"><Star size={16} aria-hidden="true" /> <strong>{live.rating.toFixed(1)} out of 5</strong>{live.count !== null && <> · {live.count} reviews</>}</p>}
              <p className="customer-rating-date">Live from Google{live.fetchedAt ? `, updated ${new Date(live.fetchedAt).toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' })}` : ''}</p>
            </> : <>
              <p className="customer-rating"><Star size={16} aria-hidden="true" /> <strong>4.1 out of 5</strong> · 83 reviews</p>
              <p className="customer-rating-date">Google Maps snapshot, 13 November 2026</p>
            </>}
          </>}
        </div>
      </header>

      {stories.length > 0 ? (
        <>
          <ul id="google-review-rail" ref={rail} className="customer-story-list" aria-label="Google review excerpts" tabIndex={0}>
            {stories.map(({ author, stars, excerpt }, index) => (
              <li className="customer-story" key={`${author}-${index}`}>
                <span className="customer-stars" aria-label={`${stars} out of 5 stars`} role="img">
                  {Array.from({ length: 5 }, (_, position) => <Star key={position} size={14} fill={position < stars ? 'currentColor' : 'none'} aria-hidden="true" />)}
                </span>
                <blockquote>“{excerpt}”</blockquote>
                <p className="customer-story-author">{author}<span>Google review excerpt</span></p>
              </li>
            ))}
          </ul>
          {stories.length > 1 && (
            <div className="customer-story-controls">
              <button type="button" aria-label="Scroll reviews left" aria-controls="google-review-rail" onClick={() => scrollReviews(-1)}><ChevronLeft size={20} aria-hidden="true" /></button>
              <button type="button" aria-label="Scroll reviews right" aria-controls="google-review-rail" onClick={() => scrollReviews(1)}><ChevronRight size={20} aria-hidden="true" /></button>
            </div>
          )}
        </>
      ) : (
        <p className="customer-story-list customer-stories-fallback">
          {reviewUrl ? 'Read customer reviews directly on Google.' : 'Google review information is being connected.'}
        </p>
      )}
      {reviewUrl && <a className="customer-reviews-link" href={reviewUrl} target="_blank" rel="noopener noreferrer">
        View reviews on Google <ExternalLink size={16} aria-hidden="true" />
      </a>}
    </section>
  );
}
