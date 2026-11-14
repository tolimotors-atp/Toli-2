# Google Reviews card rail

The original visibility issue was reproduced when a delayed footer chunk held up a shared React Suspense boundary. The previous fix moved Customer Stories outside that boundary. This update retains the independent homepage mount directly after Gallery and before Booking, the Gallery shortcut, and the visible empty-review fallback.

The [verified TOLI Motors listing](https://maps.app.goo.gl/5ryaFnYVhQeCcHWGA) showed **4.1 out of 5 from 83 reviews** on 13 November 2026. The rail includes seven short excerpts checked against the Google Reviews tab, attributed to Ravalchuru Mahaboob Basha, mandli raja, Naveen Teja, Penumala Raja sekhar, Kumar Kumar Kumar, Jagadeeswara Reddy Pothireddy and Ravi Varma. The card ratings match Google. The website labels the aggregate as a dated snapshot and links to the full listing.

A width-capped CSS grid shows five complete cards from 1024px, three at tablet widths from 768px, and two on phones down to 320px. A native horizontal scroller supports touch, trackpad-style horizontal input and keyboard scrolling. The arrow buttons move one card at a time. Proximity snapping and a thin scrollbar preserve manual control. The list and controls have accessible names and visible focus. Smooth scrolling follows the reduced-motion preference. The rail adds no third-party widget, scripts, avatars or dependencies.

## Verification

- Production build, TypeScript and lint passed. 71 relevant tests passed across nine files, including empty-review fallbacks.
- Chromium passed 20 light/dark combinations at 320×568, 360×800, 390×844, 412×915, 768×1024, 1024×768, 1366×768, 1440×900, 1920×1080 and 844×390 landscape. Verified full card counts, touch swipes on phone sizes, horizontal wheel input on wider sizes, arrow buttons, focused keyboard scrolling, and no page overflow or production console errors.
- Gallery retained six featured photos and all 16 in See More. Booking and TOLI AI reply and fallback passed on desktop and mobile emulation. Loaded Hero screenshots matched the previous build pixel for pixel in both themes. Existing MU-X display plates were verified.
- [Five cards in dark mode](google-reviews-card-rail/google-reviews-5-cards-desktop-dark.jpg), [five cards in light mode](google-reviews-card-rail/google-reviews-5-cards-desktop-light.jpg), [desktop scrolled](google-reviews-card-rail/google-reviews-horizontal-scroll-desktop.jpg)
- [Two cards in dark mode](google-reviews-card-rail/google-reviews-2-cards-mobile-dark.jpg), [two cards in light mode](google-reviews-card-rail/google-reviews-2-cards-mobile-light.jpg), [mobile scrolled](google-reviews-card-rail/google-reviews-mobile-scrolled.jpg), [Google link](google-reviews-card-rail/google-reviews-google-link.jpg)

Changes are limited to the Testimonials component, its stylesheet, focused tests, the corresponding regression checksum and this evidence. The Google snapshot requires manual updates. Physical touch and trackpad hardware, assistive technology and browsers other than Chromium were outside this run. The build remains local.
