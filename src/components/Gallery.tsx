import { createPortal } from 'react-dom';
import { useCallback, useEffect, useRef, useState } from 'react';
import { ArrowLeft, ArrowUpRight, ChevronLeft, ChevronRight, X } from 'lucide-react';
import GalleryImage from './GalleryImage';
import { featuredGalleryImages, galleryCounter, galleryImages } from '@/lib/gallery-images';
import './gallery-editorial.css';

type Photo = (typeof galleryImages)[number];

function Thumbnail({ photo, sizes, ready }: { photo: Photo; sizes: string; ready: boolean }) {
  return <GalleryImage src={ready ? photo.src : undefined} srcSet={ready ? photo.srcSet : undefined}
    sizes={sizes} alt={photo.alt} width={photo.width} height={photo.height} loading="lazy" decoding="async" />;
}

export default function Gallery() {
  const [near, setNear] = useState(false);
  const [viewer, setViewer] = useState<'featured' | 'collection' | null>(null);
  const [selected, setSelected] = useState<number | null>(null);
  const gallery = useRef<HTMLElement>(null);
  const dialog = useRef<HTMLDivElement>(null);
  const closeButton = useRef<HTMLButtonElement>(null);
  const opener = useRef<HTMLButtonElement>(null);
  const collectionOpener = useRef<HTMLButtonElement>(null);
  const photos = viewer === 'collection' ? galleryImages : featuredGalleryImages;
  const isOpen = viewer !== null;
  const photo = selected === null ? undefined : photos[selected];

  useEffect(() => {
    if (typeof IntersectionObserver === 'undefined') { setNear(true); return; }
    const observer = new IntersectionObserver(entries => {
      if (entries.some(entry => entry.isIntersecting)) {
        setNear(true);
        observer.disconnect();
      }
    }, { rootMargin: '600px' });
    const node = gallery.current;
    const main = node?.closest('.phase9-experience');
    // The Suspense placeholder temporarily puts Gallery close to the Hero.
    const ready = () => !main || !!main.querySelector('[data-section-stack]');
    let registration: MutationObserver | undefined;
    if (node) {
      if (ready()) observer.observe(node);
      else {
        registration = new MutationObserver(() => {
          if (ready()) {
            registration?.disconnect();
            observer.observe(node);
          }
        });
        registration.observe(main!, { childList: true, subtree: true });
      }
    }
    return () => { registration?.disconnect(); observer.disconnect(); };
  }, []);

  useEffect(() => {
    if (!isOpen) return;
    const trigger = opener.current;
    const previousOverflow = document.body.style.overflow;
    const previousGutter = document.documentElement.style.scrollbarGutter;
    document.body.style.overflow = 'hidden';
    document.documentElement.style.scrollbarGutter = 'stable';
    const keepFocus = (event: FocusEvent) => {
      if (!dialog.current?.contains(event.target as Node)) closeButton.current?.focus();
    };
    document.addEventListener('focusin', keepFocus);
    return () => {
      document.removeEventListener('focusin', keepFocus);
      document.body.style.overflow = previousOverflow;
      document.documentElement.style.scrollbarGutter = previousGutter;
      if (trigger?.isConnected) trigger.focus({ preventScroll: true });
    };
  }, [isOpen]);

  const previewOpen = photo !== undefined;
  useEffect(() => {
    if (!isOpen) return;
    if (!previewOpen && collectionOpener.current) {
      collectionOpener.current.focus({ preventScroll: true });
      collectionOpener.current = null;
    } else closeButton.current?.focus();
  }, [isOpen, previewOpen]);

  const close = useCallback(() => {
    collectionOpener.current = null;
    setViewer(null);
    setSelected(null);
  }, []);
  const move = (step: number) => {
    setSelected(index => index === null ? null : (index + step + photos.length) % photos.length);
  };

  useEffect(() => {
    if (!isOpen) return;
    const keyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        event.preventDefault();
        close();
      } else if (previewOpen && (event.key === 'ArrowLeft' || event.key === 'ArrowRight')) {
        event.preventDefault();
        const step = event.key === 'ArrowLeft' ? -1 : 1;
        setSelected(index => index === null ? null : (index + step + photos.length) % photos.length);
      } else if (event.key === 'Tab') {
        const controls = Array.from(dialog.current?.querySelectorAll('button') ?? []).filter(button => !button.closest('[hidden]'));
        const first = controls[0];
        const last = controls.at(-1);
        if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last?.focus(); }
        else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus(); }
      }
    };
    window.addEventListener('keydown', keyDown);
    return () => window.removeEventListener('keydown', keyDown);
  }, [isOpen, previewOpen, photos.length, close]);

  return (
    <section ref={gallery} id="gallery" className="journey-section journey-gallery editorial-gallery"
      data-journey-section="gallery" aria-labelledby="gallery-title">
      <header className="editorial-heading"><h2 id="gallery-title">Workshop gallery</h2></header>
      <div className="editorial-featured" aria-label="Featured workshop photographs">
        {featuredGalleryImages.map((image, index) => (
          <figure className="editorial-figure" key={image.file}>
            <button type="button" className="editorial-photo" aria-label={`View ${image.alt}`} aria-haspopup="dialog"
              onClick={event => { opener.current = event.currentTarget; setViewer('featured'); setSelected(index); }}>
              <Thumbnail photo={image} ready={near} sizes={
                index === 0 ? '(max-width: 599px) 92vw, 50vw'
                  : index === 1 ? '(max-width: 599px) 46vw, 38vw'
                    : index === 5 ? '(max-width: 599px) 92vw, (max-width: 900px) 46vw, 22vw'
                      : '(max-width: 900px) 46vw, 22vw'
              } />
            </button>
          </figure>
        ))}
      </div>
      <div className="gallery-actions">
        <button type="button" className="gallery-see-more" aria-haspopup="dialog"
          onClick={event => { opener.current = event.currentTarget; setViewer('collection'); }}>
          See more <ArrowUpRight size={18} aria-hidden="true" />
        </button>
        <a className="gallery-reviews-link" href="#customer-stories">Customer stories <ArrowUpRight size={16} aria-hidden="true" /></a>
      </div>

      {isOpen && createPortal(
        <div ref={dialog} id="lightbox-dialog" className="gallery-dialog" role="dialog" aria-modal="true"
          aria-label={previewOpen ? 'Workshop image preview' : 'All workshop photos'}
          onClick={event => { if (event.target === event.currentTarget) close(); }}>
          <div className="gallery-viewer">
            <header className="gallery-viewer-header">
              {previewOpen && viewer === 'collection'
                ? <button type="button" className="gallery-back" onClick={() => setSelected(null)}><ArrowLeft size={18} aria-hidden="true" /> All photos</button>
                : <h2>{previewOpen ? 'Workshop photo' : 'All workshop photos'}</h2>}
              <button ref={closeButton} type="button" className="gallery-icon-button"
                aria-label={previewOpen ? 'Close image preview' : 'Close gallery'} onClick={close}><X size={22} aria-hidden="true" /></button>
            </header>
            {viewer === 'collection' && (
              <div className="gallery-collection" hidden={previewOpen}>
                {galleryImages.map((image, index) => (
                  <button type="button" className="editorial-photo" key={image.file}
                    data-portrait={image.width < image.height || undefined} aria-label={`View ${image.alt}`}
                    onClick={event => { collectionOpener.current = event.currentTarget; setSelected(index); }}>
                    <Thumbnail photo={image} ready sizes="(max-width: 599px) 46vw, (max-width: 900px) 30vw, min(26vw, 360px)" />
                  </button>
                ))}
              </div>
            )}
            {photo && (
              <>
                <figure className="gallery-preview">
                  <GalleryImage key={photo.file} src={photo.src} alt={photo.alt} width={photo.width} height={photo.height} draggable={false} />
                  <figcaption>{photo.caption}</figcaption>
                </figure>
                <footer className="gallery-preview-controls">
                  <button type="button" className="gallery-icon-button" aria-label="Previous image" onClick={() => move(-1)}><ChevronLeft size={22} aria-hidden="true" /></button>
                  <span aria-live="polite">{galleryCounter(selected!, photos.length)}</span>
                  <button type="button" className="gallery-icon-button" aria-label="Next image" onClick={() => move(1)}><ChevronRight size={22} aria-hidden="true" /></button>
                </footer>
              </>
            )}
          </div>
        </div>, document.body
      )}
    </section>
  );
}
