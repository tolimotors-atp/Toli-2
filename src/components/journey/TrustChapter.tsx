import { lazy, Suspense, type SyntheticEvent } from 'react';
const About=lazy(()=>import('@/components/About'));
const Stats=lazy(()=>import('@/components/Stats'));
const BrandPartners=lazy(()=>import('@/components/BrandPartners'));
const WhyUs=lazy(()=>import('@/components/WhyUs'));
const ServiceArea=lazy(()=>import('@/components/ServiceArea'));
/** These two panels are always open; the summary is a label, not a toggle. */
const stayOpen=(event:SyntheticEvent<HTMLDetailsElement>)=>{const panel=event.currentTarget;if(!panel.open)panel.open=true;};
export default function TrustChapter(){return <section id="trust" className="experience-chapter trust-chapter" data-experience-chapter="trust" aria-labelledby="trust-title"><header className="chapter-heading"><p className="system-label">04 / TOLI MOTORS</p><h2 id="trust-title">Built on care.<br/>Backed by people.</h2><p>Explore the workshop, the team’s approach and how we pick up your car.</p></header><div className="trust-index"><Suspense fallback={<p>Loading workshop information…</p>}><details open onToggle={stayOpen} data-always-open><summary>01 / The workshop & our approach <span>↗</span></summary><About/><Stats/><WhyUs/></details><details open onToggle={stayOpen} data-always-open><summary>02 / Multi-brand care & doorstep pickup <span>↗</span></summary><BrandPartners/><ServiceArea/></details></Suspense></div></section>;}
