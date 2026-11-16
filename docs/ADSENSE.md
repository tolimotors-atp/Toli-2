# Switching on Google AdSense (owner guide)

Nothing here costs you anything until AdSense approves you. Ads stay **off** until every step below is done. This is practical guidance, not legal advice.

## Part A: Get a real domain live
AdSense does **not** accept `ganesh-g18.github.io/...` addresses. You need your own domain (for example `tolimotors.in`).
1. Buy the domain from any registrar (GoDaddy, Namecheap, Google Domains successor, etc.).
2. In GitHub: repository **Toli-2 → Settings → Pages → Custom domain**, type your domain (for example `www.tolimotors.in`), Save.
3. At your registrar's DNS page, add what GitHub's Pages help page tells you: for `www`, a **CNAME** record pointing to `ganesh-g18.github.io`; for the bare domain, the four GitHub **A** records. (Do this yourself; never share registrar passwords in chat.)
4. Wait (minutes to a day), then tick **Enforce HTTPS** in the same Pages screen.

## Part B: Tell the site its address
5. GitHub: **Toli-2 → Settings → Secrets and variables → Actions → Variables tab → New repository variable**.
6. Name `VITE_SITE_URL`, value `https://www.tolimotors.in/` (your real address, with `https://` and a trailing `/`). Save.
7. **Actions → Deploy to GitHub Pages → Run workflow.** After it finishes, open `https://your-domain/robots.txt` (should say `Allow: /`) and `https://your-domain/sitemap.xml`. Before this step the site tells Google *not* to index it.

## Part C: Apply for AdSense
8. Go to adsense.google.com and sign in with your Google account. Enter your site address, country and payment details **on Google's pages only**.
9. Google shows a publisher ID like `ca-pub-1234567890123456` (AdSense → Account → Settings → Account information).
10. Add repository variable `VITE_ADSENSE_PUBLISHER_ID` with that ID. Re-run the deploy. This publishes `ads.txt` and the `google-adsense-account` tag that Google checks. Click **Verify / Request review** in AdSense. Approval can take days to weeks. Ads are still **not** shown.

## Part D: Switch ads on (after approval)
11. In AdSense: **Ads → By ad unit → Display ads**, create two units named `after-gallery` and `before-footer`. Each has a 10-digit slot ID (`data-ad-slot`).
12. Add variables `VITE_ADSENSE_SLOT_AFTER_GALLERY` and `VITE_ADSENSE_SLOT_BEFORE_FOOTER` with those 10-digit numbers.
13. Add `VITE_ADS_ENABLED` = `true` and `VITE_ADS_LIVE_AUTHORIZED` = `true`. These are the two safety switches; remove either to turn ads off again.
14. **Funding Choices (needed for visitors in the EEA, UK, Switzerland):** AdSense → **Privacy & messaging** → create a **GDPR message**, select your site, publish it. Google then shows its own certified consent message to those visitors. Our banner is a simple choice for everyone else and does not replace Google's tool.
15. Re-run the deploy.

## Part E: Check it worked
16. Open the site in a private window: the **Privacy choices** banner appears; no Google requests happen until you click **Accept all** (browser DevTools → Network, filter `googlesyndication`).
17. After Accept, two boxes labelled **Advertisement** appear (after the gallery and before the footer). They stay empty for a while until Google fills them. **Reject non-essential** shows no ads and makes no Google request.
18. `https://your-domain/ads.txt` shows one line starting `google.com, pub-…`. Footer **Privacy choices** reopens the banner.
19. Never click your own ads.

## Content AdSense expects (owner input needed, none invented)
Thin sites get rejected. Suggested additions, to be written by you from real facts: a fuller About page (history, team, workshop photos); one short page per main service (what is done, typical time, brands handled); an FAQ from real customer questions; opening hours; a genuine customer-reviews page. Aim for original text, not copied.
