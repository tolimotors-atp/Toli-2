import {afterEach,expect,it,vi} from 'vitest';
import {cleanup,fireEvent,render,screen} from '@testing-library/react';
import {MemoryRouter} from 'react-router-dom';
import {advertising,canRequestAds,loadAdvertisingScript} from '@/lib/advertising';
import GalleryImage from '@/components/GalleryImage';
import Contact from '@/components/Contact';
vi.mock('@/hooks/use-section-entrance',()=>({useSectionEntrance:()=>{}}));
vi.mock('@/components/motion/Reveal',()=>({default:({children}:{children:React.ReactNode})=><>{children}</>}));
afterEach(()=>{cleanup();vi.restoreAllMocks();});
it('makes no advertising request with missing configuration, consent or authorization',async()=>{
 const append=vi.spyOn(document.head,'append');
 expect(canRequestAds(advertising,'after-gallery',true)).toBe(false);
 expect(await loadAdvertisingScript(advertising,'after-gallery',true)).toBe(false);
 const configured={enabled:true,liveAdsAuthorized:false,publisherId:'ca-pub-1234567890123456',units:{'after-gallery':'1234567890','before-footer':'1234567890'}};
 expect(canRequestAds(configured,'after-gallery',true)).toBe(false);
 expect(canRequestAds({...configured,liveAdsAuthorized:true},'after-gallery',false)).toBe(false);
 expect(append).not.toHaveBeenCalled();
});
it('reserves a gallery slot without rendering a broken img before its deferred source exists',()=>{
 const {rerender}=render(<GalleryImage alt="Workshop" width={600} height={400}/>);
 expect(document.querySelector('img')).toBeNull();
 rerender(<GalleryImage alt="Workshop" width={600} height={400} src="one.webp"/>);
 fireEvent.error(screen.getByAltText('Workshop'));expect(screen.getByText('Photo unavailable')).toBeInTheDocument();
 rerender(<GalleryImage alt="Workshop" width={600} height={400} src="two.webp"/>);
 expect(screen.getByAltText('Workshop')).toHaveAttribute('src','two.webp');
});
it('keeps contact usable with blocked storage and allows map consent to be revoked',()=>{
 vi.spyOn(Storage.prototype,'getItem').mockImplementation(()=>{throw new Error('blocked');});
 vi.spyOn(Storage.prototype,'setItem').mockImplementation(()=>{throw new Error('blocked');});
 vi.spyOn(Storage.prototype,'removeItem').mockImplementation(()=>{throw new Error('blocked');});
 render(<MemoryRouter><Contact/></MemoryRouter>);
 expect(document.querySelector('iframe')).toBeNull();fireEvent.click(screen.getByRole('button',{name:'LOAD MAP'}));
 expect(screen.getByTitle('Toli Motors location on Google Maps')).toBeInTheDocument();
 fireEvent.click(screen.getByRole('button',{name:'REMOVE MAP CONSENT'}));expect(document.querySelector('iframe')).toBeNull();
});
