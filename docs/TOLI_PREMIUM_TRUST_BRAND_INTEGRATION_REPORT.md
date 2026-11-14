# TOLI Motors trust and vehicle branding

## Audit and review source

The existing homepage already placed Customer Stories between the six-photo Gallery and Booking, shared a direct Google link with the footer, and used the official logo on a separate MU-X plate image layer. The main gaps were three equal desktop quotes, controls available only on phones, and two image layers in each MU-X placement. The Hero, navigation, phone and location pills, workshop imagery, and enquiry and assistant flows required preservation.

Reopened the [TOLI MOTORS Google Maps Reviews tab](https://www.google.com/maps/place/TOLI+MOTORS/@14.6737594,77.5817845,17z/data=!4m8!3m7!1s0x3bb14bf8997b499f:0x8040c48849f89b50!8m2!3d14.6737594!4d77.5817845!9m1!1b1!16s%2Fg%2F11vb2zttzx). The business identity was previously matched to the site's workshop address and phone, and the direct URL again opened the selected Reviews tab. On 13 November 2026, Google displayed **4.1 out of 5 from 83 reviews**. The site labels those values as a dated snapshot.

The three verified excerpts are from Ravalchuru Mahaboob Basha (5 stars), mandli raja (4 stars), and Naveen Teja (5 stars). They were checked against the public review text and remain attributed to Google. The section shows a single quote with a limited reading width and the rating summary alongside the heading on desktop. Phones stack the summary, quote, navigation and source link. Controls have accessible labels, visible focus and 44px targets. A polite live region announces the selected quote and the 160ms fade respects reduced motion. There is no autoplay, external review widget, dependency, or API request.

## Vehicle integration

The approved master is the satin-silver display plate using the official black/red `src/assets/big-transparent-lossless.webp` mark in its existing proportions. The plate follows the MU-X stock frame and contains no registration number. The approved perspective-aligned plate layer was composited into two derived images. Each MU-X now uses one responsive image in Vehicle Components, Process and Booking. The source photos, existing master layer, and authoritative MU-X reference directory were preserved.

| Derived WebP | Dimensions | Size | Previous car plus plate |
| --- | --- | --- | --- |
| `isuzu-mux-red-toli-front-3q-640.webp` | 640×384 | 53,770 bytes | 57,092 bytes |
| `isuzu-mux-red-toli-front-3q.webp` | 1100×660 | 116,244 bytes | 116,772 bytes |

Both outputs decoded, and the alpha channels matched the corresponding original pixel for pixel. The baked WebPs use lossy RGB encoding, so small pixel differences outside the plate area can occur. The body, silhouette, paint, wheels and lights are visually consistent with the source. The three approved Hero cars have no clearly defined plate faces. Their before-and-after Hero screenshots matched pixel for pixel at 1366×768 in both themes.

## Validation and evidence

- Production build, TypeScript and ESLint passed. **87 relevant tests passed across 11 files**.
- Chromium passed **18 viewport/theme combinations**. The matrix covered 320×568, 360×800, 390×844, 412×915, 768×1024, 1024×768, 1366×768, 1920×1080 and 844×390 landscape in light and dark. It verified one visible review, keyboard navigation, source-link wiring, theme switching, responsive MU-X loading, no page overflow and no observed console errors, warnings or failed responses.
- Gallery remains six featured photos followed by See More with 16 photos. The prior lazy-loading logic and Gallery source stayed intact. Booking opened and closed, and TOLI AI handled Enter, Send, a service reply, and the unsupported-question fallback on desktop and mobile emulation.
- Customer Stories [dark desktop](premium-trust-brand/customer-stories-dark-desktop.jpg), [light desktop](premium-trust-brand/customer-stories-light-desktop.jpg), and [390px phone](premium-trust-brand/customer-stories-mobile-390.jpg).
- Hero [dark](premium-trust-brand/hero-toli-plates-dark.jpg) and [light](premium-trust-brand/hero-toli-plates-light.jpg). MU-X [desktop](premium-trust-brand/mux-toli-plate-desktop.jpg) and [comparison](premium-trust-brand/mux-before-after.jpg).
- [Six featured photos](premium-trust-brand/gallery-six-before-testimonials.jpg) and [Gallery-to-reviews flow](premium-trust-brand/gallery-to-testimonials-flow.jpg).

Source changes are in `src/components/Testimonials.tsx`, `src/components/testimonials.css`, `src/components/journey/MuxPhotography.tsx` and `src/components/journey/mux-photography.css`, alongside the two derived images, affected tests and the protected source checksum for Testimonials. The first automated write review was rejected while the small candidate appeared empty. Both assets were checked for size, dimensions and successful decoding before the validated files were installed.

The Google rating is a manually refreshed snapshot. Physical devices and browsers other than Chromium were outside this run. Changes were saved locally. No push or deployment was performed.
