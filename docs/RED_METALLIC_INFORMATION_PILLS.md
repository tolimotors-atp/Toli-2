# Red metallic information pills — 5 November 2026

Project: `/home/thunder/shared/tolimotors-main1/toli-static-website`.
[Production preview](http://127.0.0.1:8200/Toli-2/) · [Saved-source preview](http://127.0.0.1:8190/Toli-2/).

## Result

Both Hero corner groups now share the actual `toli-logo-pill` styling class plus a scoped `hero-info-pill` material. They reuse the logo capsules' 999px radius, thin silver border convention, upper-edge highlight geometry and `--logo-badge-depth` shadow structure. The original logo artwork, logo-pill stylesheet and logo component were not changed.

The information capsules use red stops through 70% of a 108-degree gradient (`#a80f27`, `#d1162e`, `#b6112a`), blending into metallic `#666a73`/`#555963` at the trailing edge. This is an approximate visual 70/30 balance, not a pixel-area measurement. A restrained upper gloss, silver hairline, inset depth and bounded red shadow provide polish. No new blur filters, images, libraries or continuous motion were added. The original logo glow pseudo-element is disabled only on the information capsules; their ambient glow uses the bounded shadow.

ANANTAPUR stays bold and larger than the refined subtitle. The decorative slash before SERVICE was removed to match the requested two-line content. Both verified phone numbers, the phone icon and original `tel:` destinations are retained. White text is used in both themes. Capsules have 8px/20px desktop padding and 8px/14px at tablet/mobile widths; mobile telephone targets remain at least 44px high. Narrow layouts naturally stack the groups; tablet and desktop keep separated corner placement.

The navbar now uses red through roughly 70% of its horizontal material before transitioning into graphite/metal. Light mode also retains a red-dominant brand surface with its existing neutral controls. Navbar height, spacing, logo, silver car, car animation and navigation handlers are unchanged.

## Saved files

- `src/components/Hero.tsx`: shared capsule classes and subtitle separator only.
- `src/components/journey/hero-corner-visibility.css`: reusable scoped information material, padding and typography.
- `src/components/journey/navbar-brand.css`: red-dominant navbar gradient in both themes.
- `src/test/hero-reference.test.tsx` and `src/test/navbar-motion.test.tsx`: intentional subtitle assertions updated.
- `src/test/fixtures/separation-protected.json`: only the authorized Hero source hash updated.

Supporting artifacts: this report, [saved change log](RED_INFORMATION_PILLS_CHANGELOG.md), and `docs/red-information-pills-evidence/`. Changes were saved directly in the actual project, checked on disk and confirmed in the dev preview. No Git commits, deployment or protected-project writes occurred.

## Screenshots

[Before desktop](red-information-pills-evidence/before-desktop.jpg) · [Before/after desktop](red-information-pills-evidence/before-after-desktop.jpg).

| View | Dark | Light |
|---|---|---|
| Desktop 1440 | [Screenshot](red-information-pills-evidence/opening-dark-1440.jpg) | [Screenshot](red-information-pills-evidence/opening-light-1440.jpg) |
| Tablet 768 | [Screenshot](red-information-pills-evidence/opening-dark-768.jpg) | [Screenshot](red-information-pills-evidence/opening-light-768.jpg) |
| Mobile 320 | [Screenshot](red-information-pills-evidence/opening-dark-320.jpg) | [Screenshot](red-information-pills-evidence/opening-light-320.jpg) |
| Mobile 390 | [Screenshot](red-information-pills-evidence/opening-dark-390.jpg) | [Screenshot](red-information-pills-evidence/opening-light-390.jpg) |

## Validation

- Production build: PASS (25.95s). Existing large-chunk/Tailwind warnings remain.
- TypeScript app/node/QA checks: PASS.
- Lint: PASS.
- Relevant automated tests: **78 PASS across seven files**, covering Hero artwork/contact data, navbar motion, AI, request routing, pre-launch ad safeguards and protected workshop assets. The initial run found one additional obsolete slash assertion; it was updated and the relevant suite rerun successfully. Existing React Router and jsdom scroll notices remain in test output.
- Both themes checked at **320×568, 360×640, 390×844, 430×932, 768×1024, 1440×900, 1920×1080**.
- Measurements show no overlap between pills or with the central logo, both capsules below the navbar, both pills within the viewport and no horizontal document overflow. Numbered navigation stays clear in the screenshots. See [responsive measurements](red-information-pills-evidence/responsive.json).
- Phone destinations remain `tel:+919908303888` and `tel:+918074946335`. No call was initiated.
- Production Book Service opens the canonical Service Request popup. TOLI AI still answers contact questions with both verified numbers. Production console was empty of warnings/errors during the checks. No enquiry or external message was sent.
- These are browser viewport checks, not physical-device certification. No new Lighthouse run was required or claimed for this scoped styling task; previous mobile-performance limitations remain outside its scope.

## Protection

A fresh before/after source-and-asset hash comparison found exactly the six implementation/test files above changed. No source files were added or removed. The central/logo capsule CSS and component, car/background assets, heading/caption text, Services finish, Gallery, enquiry/WhatsApp logic, AI implementation and advertising safeguards are unchanged. Padding can naturally increase the corner-information row; no vehicle scaling or background framing rules were changed.

All **1,393** audited files in `toli-3d-website` and **2,948** in the original `tolimotors-main` sibling are unchanged. The comparison excludes generated docs/build/dependency directories. [Protection result](red-information-pills-evidence/project-protection.json).

## Acceptance

| Criterion | Result |
|---|---|
| LOCATION METALLIC PILL | PASS |
| CONTACT METALLIC PILL | PASS |
| RED-DOMINANT GRADIENT | PASS |
| GLOSSY SHINE AND GLOW | PASS |
| NAVBAR RED GRADIENT | PASS |
| TEXT READABILITY | PASS |
| RESPONSIVE LAYOUT | PASS for listed browser checks |
| LOCAL FILES SAVED | PASS |
| EXISTING FUNCTIONALITY PRESERVED | PASS for relevant suite and browser checks |
| 3D WEBSITE UNCHANGED | PASS |
| DEPLOYMENT | NOT PERFORMED |
