# Google testimonials and TOLI display plates

## Google reviews

The previous testimonial section linked to a Google Maps search from the Trust accordion and footer. It supplied no customer quotes, ratings, review count or live review integration. The site’s workshop address and public telephone number match the [TOLI MOTORS Google Maps review listing](https://www.google.com/maps/place/TOLI+MOTORS/@14.6737594,77.5817845,17z/data=!4m8!3m7!1s0x3bb14bf8997b499f:0x8040c48849f89b50!8m2!3d14.6737594!4d77.5817845!9m1!1b1!16s%2Fg%2F11vb2zttzx). Google Maps displayed **4.1 out of 5 from 83 reviews** when checked on 13 November 2026. The site labels this as a dated snapshot. The external link leads to the source for the current count and full reviews. The footer now shares that direct link.

The three short Google review excerpts are attributed to Ravalchuru Mahaboob Basha (5 stars), mandli raja (4 stars) and Naveen Teja (5 stars). They cover full-body painting, service feedback and staff responsiveness. The site uses the public display names and the ratings Google showed for each review. Customer photos and review dates are omitted.

Customer Stories sits between Gallery and Booking. Three editorial columns display on tablet and desktop. Phones display one review with manual Previous and Next controls, a live position label and no autoplay. The section uses the existing light and dark theme roles. It does not load Google scripts or make review API requests.

## Vehicle display plates

The active red Isuzu MU-X has a visible front display plate. A transparent WebP layer places the official `src/assets/big-transparent-lossless.webp` logo on a satin-silver face. Its four corners match the original plate perspective and the stock frame remains visible. The layer is decorative for assistive technology and has the same dimensions and object fit as the original 1100×660 canvas. Both existing responsive car images remain in use. Vehicle Components, Process and Booking share the same lazy-loaded 5,540-byte layer.

The three-car Hero artwork has no clear number-plate faces. Branding there would require adding new mounts over the grilles or bumper surfaces. Its source files and rendered composition were preserved. At 1366×768, before and after Hero captures matched pixel for pixel in both themes. In the corresponding light MU-X comparison, the difference was confined to the 57×32px plate region, including antialiased edges. The authoritative MU-X reference folder and original production car images were preserved. Documentary gallery images were outside the display-plate edit.

## Validation

- Production build, TypeScript, and ESLint passed.
- 35 relevant tests passed across nine files. Vitest emitted existing React Router and React testing warnings.
- Chromium passed 14 cases across 320×568, 360×800, 390×844, 412×915, 768×1024, 1366×768, and 1920×1080 in both themes. Verified review visibility and controls, exact link target, theme switching, plate alignment across three placements, no horizontal overflow, and the six-photo Gallery with all 16 images in See More. No production console warnings, page errors or failed responses were observed in these flows.
- [Desktop dark](google-testimonials-toli-plates/google-testimonials-desktop-dark.jpg), [desktop light](google-testimonials-toli-plates/google-testimonials-desktop-light.jpg), [mobile](google-testimonials-toli-plates/google-testimonials-mobile.jpg), [MU-X plate](google-testimonials-toli-plates/mux-toli-number-plate.jpg), [MU-X before and after](google-testimonials-toli-plates/mux-plate-comparison.jpg), and [Hero before and after](google-testimonials-toli-plates/hero-comparison.jpg).

Changes were made locally. Physical devices and browsers other than Chromium were outside this run. The snapshot remains dated until it is refreshed.
