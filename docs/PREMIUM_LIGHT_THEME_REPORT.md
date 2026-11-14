# Premium TOLI Motors light theme

Validated locally on 10 November 2026. Static project only; no deployment.

## Result

The existing light mode now has pearl and warm-white rooms, metallic silver panels, graphite typography, approved bright-red actions and restrained bronze technical accents. The existing theme toggle, preference storage, enquiry flow and AI behavior remain in place. Dark mode remains available with its existing appearance.

Production preview: http://127.0.0.1:8208/Toli-2/
Development preview: http://127.0.0.1:8190/Toli-2/

## Palette and materials

| Role | Value / treatment |
| --- | --- |
| Page | `#F4F3F0` |
| Pearl | `#FAF9F6` |
| Raised white | `#FFFFFF` |
| Metallic inner surface | `#E5E5E2` |
| Silver | `#C7C8C6` |
| Primary / deep copy | `#24272B` / `#17191C` |
| Supporting / secondary copy | `#454B52` / `#60656C` |
| Input boundary | `#74777B` |
| Bright primary red | Existing `--brand-red` (`#E52238`), preserved |
| Readable red copy / focus / depth | `#B51B29` |
| Error | `#A4192C` |
| Technical bronze | `#80572F`, thin `#B7834A` edges |

New `--light-*` tokens define surfaces, text, boundaries and three shadow elevations. Scoped semantic variables reuse the existing components. White radial highlights, silver directional gradients and approximately 4% red reflected light create depth without heavy blur or new rendering libraries. Bronze is limited to labels, dividers and completed-step details; no beige or orange room backgrounds.

Cards use white-to-silver gradients, thin defined edges, inset highlights and low-opacity graphite shadows. Section headings remain dark with red micro-dividers. Primary buttons retain approved bright red with darker depth and white text. Secondary buttons use silver, graphite and red hover/selection states. Scrollbars and text selection have corresponding light variants.

## Coverage

- **Navigation:** theme materials only: pearl/silver background, graphite controls, red booking action and neutral elevated logo pill. Original artwork, car graphic, dimensions, placement and behavior unchanged.
- **Hero:** no new Hero selectors or structural/asset changes. Existing Hero theme behavior remains in force.
- **Services and process:** visible card boundaries, readable icons/copy and red active states.
- **Explore Vehicle Components:** pearl/silver room with restrained red reflection, dark heading, metallic component buttons and red selected state. No restored rotation controls.
- **All three MU-X locations:** existing red front-three-quarter WebP remains unchanged in components, Section 03 and Section 05. Only the surrounding contact-shadow treatment changes. Production verified all three loaded the same approved asset; zero active canvases.
- **Enquire Now:** popup and direct page use matching pearl/silver surfaces, white fields, graphite labels/placeholders, red focus and validation, readable selected/completed steps, brand search results and review details. Back/Continue/close controls remain accessible. A light-only tablet correction replaces the desktop translate entrance with the existing stationary fade at widths up to 900px; existing reduced-motion handling remains applicable.
- **Gallery:** photography remains unfiltered with silver edges/shadows. Lightbox has a neutral light surface.
- **Footer/contact:** deliberate silver/light-graphite surfaces with readable links and red/bronze details.
- **TOLI AI:** pearl launcher, panel, messages, quick actions and input; graphite text; red send/focus states; explicit readable disabled styling. Existing service response behavior verified.

## Responsive and interaction validation

Checked nine major views at every requested size: Hero, services, components, Section 03, trust, gallery, Section 05, contact and footer.

| Viewport | Section checks | Enquiry close/actions | AI panel/input | Horizontal overflow |
| --- | --- | --- | --- | --- |
| 320 × 568 | PASS | PASS | PASS | None |
| 360 × 800 | PASS | PASS | PASS | None |
| 390 × 844 | PASS | PASS | PASS | None |
| 412 × 915 | PASS | PASS | PASS | None |
| 768 × 1024 | PASS | PASS after entrance correction | PASS | None |
| 1366 × 768 | PASS | PASS | PASS | None |
| 1920 × 1080 | PASS | PASS | PASS | None |

