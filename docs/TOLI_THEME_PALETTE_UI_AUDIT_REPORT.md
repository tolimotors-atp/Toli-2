# TOLI Motors theme and palette reconstruction

## Summary

The existing automotive composition and routes are preserved. Dark content chapters now use graphite surfaces with red reserved for actions and selection. Light chapters use warm white, pearl and silver with graphite type. In both themes, the real workshop photography and existing MU-X asset have clearer separation from the surrounding UI.

## Findings and changes

| Audit area | Implementation |
| --- | --- |
| Color and light/dark parity | Consolidated section and portal materials in `src/workshop-surfaces.css`. Removed the competing content palette and duplicate form, card and assistant finishes from `src/premium-light.css`. |
| Red and bronze | Filled actions share #B51220 with #C71929 hover and #8F111B pressed. Selection uses a red edge and a theme-appropriate tint. #EA3442 is a highlight. Titanium Bronze stays on chapter metadata and selected numbers. The existing Hero, navbar artwork and product-image colors are deliberate exceptions. |
| Typography | Chapter headings use responsive Inter at 32–64px with consistent weight and a 26ch maximum. Supporting copy uses 15–17px and a 62ch maximum. Chapter metadata uses a 12px label with restrained tracking. |
| Spacing and layout | The main chapters share fluid gutters and the chapter heading has a 1300px maximum width. Repeated gaps and panel padding use the shared spacing values. The chapter order and sticky navigation behavior were retained. |
| Shape, shadows and borders | Use 8px for controls, 12px for panels and 18px for the desktop enquiry dialog. Reserve the existing pill shape for approved brand utilities. Chapter separators replace outlined and shadowed section shells. About, trust and contact use dividers where the panels previously repeated. |
| Motion | Removed the decorative scale on covered chapters and the glow/lift treatment on normalized controls. Retained the section stack, approved Hero and navbar movement, gallery and dialog transitions. Normalized interactions use 150ms and 220ms with the existing easing and reduced-motion support. |
| Hero and contact | The existing light-only central radial now peaks at 65% desktop, 64% tablet and 62% mobile, down from 70%, 67% and 64% in the immediate baseline. Its desktop ellipse shrank from 31% × 136px to 29% × 128px. Photo, floor treatment and crop were retained. The dark lighting was untouched. All measured Hero and navbar geometry matched the baseline. The existing single 30–38px red phone icon, two stacked links and pearl/graphite materials already met the contact requirement and were preserved. |
| Services, vehicle and process | Replaced bright red service rows with a tinted selected row and a clearly separate detail panel. Removed the legacy white-on-white text override in light mode. Preserved the existing user-supplied red MU-X images, wheel and battery illustration controls, and all section copy. |
| Gallery and images | Gallery frames use a quiet border with a shared radius. The original crops, captions, alternative text, lazy sources, responsive assets and lightbox were retained. All 16 images were loaded before the full-page captures. |
| Forms, booking and assistant | Standardized raised surfaces, neutral borders, primary actions, field contrast and focus rings. Removed the enquiry backdrop blur. Verified direct enquiry routing, modal entry, contact draft, and TOLI AI open, close, Enter, send and unrecognized-question fallback. No external WhatsApp draft was sent. |
| Footer and utilities | The footer uses a neutral base, a thin divider and consistent headings. TOLI AI uses a neutral utility treatment and the existing WhatsApp workflow remains in place. |
| Performance and CSS health | The main built stylesheet fell from 354.91 to 335.08 kB, or 58.74 to 56.60 kB gzip. Removed redundant decoration and cascading style rules without adding dependencies. The homepage requested no WebGL runtime or GLB. Archived 3D sources and compatibility styles were retained. |

## Semantic roles

| Role | Dark | Light |
| --- | --- | --- |
| Page | #17191C | #F4F3F0 |
| Subtle surface | #202327 | #E5E5E2 |
| Raised surface | #2A2E33 | #FFFFFF |
| Control surface | #111214 | #FFFFFF |
| Primary text | #F4F3F0 | #24272B |
| Secondary text | #C7C8C6 | #454B52 |
| Muted text | #AEB3B9 | #60656C |
| Strong border | #747A82 | #74777B |
| Focus | #FFA9B1 | #B51220 |

Surface, ink, line, action, focus, error, radius, depth, spacing and timing roles feed the existing component variables. The assistant launcher and enquiry dialog preserve their existing stacking levels through shared tokens. Protected Hero, gallery photo crops and navbar geometry retain their own composition rules.

## Verification and evidence

- Production build, TypeScript and ESLint passed. The complete Vitest suite passed 375 tests across 55 files. The final focused regression rerun passed 82 tests across eight files. Existing React Router and other test-environment warnings appeared in Vitest, separate from production browser output.
- Chromium verified both themes at 320×568, 360×800, 390×844, 412×915, 768×1024, 1366×768, 1920×1080, 844×390 and 683×384. No horizontal overflow, browser warnings, uncaught errors or HTTP asset failures were observed on the homepage. Measured Services panel text contrast was at least 4.5:1 in both themes.
- Tested gallery activation with Enter, next image with Arrow Right and close with Escape. Tested the navigation menu with Enter and Escape, theme switching, enquiry contact draft preservation and assistant replies on desktop and mobile emulation. Verified one H1 on the homepage, direct enquiry, three policy pages and custom 404. The 404 returned HTTP 404.
- [Full desktop pages side by side](theme-audit/screenshots/full-page-comparison.jpg), [desktop Hero comparison](theme-audit/screenshots/hero-comparison.jpg) and [mobile Hero comparison](theme-audit/screenshots/mobile-comparison.jpg). The complete screenshot directory includes before/after vehicle, enquiry and assistant views in both themes.
- [Pre-edit audit](TOLI_COMPLETE_VISUAL_SYSTEM_AUDIT.md), [source inventory](theme-audit/source-inventory.json), [before browser measurements](theme-audit/before-browser.json) and [after browser measurements](theme-audit/after-browser.json).
- [Local production preview](http://127.0.0.1:8230/Toli-2/)

## Files and remaining checks

Source changes are limited to `src/workshop-surfaces.css`, `src/premium-light.css`, `src/brand-environments.css` and `src/components/journey/navbar-brand.css`. The audit, final report, browser measurements and screenshots were added under `docs/`. Both sibling projects were left untouched. No commit, push or deployment was performed.

The 683×384 check approximates desktop reflow at 200% zoom. Native zoom, physical devices, Safari, Firefox and a screen reader were outside this run. The checks are a targeted accessibility and performance assessment rather than an exhaustive WCAG or device benchmark.
