import { Link } from "react-router-dom";
import LegalPageShell from "@/components/LegalPageShell";

const CookiePolicy = () => (
  <LegalPageShell kicker="Legal" title="Cookie Policy">
    <p><strong>Last updated: 16 November 2026</strong></p>
    <p>
      This Cookie Policy explains how the Toli Motors website uses cookies and similar technologies, and
      what choices you have.
    </p>

    <h2>1. What are cookies?</h2>
    <p>
      Cookies are small text files stored on your device when you visit a website. They are widely used to
      make websites work, work more efficiently, or provide information to the site owner.
    </p>

    <h2>2. Cookies on this website</h2>
    <p>
      This website <strong>does not set any first-party cookies</strong> and does not run analytics. We do not use cookies to
      identify you or build a profile. Your theme and advertising choices are saved in your browser’s localStorage, which is not a cookie.
      When advertising is switched on, third parties may set cookies, but only after you choose “Accept all”.
    </p>

    <h2>3. Third-party cookies</h2>
    <p>The only cookies that could be set come from third-party services used by this website:</p>
    <table className="w-full text-sm">
      <thead>
        <tr className="border-b border-border text-left">
          <th className="py-2 pr-4">Service</th>
          <th className="py-2 pr-4">Why</th>
          <th className="py-2">How to control</th>
        </tr>
      </thead>
      <tbody>
        <tr className="border-b border-border/60">
          <td className="py-2 pr-4">Google AdSense</td>
          <td className="py-2 pr-4">
            Advertising, when switched on. Google and its partners use cookies and similar technology to show and measure ads
            and, if you accept, to personalise them.
          </td>
          <td className="py-2">
            Nothing loads until you choose “Accept all”. Use “Privacy choices” in the footer to change your choice, or see the links below.
          </td>
        </tr>
        <tr className="border-b border-border/60">
          <td className="py-2 pr-4">Google Fonts</td>
          <td className="py-2 pr-4">
            Font files are self-hosted in the current release.
          </td>
          <td className="py-2">No Google Fonts request is made by this release.</td>
        </tr>
      </tbody>
    </table>

    <h2>4. Your advertising choice</h2>
    <p>
      The first time you visit, a banner asks you to choose. <strong>Accept all</strong> allows Google advertising to load. <strong>Reject non-essential</strong>
      keeps all Google advertising switched off on this site. Your choice is remembered in your browser using <strong>localStorage</strong>. Open
      “Privacy choices” in the page footer at any time to change it. If you withdraw consent after ads have loaded, the page reloads so the ad code stops running.
    </p>
    <p>
      Google and its partners use cookies and similar technology for advertising. To learn more or opt out, see
      <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener noreferrer">how Google uses information from sites that use its services</a>, <a href="https://adssettings.google.com" target="_blank" rel="noopener noreferrer">Google Ads Settings</a> and the <a href="https://optout.aboutads.info" target="_blank" rel="noopener noreferrer">industry opt-out page (aboutads.info)</a>. Visitors in the EEA, UK and Switzerland are shown Google’s certified consent message where advertising is enabled.
    </p>

    <h2>Local preferences and enquiry drafts</h2><p>Theme preferences are also stored in localStorage. Enquiry drafts are held in memory while the page is open, rather than written to localStorage.</p>
    <h2>5. How to control or delete cookies</h2>
    <p>
      Most browsers let you view, block, or delete cookies, and to block third-party requests. The "Help"
      menu of your browser explains how. Blocking advertising cookies does not affect how the rest of this website works.
    </p>

    <h2>6. Contact</h2>
    <p>
      Questions about this Cookie Policy:{" "}
      <a href="mailto:tolimotorsatp@gmail.com">tolimotorsatp@gmail.com</a>.
    </p>

    <p>
      Read more in our <Link to="/privacy-policy/">Privacy Policy</Link>.
    </p>


    <h2>Trademarks</h2>
    <p>
      Toli Motors is an independent multi-brand workshop. It is not owned by, affiliated with or endorsed by any car manufacturer. Car brand names and logos shown on this website belong to their respective owners and are used only to say which makes of vehicle we service.
    </p>
  </LegalPageShell>
);

export default CookiePolicy;