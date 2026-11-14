import { lazy, Suspense, useEffect } from 'react';
import { BrowserRouter, Route, Routes, useLocation } from "react-router-dom";
import { Toaster as Sonner } from "@/components/ui/sonner";
import ServiceRequestDialogProvider from "@/components/ServiceRequestDialog";
const ServiceRequest = lazy(() => import("./pages/ServiceRequest"));
import { SERVICE_REQUEST_ROUTE } from "@/lib/service-request";
const Index = lazy(() => import('./pages/Index'));
const PrivacyPolicy = lazy(() => import("./pages/PrivacyPolicy"));
const TermsAndConditions = lazy(() => import("./pages/TermsAndConditions"));
const CookiePolicy = lazy(() => import("./pages/CookiePolicy"));
import NotFound from "./pages/NotFound.tsx";
import PageTransition from "@/components/motion/PageTransition";

import { pageInfo, pageMetadata, pagePath, publicSiteUrl } from '../seo.config';

const publicUrl = publicSiteUrl(import.meta.env.VITE_SITE_URL);

function RouteMetadata() {
  const { pathname } = useLocation();
  useEffect(() => {
    const path = pagePath(pathname);
    document.title = pageInfo(path).title;
    document.head.querySelectorAll('[data-page-seo]').forEach(node => node.remove());
    document.head.insertAdjacentHTML('beforeend', pageMetadata(path, publicUrl));
  }, [pathname]);
  return null;
}

const App = () => (
  <BrowserRouter basename={import.meta.env.BASE_URL} future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
    <RouteMetadata />
    <Sonner />
    <ServiceRequestDialogProvider>
      <PageTransition>
        <Suspense fallback={<div role="status" className="p-8">Loading page…</div>}>
          <Routes>
            <Route path="/" element={<Index />} />
            <Route path={SERVICE_REQUEST_ROUTE} element={<ServiceRequest />} />
            <Route path="/privacy-policy" element={<PrivacyPolicy />} />
            <Route path="/terms-and-conditions" element={<TermsAndConditions />} />
            <Route path="/cookie-policy" element={<CookiePolicy />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </Suspense>
      </PageTransition>
    </ServiceRequestDialogProvider>
  </BrowserRouter>
);

export default App;
