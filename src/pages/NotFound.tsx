import { Link } from 'react-router-dom';
import Breadcrumbs from '@/components/Breadcrumbs';
import ToliLogoPill from '@/components/ToliLogoPill';

export default function NotFound() {
  return (
    <main className="toli-content-page min-h-dvh bg-background px-6 py-12">
      <div className="mx-auto max-w-3xl">
        <Link to="/" aria-label="Toli Motors home"><ToliLogoPill size="compact" /></Link>
        <div className="mt-10"><Breadcrumbs label="Page not found" /></div>
        <p className="text-sm font-semibold text-primary">404</p>
        <h1 className="my-4 text-4xl font-bold">Page not found</h1>
        <p className="mb-6 text-muted-foreground">This address doesn’t lead to a Toli Motors page.</p>
        <nav aria-label="Workshop links" className="flex flex-wrap gap-5 underline underline-offset-4">
          <Link to="/">Toli Motors home</Link>
          <a href={import.meta.env.BASE_URL + '#services'}>Browse workshop services</a>
          <Link to="/enquire-now/">Request service</Link>
        </nav>
      </div>
    </main>
  );
}
