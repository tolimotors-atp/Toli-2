# Light Hero lighting and contact pill

## Lighting

The daylight WebP already contains illuminated fixtures, ceiling structure and natural window light. The large white bloom came from the first radial gradient in `src/premium-light.css`, painted over the photo in `.hero-workshop-atmosphere::before` on desktop. On smaller screens, `.entry-composition::before` used the separate `--hero-daylight-copy` radial gradient.

The desktop layer now spans a 31% by 136px ellipse with 70% peak opacity, down from 39% by 176px and 96%. It sits 23px higher to cover the subtitle and heading with less wash on the wall. The tablet and mobile layers now peak at 67% and 64% respectively, down from 91% and 96%, with tighter falloff. Fully removing the layer during visual QA put dark roof beams directly behind parts of the headline and caption. The smaller, more transparent layer gives that text separation while keeping the beams visible. The daylight photo, crop, floor fade and localized index-label gradient use their existing settings.

## Contact pill

The existing grid uses a 30–38px icon column. The red phone icon spans and centers across both number rows. The numbers keep the same weight, text and destinations, `tel:+919908303888` and `tel:+918074946335`. At 1366px, the pill is about 159px wide and 65px high, with the icon growing from 12px to 36px. At 390px, the pill is 127px wide and 62px high, with the icon growing from 10px to 30px. The right edge and height match their previous positions. Light uses pearl and metallic-grey tokens with graphite text. Dark uses the existing graphite treatment with silver-white text.

## Evidence

- Light desktop [before](hero-light-lighting-evidence/hero-light-before-lighting-fix.jpg) and [after](hero-light-lighting-evidence/hero-light-after-lighting-fix.jpg)
- Dark desktop [before](hero-light-lighting-evidence/hero-dark-before.jpg) and [after](hero-light-lighting-evidence/hero-dark-regression.jpg)
- Contact pill [light desktop](hero-light-lighting-evidence/contact-pill-light-desktop.jpg), [dark desktop](hero-light-lighting-evidence/contact-pill-dark-desktop.jpg) and [light mobile](hero-light-lighting-evidence/contact-pill-mobile.jpg)
- Light mobile [before](hero-light-lighting-evidence/hero-light-mobile-before.jpg) and [after](hero-light-lighting-evidence/hero-light-mobile-after.jpg)

- [Desktop comparison at 1366px and 1920px](hero-light-lighting-evidence/desktop-comparison.jpg) and [light responsive contact sheet](hero-light-lighting-evidence/responsive-light.jpg)

## Validation

- Production build, TypeScript and ESLint passed.
- 85 tests passed across eight files covering the Hero, site theme, navigation and TOLI AI. Vitest emitted a React `act(...)` warning in the existing theme test.
- Chromium production preview covered 320×568, 360×800, 390×844, 412×915, 768×1024, 1366×768, 1920×1080, 844×390 landscape and 683×384 in both themes. Measurements matched the baseline for the navbar, location pill, central logo, subtitle, headline, caption and vehicle image. The phone icon was centered across both rows. The viewport checks found no horizontal overflow, clipping of the number rows, or contact-pill overlap with those elements.
- The 1366×768 dark-theme PNG captures had zero differing pixels outside the masked contact-pill and shadow region.
- At 1366×768 and 390×844 in both themes, repeated theme toggling and the TOLI AI open, input, send, reply and close flow passed. Production checks found no console warnings, uncaught exceptions or failed asset responses.
- The 683×384 viewport approximates the CSS reflow at 200% zoom on a 1366×768 viewport. Browser-native zoom, physical devices and OS dialing were outside this verification.

## Files

- `src/premium-light.css`
- `src/components/journey/hero-corner-visibility.css`
- This report and its screenshot directory

The work was saved in the static website checkout. No deployment or push was performed.
