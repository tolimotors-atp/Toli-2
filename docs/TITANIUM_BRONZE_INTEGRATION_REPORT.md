# Titanium Bronze integration — 6 November 2026

Target: `/home/thunder/shared/tolimotors-main1/toli-static-website`.
Local source saved. No deployment. Independent 3D/original projects not edited.

## Material system
Titanium Bronze replaces the previous ice-blue accent and champagne page-indicator palette. Shared tokens use #B7834A main bronze, #D3A66F highlight, #E0BE94 reflection, #80572F deep bronze and #51351F shadow. There is no global bronze opacity rule or transparent bronze wash. Functional bronze details use opaque colors; a local metallic reflection is separate from the coverage target.

The composition targets approximately 80% red/grey/graphite/silver and 20% bronze influence. This is a visual design estimate, not a counted pixel ratio. Bronze is distributed through substantial selected-service header trim, active-row edging, card details, progress states, numbering, gallery frames and footer/assistant accents, rather than only tiny icons. Red actions, grey structural surfaces and existing photography remain dominant. No large flat bronze section or bronze Hero overlay was introduced.

## Applied changes
- **01–06 rail:** inactive numbers use main bronze on a darker graphite surface for contrast. The active number uses the bronze reflection shade, a bronze border and reflection, the existing red ambient light and raised effect. Old unrelated gold values were removed from this component. Scroll tracking is unchanged.
- **Services:** a 42px directional metallic bronze trim tops the selected details panel; the active service row keeps its red identity with a deep-bronze trailing edge. Number/icon plates, varied edge details and a bronze CTA border reinforce the material. The Request Service fill stays red.
- **Cards and chapter transitions:** bronze heading plates, a metallic underline, alternating card edges, process-step numbers, selected icons and process/request-panel trim. Existing card surfaces remain graphite/silver with red lighting. Borders are varied rather than identical bronze outlines everywhere.
- **Enquiry:** valid completed steps receive bronze trim and metallic number badges; the current step remains red with bronze/graphite numbering; upcoming steps stay grey. Completion styling excludes error states. The existing validation markers, labels and keyboard focus rings remain intact.
- **Gallery:** bronze number plates, counter, selected frame edges and lightbox controls. Photos have no new filter or tint.
- **TOLI AI:** bronze technical labels, message-edge detail, header separator and launcher icon. Red send/request actions and all response logic are unchanged.
- **Footer:** bronze heading plates, small icons, fine separators and link underline highlights on the existing base.
- **Hero:** only service-tile border colors and the allowed rail trim change. Logo, text, small frosted pills, vehicles, camera/framing, workshop assets and contact-shadow/reflection styles are untouched.

## Files modified
1. `src/workshop-surfaces.css` — bronze tokens and scoped integration across chapters, forms, gallery, footer and AI.
2. `src/components/journey/experience.css` — rail palette and darker number surface for contrast; existing geometry/motion retained.
3. `src/test/fixtures/separation-protected.json` — only the approved experience.css hash updated.
4. This report and `docs/titanium-bronze-evidence`.

No React component, handler, backend, routing, export, dependency, image or model was changed.

## Contrast and accessibility
Twenty sampled functional text/plate or controlled-gradient combinations passed a 4.5:1 target; the lowest checked ratio is **4.77:1** (main bronze rail number on its darkest permitted graphite system). See contrast-results.json. Functional light-theme text uses deep bronze/shadow on pearl; dark-theme small text uses the reflection shade on controlled graphite plates. Selected service numbers/arrows remain legible in both themes. Completed-step dark text is checked against the darkest stop of its bright bronze gradient.

This is targeted contrast verification, not a full accessibility certification. Existing keyboard focus rings were retained instead of replacing them with lower-contrast bronze outlines on mixed backgrounds. Error flags are excluded from completed-step bronze styling. Reduced-motion behavior is preserved; no animation, blur or heavy renderer was added.

## Validation
- **Production build:** PASS, including final rebuild after visual/accessibility corrections.
- **All TypeScript projects:** PASS.
- **Lint:** PASS.
- **Automated suite:** 55 files, 394 tests PASS. Existing request flow, validation/drafts, gallery, theme, AI and protected-artwork checks passed. No tests were removed or bypassed.
- **Responsive browser checks:** nine required sizes in dark and light themes, 18 PASS: 360×640, 390×844, 430×932, 600×960, 768×1024, 1024×768, 1366×768, 1440×900 and 1920×1080. No horizontal overflow, no corner-pill/logo/heading/caption collisions; vehicle images loaded. See responsive-results.json.
- **Hero protection:** exact dark-theme before/after rectangles match for the Hero, logo, vehicle image and both corner pills at all nine sizes. SHA-256 checks confirm all 22 saved Hero asset/style/component files are unchanged, including grounding and compact-pill styles. See hero-protection.json.
- **Enquiry interaction:** popup opens; contact test data survives step/theme changes and appears correctly in Review. Completed/current/upcoming states were inspected. Empty required fields still produce errors and error markers are not treated as completion. Temporary contact data was cleared. No WhatsApp draft or enquiry was submitted.
- **Gallery/AI:** image preview opens, Next changes the image, Escape closes; AI returns its existing Battery Services response. Both themes inspected.
- **Final production console:** no warnings/errors in the final fresh tab. A stopped local preview server caused an earlier module-fetch failure during QA; the module existed on disk, the server was restarted, and the form/assistant/gallery were rechecked successfully. No code workaround was added for that local outage.
- Existing build warnings about ambiguous utilities and the large loader chunk remain; existing test-runner Router/jsdom notices remain.

## Evidence
Full-page before/after captures, mobile enquiry/AI and gallery interaction shots, theme comparisons, geometry and contrast records are in `titanium-bronze-evidence`.

Design-taste principles were used for consistency, visual rendering and contrast review within the existing approved design. Its starter/layout/copy replacement workflow and kit-specific layout checker were not applied: those would conflict with the user's explicit requirements to preserve the Hero, real contact details, gradients and existing layout.

## Acceptance
| Criterion | Status |
|---|---|
| Titanium Bronze implemented | PASS |
| Bronze presence approximately 20% | PASS — visual design estimate, not a pixel measurement |
| Red + grey approximately 80% | PASS — dominant surfaces and red CTAs retained |
| Bronze not implemented as 20% opacity | PASS |
| Metallic bronze depth | PASS |
| 01–06 bronze system | PASS |
| Services integration | PASS |
| Enquiry integration | PASS |
| Gallery integration | PASS |
| TOLI AI integration | PASS |
| Light theme | PASS |
| Dark theme | PASS |
| Small Hero pills preserved | PASS |
| Desktop cars grounded | PASS — existing grounding untouched |
| Mobile/tablet responsiveness | PASS |
| Local files updated | PASS |
| Separate 3D website unchanged | PASS — no writes |
| Deployment | NOT PERFORMED |

## Limits
Physical-device and other-engine testing were not performed. No new Lighthouse/performance audit was run; the previously reported performance regression remains unresolved. The 80/20 balance is a compositional judgement rather than a certified numeric coverage result.

Preview: http://127.0.0.1:8200/Toli-2/
