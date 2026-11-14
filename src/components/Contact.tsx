import JourneyTrim from "@/components/journey/JourneyTrim";
import { useSectionEntrance } from "@/hooks/use-section-entrance";
import { useRef, useState } from "react";
import { Phone, Mail, MapPin, Navigation, MapPinOff } from "lucide-react";
import Reveal from "@/components/motion/Reveal";
import { Link } from "react-router-dom";

// Use the existing published address; no unverified place ID or fabricated embed token.
const MAP_EMBED_URL = "https://maps.google.com/maps?q=" + encodeURIComponent("6-2-806, Ram Nagar, Kovur Nagar, Anantapur, Andhra Pradesh 515004") + "&output=embed";
const DIRECTIONS_URL = "https://www.google.com/maps/dir/?api=1&destination=6-2-806+Ram+Nagar+Kovur+Nagar+Anantapur+Andhra+Pradesh+515004";

const Contact = () => {
  const gridRef = useRef<HTMLDivElement>(null);
  const MAP_CONSENT_KEY = "toli:maps-consent";
  const [mapConsent, setMapConsent] = useState<boolean>(
    () => {try {return typeof window !== "undefined" && window.localStorage.getItem(MAP_CONSENT_KEY) === "1";} catch {return false;}}
  );

  const loadMap = () => {
    try {
      window.localStorage.setItem(MAP_CONSENT_KEY, "1");
    } catch { /* Optional browser capability/storage may be unavailable; retain the usable fallback. */ }
    setMapConsent(true);
  };

  // Anime.js scroll-linked reveal for contact cards
  useSectionEntrance(gridRef, ".contact-card, .contact-icon");
  return (
    <section id="contact" className="journey-section journey-contact section-padding luxury-section bg-card/80" data-journey-section="contact">
      <JourneyTrim number="14" label="VISIT TOLI" motif="route" />
      <div className="max-w-5xl mx-auto">
        <Reveal variant="fade" className="text-center mb-12">
          <p className="luxury-kicker text-primary font-medium uppercase text-sm mb-3 text-reveal">Get In Touch</p>
          <h2
            className="luxury-heading font-display text-4xl min-[360px]:text-5xl sm:text-6xl mb-4 text-reveal"
            style={{ "--motion-delay": "80ms" } as React.CSSProperties}
          >
            CONTACT US
          </h2>
          <p className="text-muted-foreground max-w-lg mx-auto">
            Ready to give your car the care it deserves? Reach out today.
          </p>
        </Reveal>

        <Reveal variant="fade" className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5 sm:gap-8 mb-10">
          <div ref={gridRef} className="contents">
            <div
              className="contact-card cinematic-card premium-interactive flex flex-col items-center gap-3 luxury-panel rounded-xl p-5 min-[360px]:p-6 sm:p-8 hover:border-primary/40 hover:shadow-xl hover:shadow-primary/10"
            >
              <Phone className="contact-icon icon-luxury w-11 h-11 rounded-full bg-primary/10 p-2.5 text-primary" />
              <span className="font-display text-xl">CALL US</span>
              <a href="tel:+918074946335" className="text-muted-foreground text-sm inline-flex items-center min-h-11">+91-8074946335</a>
              <a href="tel:+919908303888" className="text-muted-foreground text-sm inline-flex items-center min-h-11">+91-9908303888</a>
            </div>

            <a
              href="mailto:tolimotorsatp@gmail.com"
              className="contact-card cinematic-card premium-interactive flex flex-col items-center gap-3 luxury-panel rounded-xl p-5 min-[360px]:p-6 sm:p-8 hover:border-primary/40 hover:shadow-xl hover:shadow-primary/10"
              style={{ "--motion-delay": "70ms" } as React.CSSProperties}
            >
              <Mail className="contact-icon icon-luxury w-11 h-11 rounded-full bg-primary/10 p-2.5 text-primary" />
              <span className="font-display text-xl">EMAIL US</span>
              <span className="text-muted-foreground text-sm">tolimotorsatp@gmail.com</span>
            </a>

            <a
              href={DIRECTIONS_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="contact-card flex flex-col items-center gap-3 luxury-panel rounded-xl p-5 min-[360px]:p-6 sm:p-8 hover:bg-primary/5 transition-colors"
              style={{ "--motion-delay": "140ms" } as React.CSSProperties}
            >
              <MapPin className="contact-icon icon-luxury w-11 h-11 rounded-full bg-primary/10 p-2.5 text-primary" />
              <span className="font-display text-xl">VISIT US</span>
              <span className="text-muted-foreground text-sm text-center">
                6-2-806, Ram Nagar, Kovur Nagar,<br />Anantapur, Andhra Pradesh 515004
              </span>
            </a>
          </div>
        </Reveal>

        {/* Google Map */}
        <Reveal variant="fade-up" className="mb-6">
          <div className="cinematic-card luxury-panel rounded-2xl overflow-hidden">
            <div className="aspect-[16/9] w-full bg-muted">
              {mapConsent ? (
                <iframe
                  src={MAP_EMBED_URL}
                  width="100%"
                  height="100%"
                  style={{ border: 0 }}
                  allowFullScreen
                  loading="lazy"
                  referrerPolicy="no-referrer-when-downgrade"
                  title="Toli Motors location on Google Maps"
                  className="w-full h-full"
                />
              ) : (
                <div className="flex h-full w-full flex-col items-center justify-center gap-4 px-6 text-center">
                  <div className="flex h-14 w-14 items-center justify-center rounded-full bg-primary/10 text-primary">
                    <MapPinOff className="w-7 h-7" />
                  </div>
                  <p className="max-w-md text-sm text-muted-foreground">
                    This map is embedded from Google Maps. Google may set cookies when it loads.
                  </p>
                  <button
                    type="button"
                    onClick={loadMap}
                    className="luxury-button inline-flex items-center gap-2 px-6 py-3 rounded-full bg-primary text-primary-foreground font-display tracking-wider hover:bg-primary/90 transition-colors"
                  >
                    LOAD MAP
                  </button>
                  <p className="text-xs text-muted-foreground">
                    Your choice is saved on this device. See our{" "}
                    <Link to="/cookie-policy/" className="text-primary underline">Cookie Policy</Link>.
                  </p>
                </div>
              )}
            </div>
            {mapConsent && <button type="button" className="luxury-button m-4 px-4 py-3 border border-border rounded-lg" onClick={()=>{try {localStorage.removeItem(MAP_CONSENT_KEY);}catch { /* Keep revocation available with blocked storage. */ }setMapConsent(false);}}>REMOVE MAP CONSENT</button>}
            <div className="p-4 sm:p-5 flex flex-col sm:flex-row items-center justify-between gap-3">
              <div>
                <p className="font-display text-lg tracking-wider">TOLI MOTORS</p>
                <p className="text-sm text-muted-foreground">6-2-806, Ram Nagar, Kovur Nagar, Anantapur, Andhra Pradesh 515004</p>
              </div>
              <a
                href={DIRECTIONS_URL}
                target="_blank"
                rel="noopener noreferrer"
                className="luxury-button inline-flex items-center gap-2 px-5 py-2.5 rounded-lg border border-border bg-background font-display text-sm tracking-wider hover:border-primary hover:text-primary transition-all"
              >
                <Navigation className="w-4 h-4" />
                GET DIRECTIONS
              </a>
            </div>
          </div>
        </Reveal>
      </div>
    </section>
  );
};

export default Contact;
