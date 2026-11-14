# Customer Stories visibility correction

## Root cause and fix

The previous production build mounted Customer Stories inside the same React Suspense boundary as booking, contact and the footer. Delaying the footer chunk in Chromium reproduced a visible Gallery followed by a loading placeholder with no Customer Stories. The reviews appeared after the footer resolved. The exact loading state in the originally reported browser session is unknown.

Customer Stories now imports with the homepage and renders directly after Gallery, independently of that lower-page loading boundary. The same delayed-footer browser check confirmed the section is visible while the footer is still pending. Gallery has a Customer Stories shortcut beside See More, and the homepage supports the `#customer-stories` deep link. Booking follows the section.

## Source and fallback

The [supplied Google Maps link](https://maps.app.goo.gl/5ryaFnYVhQeCcHWGA) opened the TOLI MOTORS profile at 6-2-806, Ram Nagar, Kovur Nagar, Anantapur. The listing's phone ending 46335 and website matched the project. The public profile displayed **4.1 out of 5 from 83 reviews** on 13 November 2026. The homepage and footer link to the supplied URL.

The featured excerpts are attributed to Ravalchuru Mahaboob Basha (5 stars), mandli raja (4 stars) and Naveen Teja (5 stars). One quote is visible at a time in both themes. Previous and Next are keyboard-accessible and the selected quote is announced in a live region.

An empty review list still renders both headings and a link to the verified profile, with no stars, rating, count or quotes. If the profile link is also unavailable, the section displays a neutral connection message. Both fallback cases are covered by tests.

## Validation

- Production build, TypeScript, lint and 71 relevant tests across nine files passed. Vitest emitted existing test-environment warnings.
- Production Chromium passed 14 viewport and theme combinations at 320×568, 360×800, 390×844, 412×915, 768×1024, 1366×768 and 1920×1080. The production console was clean.
- Verified the shortcut scroll, keyboard review controls, original phone and desktop layouts, six featured Gallery photos and 16 photos in See More, and all three branded MU-X presentations. The booking dialog and TOLI AI typing, Enter, Send, reply, fallback, close and overlay layering passed on desktop and mobile emulation.
- Desktop Hero before-and-after screenshots matched pixel for pixel in light and dark. The vehicle assets, navbar and phone pill received no edits.

## Screenshots

- [Desktop dark](google-testimonials-fix/google-testimonials-desktop-dark.jpg)
- [Desktop light](google-testimonials-fix/google-testimonials-desktop-light.jpg)
- [390px phone](google-testimonials-fix/google-testimonials-mobile-390.jpg)
- [Gallery to Customer Stories](google-testimonials-fix/gallery-to-google-testimonials.jpg)
- [Customer Stories to booking](google-testimonials-fix/google-testimonials-to-booking.jpg)

## Files and limits

Changed `src/pages/Index.tsx`, `src/components/Testimonials.tsx`, `src/components/testimonials.css`, `src/components/Gallery.tsx`, `src/components/gallery-editorial.css`, `src/lib/google-reviews.ts` and `src/lib/section-links.ts`, along with the affected review and homepage tests and source checksums.

The Google rating remains a dated snapshot. Physical devices and browsers other than Chromium were outside this run. The production build is available through the local preview. No remote deployment was performed.
