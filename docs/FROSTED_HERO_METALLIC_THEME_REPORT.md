# Frosted Hero and metallic theme — 5 November 2026

Local static project only. No deployment performed.

## Saved implementation
- `src/components/journey/hero-corner-visibility.css`: translucent graphite/grey with a restrained red tint, opaque white text, silver border and upper reflection. Backdrop blur 8px desktop / 5px up to 900px. Near-opaque fallback precedes the feature query. Existing pill positions, padding, dimensions and phone links retained; no whole-element opacity, animated blur or extra large filters.
- `src/components/journey/navbar-brand.css`: graphite/metallic grey across roughly 70% of the gradient, restrained red trailing illumination. Light mode uses silver/grey. Logo artwork/pill, car, controls, geometry and animation untouched.
- `src/workshop-surfaces.css`: directional red/grey metallic chapter backgrounds, glossy dark panels, bright-red active services and request buttons, sparse champagne labels/indexes/hairlines. Pearl/silver light mode uses dark ink and a darker champagne label for contrast. Assistant and enquiry surfaces included. Ratios are visual targets, not measured pixel coverage; gold is deliberately sparse.
- `src/assets/hero/workshop-depth.svg` and `workshop-depth-dark.svg`: removed only the two SVG paths forming the foreground lift posts and arms. Other SVG elements retained.
- `src/components/journey/hero-caption.css`: only the two desktop/tablet photographic background URLs changed to new grounded variants.
- New `src/assets/hero/garage-grounded-wide-1600.webp` and `garage-grounded-wide-960.webp`: image-editing skill removed the two central freestanding hydraulic posts and feet. Existing roof, lighting, workshop equipment, side-bay structures and floor composition retained. Generated edit was inspected and exported as optimized WebP; small photographic texture variations from the edit are possible. Original background files retained. Mobile portrait background untouched because its lifts belong to the side bays, not the vehicle presentation.

Three-car transparent images are byte-for-byte unchanged, including original contact shadows. Their positioning/scaling CSS, Hero text, central logo, navbar logo and official artwork are unchanged.

## Validation
- Production build: PASS, including rebuild after final background edit.
- All TypeScript projects: PASS.
- Lint: PASS.
- Full automated suite: 55 files / 394 tests PASS. Final Hero/reference/protected-artwork recheck: 3 files / 15 tests PASS.
- Existing build warnings: ambiguous Tailwind utilities and a large GLTF chunk. Test runner emits existing Router/jsdom/act notices; no failed tests.
- Browser: dark and light at 320×568, 360×640, 390×844, 430×932, 768×1024, 1440×900 and 1920×1080. No horizontal overflow; pills remain separate and readable, with both contact numbers. Desktop Hero framing and original mobile side-car cropping retained. See responsive.json and screenshots.
- Service selection updates details and booking summary. Enter activates service selection. Navbar Book Service opens the canonical four-step popup. Gallery opens and Escape closes. TOLI AI opens and answers a typed contact question correctly. Both Hero tel links unchanged. No external enquiry sent.
- Production browser warnings/errors: none captured during checks.
- Existing AdSense configuration remains disabled, unauthorized and without publisher/unit IDs. Production slots render nothing; consent/loading safeguards unchanged.
- SHA-256 audit: only the six listed existing source/assets plus two new images changed. All 1,393 files checked in the independent 3D project and 2,948 in the original project unchanged. No files removed. See protection.json.

## Evidence and limits
Before/after full-page screenshots and paired Hero comparisons are in this folder. Evidence captures use identical dimensions. Browser viewport checks are emulation, not physical Android/iOS certification. Unsupported-backdrop fallback, actual mouse hover and reduced-motion rendering were reviewed in source; not certified on a separate physical browser. Existing reduced-motion rules retained. Color ratios and perceived 40% frosting are visual approximations.

## Acceptance
| Criterion | Status |
|---|---|
| Frosted location/contact pills | PASS |
| Pill text readability | PASS |
| Foreground hydraulic structures removed | PASS |
| Three vehicles preserved / natural floor contact | PASS |
| Metallic-grey navbar | PASS |
| Non-Hero red/grey metallic theme | PASS |
| Complementary decorative accent | PASS — sparse champagne, not literal 10% pixel coverage |
| Light theme | PASS |
| Responsive layouts | PASS — browser sizes listed above |
| TOLI AI | PASS |
| AdSense safeguards | PASS |
| Local files saved | PASS |
| Separate 3D project unchanged | PASS |
| Deployment | NOT PERFORMED |

Preview: http://127.0.0.1:8200/Toli-2/

## Performance — unresolved regression
Fresh local Lighthouse mobile runs, same production preview and CLI settings:

| Run | Performance | Accessibility | Best practices | SEO | LCP | TBT | CLS |
|---|---:|---:|---:|---:|---:|---:|---:|
| Before | 67 | 100 | 100 | 100 | 5.3s | 510ms | 0 |
| After | 57 | 100 | 100 | 100 | 7.6s | 620ms | 0 |
| After isolated repeat | 50 | 100 | 100 | 100 | 5.6s | 1860ms | 0 |

Performance preservation = FAIL / unresolved. These measurements show a regression and considerable run variability; they do not isolate CSS blur as the cause. The first after run spent much longer loading the unchanged mobile background; the repeat was dominated by increased blocking time. No claim of performance improvement is made. Raw audits are retained. New desktop background weighs 207,552 bytes versus 233,162 originally; tablet is 103,040 versus 102,338. No new JS library or interaction logic was added. Blur is static and limited to two small pills. Existing broader performance work remains necessary before launch.
