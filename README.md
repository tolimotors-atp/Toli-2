# Toli Motors website

Run `npm ci`, then `npm run dev`. The default local URL is http://127.0.0.1:8190/Toli-2/. Use `npm run build` and `npm run preview` to check the production output. The verification commands are `npm run typecheck`, `npm run lint`, and `npm test`.

## Domain and hosting

Connect the owned domain in the hosting provider and apply the provider's DNS and HTTPS instructions. Set `VITE_SITE_URL` to the final public HTTPS URL before building. The URL path sets the build base, so a custom domain at its root produces root-relative assets and clean routes. A build without a public URL stays on `/Toli-2/` and discourages indexing.

Publish `dist/` with directory indexes enabled. Serve each generated route directly, redirect slashless page URLs to their trailing-slash versions, and serve `404.html` with HTTP status 404 for unknown URLs. Avoid a catch-all rewrite that serves the homepage with status 200. Test a direct request to `/enquire-now/` and a nonexistent URL after deployment. Old homepage hash routes are migrated in the browser.

The build generates per-page titles, descriptions, social tags, canonical links, breadcrumb data and a homepage AutoRepair schema. With a public URL it also generates `sitemap.xml` and points to it from `robots.txt`. The assistant reference file is `llms.txt` and the requested `lms.txt` is an alias. Both are served from the build root.

## Release checks

- Check the public hostname, HTTPS, redirects and 404 status.
- Inspect each clean route's title, description, canonical, one H1 and breadcrumb. Check the sitemap and social image using the public hostname.
- Check production console, broken resources, image alternative text and script sizes. Production maps are disabled. Decorative images deliberately have empty alt attributes.
- Confirm the published privacy and terms copy with the business. Use confirmed profile URLs and genuine workshop photos for any future additions.
- The live site uses the existing WhatsApp enquiry handoff and still vehicle artwork. Optional Supabase configuration is listed in `.env.example`. Keep private service keys out of Vite variables.
