import JourneyTrim from "@/components/journey/JourneyTrim";
import { useSectionEntrance } from "@/hooks/use-section-entrance";
import { useRef } from "react";
import Reveal from "@/components/motion/Reveal";
import { brandLogos } from "@/lib/brand-logos";
const brands = [
  "Maruti Suzuki", "Hyundai", "Tata", "Toyota", "Mahindra", "Kia", "Honda",
  "MG", "Renault", "Nissan", "Volkswagen", "Škoda", "Ford", "Jeep", "Isuzu",
  "Volvo", "Audi", "BMW", "Mercedes-Benz"
];

const BrandPartners = () => {
  const sectionRef = useRef<HTMLElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  useSectionEntrance(sectionRef, ".brand-logo-item");
  return (
    <section ref={sectionRef} className="journey-section journey-brands py-12 sm:py-16 border-y border-border bg-secondary/30" data-journey-section="brands">
      <JourneyTrim number="04" label="MULTI-BRAND CARE" motif="ring" />
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <Reveal variant="fade" className="text-center mb-10">
          <p className="text-sm text-muted-foreground uppercase tracking-widest">
            Multi-brand vehicle care
          </p>
        </Reveal>

        <div
          ref={containerRef}
          className="grid grid-cols-2 min-[360px]:grid-cols-3 sm:grid-cols-4 md:grid-cols-6 lg:grid-cols-7 gap-4 sm:gap-5 items-center justify-items-center"
        >
          {brands.map((brand) => (
            <div
              key={brand}
              data-brand={brand}
              className="brand-logo-item flex flex-col items-center justify-center gap-2 min-h-24 w-full text-center text-sm font-medium px-2 sm:px-4 py-3 rounded-xl border border-border/60 bg-background/60 backdrop-blur-sm hover:border-primary/30 hover:bg-primary/5 hover:shadow-sm transition-all duration-300 cursor-default break-words"
            >
              <svg viewBox={brandLogos[brand]?.viewBox ?? "0 0 24 24"} className={`brand-logo-mark h-8 text-foreground/85 ${brandLogos[brand]?.viewBox ? "w-20" : "w-12"}`} fill="currentColor" aria-hidden="true" focusable="false">
                {brandLogos[brand]?.path && <path d={brandLogos[brand].path} />}
              </svg>
              {brand}
            </div>
          ))}
        </div>

        <Reveal variant="fade" className="text-center mt-8">
          <p className="text-xs text-muted-foreground/70">
            Contact the workshop to confirm support for your model.
          </p>
        </Reveal>
      </div>
    </section>
  );
};

export default BrandPartners;
