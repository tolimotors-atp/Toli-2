import { afterEach, expect, it, vi } from 'vitest';
import { cleanup, render, screen, fireEvent, within, waitFor } from '@testing-library/react';
import { galleryCounter } from '@/lib/gallery-images';
import { featuredGalleryImages, galleryImages } from '@/lib/gallery-images';
import Gallery from '@/components/Gallery';
afterEach(()=>{cleanup();vi.unstubAllGlobals();});
it('formats the actual image count',()=>{expect(galleryCounter(0,16)).toBe('01 / 16');expect(galleryCounter(15,16)).toBe('16 / 16');});
it('represents all real images once, in intentional logical order with intrinsic dimensions and descriptive alts',()=>{
 expect(galleryImages).toHaveLength(16);expect(new Set(galleryImages.map(image=>image.src)).size).toBe(16);
 const {container}=render(<Gallery/>);const photos=container.querySelectorAll<HTMLButtonElement>('.editorial-photo');
 expect(photos).toHaveLength(6);
 featuredGalleryImages.forEach((image,index)=>{const img=photos[index].querySelector('img')!;expect(img.alt).toBe(image.alt);expect(img.alt.length).toBeGreaterThan(40);expect(img).toHaveAttribute('width',String(image.width));expect(img).toHaveAttribute('height',String(image.height));expect(img).toHaveAttribute('loading','lazy');});
 expect(screen.getAllByRole('button',{name:/^View Toli Motors gallery image/})).toHaveLength(6);
 expect(container.querySelector('[aria-hidden=true] button')).toBeNull();
});
it('keeps the six featured triggers available in reduced motion',()=>{
 vi.stubGlobal('matchMedia',()=>({matches:true,addEventListener:vi.fn(),removeEventListener:vi.fn()}));
 const {container}=render(<Gallery/>);expect(container.querySelector('.gallery-deck-shell')).toBeNull();
 expect(screen.getAllByRole('button',{name:/^View Toli Motors gallery image/})).toHaveLength(6);
 container.querySelectorAll('.editorial-photo').forEach(button=>expect(button).not.toHaveAttribute('tabindex','-1'));
});
it('does not load the editorial images at Hero entry before the Gallery approaches',()=>{
 vi.stubGlobal('IntersectionObserver',class{observe(){}disconnect(){}});
 const {container}=render(<Gallery/>);container.querySelectorAll('.editorial-photo img').forEach(img=>expect(img).not.toHaveAttribute('src'));
});
it.each([0,1,2,3])('opens the correct editorial slot %s with ordered navigation and focus return',index=>{
 const {container}=render(<Gallery/>);const trigger=container.querySelectorAll<HTMLButtonElement>('.editorial-photo')[index];trigger.focus();fireEvent.click(trigger);
 const dialog=screen.getByRole('dialog');expect(within(dialog).getByRole('img')).toHaveAttribute('alt',galleryImages[index].alt);
 fireEvent.keyDown(window,{key:'ArrowRight'});expect(within(dialog).getByRole('img')).toHaveAttribute('alt',galleryImages[index+1].alt);
 fireEvent.keyDown(window,{key:'ArrowLeft'});expect(within(dialog).getByRole('img')).toHaveAttribute('alt',galleryImages[index].alt);
 fireEvent.keyDown(window,{key:'Escape'});expect(screen.queryByRole('dialog')).toBeNull();expect(trigger).toHaveFocus();
});

it('offers smaller responsive thumbnails while preserving originals for the lightbox',()=>{
 vi.stubGlobal('IntersectionObserver',undefined);const {container}=render(<Gallery/>);
 for(const image of galleryImages){expect(image.srcSet).toContain('480w');expect(image.srcSet).toContain(`${image.width}w`);}
 const thumbnail=container.querySelector('.editorial-photo img')!;expect(thumbnail).toHaveAttribute('srcset',galleryImages[0].srcSet);
 fireEvent.click(screen.getByRole('button',{name:`View ${galleryImages[0].alt}`}));
 const full=within(screen.getByRole('dialog')).getByRole('img');expect(full).toHaveAttribute('src',galleryImages[0].src);expect(full).not.toHaveAttribute('srcset');
});

it('waits for the real homepage stack before measuring Gallery proximity',async()=>{
 const observe=vi.fn();vi.stubGlobal('IntersectionObserver',class{observe=observe;disconnect(){}});
 const {container}=render(<main className="phase9-experience"><div className="stack-placeholder"/><Gallery/></main>);
 expect(observe).not.toHaveBeenCalled();expect(container.querySelector('.editorial-photo img')).toBeNull();expect(container.querySelector('.gallery-image-pending')).toBeInTheDocument();
 const stack=document.createElement('div');stack.dataset.sectionStack='';container.querySelector('main')!.prepend(stack);
 await waitFor(()=>expect(observe).toHaveBeenCalledOnce());expect(container.querySelector('.editorial-photo img')).toBeNull();expect(container.querySelector('.gallery-image-pending')).toBeInTheDocument();
});

it('mounts the complete collection only on request and restores both focus transitions', () => {
 const { container } = render(<Gallery />);
 const seeMore = screen.getByRole('button', { name: 'See more' });
 expect(container.querySelectorAll('.editorial-photo')).toHaveLength(6);
 expect(document.querySelector('.gallery-collection')).toBeNull();

 fireEvent.click(seeMore);
 const collection = screen.getByRole('dialog', { name: 'All workshop photos' });
 const buttons = within(collection).getAllByRole('button', { name: /^View Toli Motors gallery image/ });
 expect(buttons).toHaveLength(galleryImages.length);
 expect(within(collection).getByRole('button', { name: 'Close gallery' })).toHaveFocus();
 expect(within(collection).getAllByRole('img').every(img => img.getAttribute('loading') === 'lazy')).toBe(true);

 const last = buttons.at(-1)!;
 fireEvent.click(last);
 const preview = screen.getByRole('dialog', { name: 'Workshop image preview' });
 expect(preview).toBe(collection);
 expect(within(preview).getByRole('img')).toHaveAttribute('src', galleryImages.at(-1)!.src);
 fireEvent.keyDown(window, { key: 'ArrowRight' });
 expect(within(preview).getByRole('img')).toHaveAttribute('src', galleryImages[0].src);
 fireEvent.click(within(preview).getByRole('button', { name: 'All photos' }));
 expect(last).toHaveFocus();
 fireEvent.keyDown(window, { key: 'Escape' });
 expect(screen.queryByRole('dialog')).toBeNull();
 expect(seeMore).toHaveFocus();
});

it('keeps featured preview navigation within the curated set', () => {
 render(<Gallery />);
 fireEvent.click(screen.getByRole('button', { name: `View ${featuredGalleryImages.at(-1)!.alt}` }));
 fireEvent.keyDown(window, { key: 'ArrowRight' });
 expect(within(screen.getByRole('dialog')).getByRole('img')).toHaveAttribute('src', featuredGalleryImages[0].src);
});