63 final light section checks passed; each checked framing, occlusion, overflow and image loading where applicable. Form and AI checks covered all seven sizes. Raw chronological observations retain the initial tablet entrance failure; the corrected retest passes. `validation-summary.json` contains the final observations.

Three full dark/light toggle cycles preserved Mahindra / Scorpio enquiry values. Service selection and review displayed the correct vehicle/service values. Required contact validation remained functional and readable. No customer contact data was entered and no WhatsApp submission was sent. A local AI service question returned the existing catalogue response. Preference persisted through reload on both the development and production origins.

Dark regression: inspected all nine views at laptop size plus Hero, components and booking on mobile; popup/AI controls passed desktop/mobile checks. Captured dark evidence. All 74 new CSS rules require `[data-theme=light]`. Dark rules and preference implementation were not edited.

### Accessibility and zoom

The added contrast test checks primary/deep/body/metadata/red text at least 4.5:1 against page/pearl/white/metal, input boundaries at least 3:1, and white action text at least 4.5:1 against the relevant red surfaces. Explicit red keyboard focus, error borders/messages and readable disabled states were inspected. This is targeted contrast and usability verification, not a formal whole-site accessibility certification.

The in-app browser did not apply native zoom shortcuts. A 200%-equivalent 683 × 384 reflow check passed: the form close control and action bar remained accessible with internal scrolling and no horizontal overflow. Native browser zoom and physical-device testing remain unverified.

## Technical validation

- TypeScript: PASS — application, node and QA configurations.
- ESLint: PASS.
- Production build: PASS — 18.19 seconds.
- Final tests: PASS — 55 files / 374 tests, 151.81 seconds.
- Production browser console: no warnings or errors during the checked direct enquiry/home/vehicle flows.
- Existing development React Router future-flag warnings and build advisory for a historical scene chunk remain. Existing Tailwind ambiguous-utility warnings remain. These are outside the light-theme change.
- No dependencies, fonts, WebGL effects or vehicle assets added.

## Saved evidence

Screenshots: `docs/light-theme/screenshots/`

- `light-theme-home-desktop.jpg`
- `light-theme-section03-red-mux.jpg`
- `light-theme-vehicle-components.jpg`
- `light-theme-section05-red-mux.jpg`
- `light-theme-enquire-now.jpg`
- `light-theme-toli-ai.jpg`
- `light-theme-mobile.jpg`
- `light-enquire-direct-production.jpg`
- `overview.jpg`
- `dark-*-desktop.jpg`, `dark-*-mobile.jpg`, `dark-enquiry-mobile.jpg`, `dark-ai-mobile.jpg`
- Individual section/form/AI captures at the requested viewports.

Observations: `responsive.json`, `ui-responsive.json`, `dark-regression.json`, `toggle-proof.json`, `zoom-reflow.json`, `production-proof.json`, `validation-summary.json` under `docs/light-theme/`.

## Files and protection

Source changes:

1. `src/premium-light.css` — light-only tokens and component theme treatments.
2. `src/main.tsx` — import light finish after existing theme/layout styles.
3. `src/test/brand-palette.test.ts` — contrast test against actual light tokens.

Documentation/evidence: this report and `docs/light-theme/`.

A 393-file source/public baseline verified only the two intended existing source files above changed. Hero, navbar component source, vehicle artwork, workshop assets, theme-persistence implementation and existing provider were unchanged. All other new styling is confined to the new light stylesheet. No separate 3D project was edited.

## GitHub and release status

After validation, `git status --short` returned:

```
fatal: not a git repository (or any parent up to mount point /)
Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).
```

There is no repository/current branch/configured remote in this project checkout. Commit and push are BLOCKED. No repository was initialized, no remote was invented and no repository configuration was changed. An existing Git checkout or configured remote/branch is needed to complete publishing.

Deployment: NOT PERFORMED.
