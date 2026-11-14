import {afterEach,expect,it,vi} from 'vitest';
import {cleanup,fireEvent,render,screen} from '@testing-library/react';
import App from '@/App';
vi.mock('@/pages/Index',()=>({default:()=> <h1>Traditional homepage</h1>}));
afterEach(()=>{cleanup();vi.restoreAllMocks();});
it('opens the traditional website at root',async()=>{history.replaceState(null,'','/');render(<App/>);expect(await screen.findByRole('heading',{name:'Traditional homepage'})).toBeInTheDocument();expect(document.querySelector('.spatial-experience')).toBeNull();});
it('does not mount the removed experimental showroom deep link',async()=>{history.replaceState(null,'','/3d-production-preview/');render(<App/>);expect(await screen.findByRole('heading',{name:'Page not found'})).toBeInTheDocument();expect(document.querySelector('canvas')).toBeNull();});

it('returns from a direct service request when scrollTo returns a promise', async () => {
  vi.spyOn(window, 'scrollTo').mockImplementation(() => Promise.resolve());
  history.replaceState(null, '', '/enquire-now/');
  render(<App />);
  const breadcrumb = await screen.findByRole('navigation', { name: 'Breadcrumb' });
  const home = breadcrumb.querySelector('a');
  expect(home).toHaveAttribute('href', '/');
  if (home) fireEvent.click(home);
  expect(await screen.findByRole('heading', { name: 'Traditional homepage' })).toBeInTheDocument();
});
