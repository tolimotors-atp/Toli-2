# Saved change log — 5 November 2026

- Baseline recorded from actual static project; no Git repository present, no resets/commits used.
- Step 2 saved: navbar-brand.css uses graphite/metal/red lighting; light mode uses pearl/silver. Navbar artwork and geometry unchanged.
- Step 3 saved: local Hero corner backplates, high-contrast type, visible phone icon and mobile separation; existing heading/assets retained.
- Step 4 saved: reproduced ABOUT-query gap; added verified business/contact answers and actionable fallback, guarded answer failures, composition-safe Enter and viewport resize fallback.
- Reproduced a stale click-time AI import failure in the dev browser. Saved AIChatWidget.tsx with the small panel bundled into the already route-lazy homepage; removed the rejected-lazy-import trap.
- Focused checks passed: navbar 5 tests, Hero 4 tests, TOLI AI 35 tests.
- Final validation passed: production build, app/node/QA TypeScript, lint, 394 tests across 55 files.
- Verified saved-source preview at 8190 and final production preview at 8200; both themes and all requested viewports checked.
- Real browser: Enter and Send, repeated questions, unsupported fallback, Escape/focus restore, bounded mobile chat and AI-to-Service-Request handoff verified. No external enquiry sent.
- Verified assistant opens and answers after the loaded dev server was stopped; restarted the server afterward. Current Lighthouse: 60/100/100/100; no fresh before/after performance claim.
