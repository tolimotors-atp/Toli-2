import { GOOGLE_REVIEWS_URL } from '@/lib/google-reviews';
import ToliLogoPill from '@/components/ToliLogoPill';
import JourneyTrim from "@/components/journey/JourneyTrim";
import { navigateExperience } from "@/lib/experience-navigation";
import { useSectionEntrance } from "@/hooks/use-section-entrance";
import { useRef } from "react";
import { Link } from "react-router-dom";
import { adsConfigured, advertising } from "@/lib/advertising";
import { reopenConsent } from "@/lib/consent";
import { Phone, Mail, MapPin, Star } from "lucide-react";
import Reveal from "@/components/motion/Reveal";
import { stagger } from "animejs";

const quickLinks = [
  { label: "Services", href: "#services" },
  { label: "Offers", href: "#offers" },
  { label: "About", href: "#about" },
  { label: "Gallery", href: "#gallery" },
  { label: "Why Us", href: "#why-us" },
  { label: "Contact", href: "#contact" },
];

const Footer = () => {
  const footerRef = useRef<HTMLElement>(null);

  // Anime.js scroll-linked reveal for footer content
  useSectionEntrance(footerRef, ".footer-section, .social-icon");  return (
    <footer ref={footerRef} className="journey-section journey-footer bg-secondary/70 border-t border-border" data-journey-section="footer"><h2 className="sr-only">Toli Motors links and contact details</h2>
      <JourneyTrim number="15" label="SERVICE · REPAIR · CARE" motif="ring" />
      <Reveal as="div" variant="fade-up" stagger={55} className="max-w-7xl mx-auto px-6 py-14 grid gap-10 md:grid-cols-4">
        <div className="footer-section md:col-span-1">
          <ToliLogoPill/>
          <p className="text-sm text-muted-foreground leading-relaxed">
            A trusted multi-brand car workshop in Anantapur — premium care, genuine parts, fair pricing.
          </p>

        </div>

        <div className="footer-section">
          <h3 className="font-display text-lg tracking-wider mb-4">QUICK LINKS</h3>
          <ul className="space-y-2 text-sm">
            {quickLinks.map((l) => (
              <li key={l.label}>
                <a href={l.href} onClick={(event) => {
                  if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
                  const section = document.getElementById(l.href.slice(1));
                  if (!section) return;
                  event.preventDefault();
                  history.replaceState(history.state, "", l.href);
                  navigateExperience(l.href.slice(1));
                }} className="text-muted-foreground hover:text-primary transition-colors duration-200 hover:translate-x-0.5 inline-block">
                  {l.label}
                </a>
              </li>
            ))}
            <li><Link to="/enquire-now/" className="text-muted-foreground hover:text-primary">Request service</Link></li>
          </ul>
        </div>

        <div className="footer-section">
          <h3 className="font-display text-lg tracking-wider mb-4">CONTACT</h3>
          <ul className="space-y-3 text-sm text-muted-foreground">
            <li className="flex items-start gap-2">
              <Phone className="w-4 h-4 text-primary mt-0.5 shrink-0" />
              <span>
                <a href="tel:+918074946335" className="hover:text-primary block">+91-8074946335</a>
                <a href="tel:+919908303888" className="hover:text-primary block">+91-9908303888</a>
              </span>
            </li>
            <li className="flex items-start gap-2">
              <Mail className="w-4 h-4 text-primary mt-0.5 shrink-0" />
              <a href="mailto:tolimotorsatp@gmail.com" className="hover:text-primary break-all">tolimotorsatp@gmail.com</a>
            </li>
            <li className="flex items-start gap-2">
              <MapPin className="w-4 h-4 text-primary mt-0.5 shrink-0" />
              <span>6-2-806, Ram Nagar, Kovur Nagar,<br />opposite DMart, Anantapur, Andhra Pradesh 515004</span>
            </li>
            <li className="flex items-start gap-2">
              <Star className="w-4 h-4 text-primary mt-0.5 shrink-0" />
              <a
                href={GOOGLE_REVIEWS_URL}
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-primary"
              >
                Read our reviews on Google
              </a>
            </li>
          </ul>
        </div>

        <div className="footer-section">
          <h3 className="font-display text-lg tracking-wider mb-4">LEGAL</h3>
          <ul className="space-y-2 text-sm">
            <li>
              <Link to="/privacy-policy/" className="text-muted-foreground hover:text-primary transition-colors duration-200 hover:translate-x-0.5 inline-block">
                Privacy Policy
              </Link>
            </li>
            <li>
              <Link to="/terms-and-conditions/" className="text-muted-foreground hover:text-primary transition-colors duration-200 hover:translate-x-0.5 inline-block">
                Terms &amp; Conditions
              </Link>
            </li>
            <li>
              <Link to="/cookie-policy/" className="text-muted-foreground hover:text-primary transition-colors duration-200 hover:translate-x-0.5 inline-block">
                Cookie Policy
              </Link>
            </li>
          </ul>
        </div>
      </Reveal>

      <div className="border-t border-border">
        <div className="max-w-7xl mx-auto px-6 py-5 flex flex-col md:flex-row items-center justify-between gap-3 text-sm text-muted-foreground">
          <ToliLogoPill/>
          <nav className="flex flex-wrap justify-center gap-x-5 gap-y-1" aria-label="Legal">
            <Link to="/privacy-policy/" className="hover:text-primary transition-colors">Privacy</Link>
            <Link to="/terms-and-conditions/" className="hover:text-primary transition-colors">Terms</Link>
            <Link to="/cookie-policy/" className="hover:text-primary transition-colors">Cookies</Link>
            {adsConfigured(advertising) && <button type="button" onClick={reopenConsent} className="hover:text-primary transition-colors">Privacy choices</button>}
          </nav>
          <p>&copy; {new Date().getFullYear()} Toli Motors (Multi-brand Car Workshop). All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
