/** Public HTTPS location supplied by the deployment. */
export function publicSiteUrl(value?: string): string | undefined {
  if (!value) return;
  try {
    const url = new URL(value);
    if (url.protocol !== 'https:' || url.username || url.password || url.search || url.hash ||
        !url.hostname.includes('.') || url.hostname.endsWith('.localhost') || url.hostname === '127.0.0.1') return;
    return url.href.endsWith('/') ? url.href : url.href + '/';
  } catch {
    return;
  }
}

/** AdSense publisher id (ca-pub-0000000000000000), or undefined when unset/invalid. */
export const adsensePublisherId = (value?: string) => value && /^ca-pub-\d{16}$/.test(value) ? value : undefined;
export const adsTxt = (id: string) => `google.com, ${id.replace('ca-', '')}, DIRECT, f08c47fec0942fa0
`;
export const adsenseMeta = (id?: string) => id ? `<meta name="google-adsense-account" content="${id}">` : '';

export const pages = {
  '/': {
    label: 'Home',
    heading: 'Multi-brand car workshop in Anantapur',
    title: 'Toli Motors | Multi-Brand Car Workshop in Anantapur',
    description: 'Toli Motors offers multi-brand car servicing, repairs, detailing and spare parts in Anantapur, Andhra Pradesh. Explore services or request an appointment.',
  },
  '/enquire-now': {
    label: 'Service Request',
    heading: 'Service request',
    title: 'Request Car Service in Anantapur | Toli Motors',
    description: 'Tell Toli Motors about your vehicle and the service you need. Prepare an enquiry and review it before sending it to our Anantapur workshop on WhatsApp.',
  },
  '/privacy-policy': {
    label: 'Privacy Policy',
    heading: 'Privacy Policy',
    title: 'Privacy Policy | Toli Motors',
    description: 'Learn what information Toli Motors uses when you prepare an enquiry, open WhatsApp, use the local assistant or see advertising.',
  },
  '/terms-and-conditions': {
    label: 'Terms & Conditions',
    heading: 'Terms & Conditions',
    title: 'Terms & Conditions | Toli Motors',
    description: 'Read the terms for using the Toli Motors website and how our Anantapur workshop handles estimates, enquiries and appointment confirmation.',
  },
  '/cookie-policy': {
    label: 'Cookie Policy',
    heading: 'Cookie Policy',
    title: 'Cookie Policy | Toli Motors',
    description: 'Find out how this website stores preferences, how advertising cookies work and how to manage your consent choices.',
  },
} as const;

const notFound = {
  label: 'Page not found',
  heading: 'Page not found',
  title: 'Page Not Found | Toli Motors',
  description: 'Find your way back to Toli Motors, browse workshop services or start a service request.',
};

export type PagePath = keyof typeof pages;
export function pagePath(path: string): PagePath | undefined {
  const normalized = path.replace(/\/$/, '') || '/';
  return Object.prototype.hasOwnProperty.call(pages, normalized) ? normalized as PagePath : undefined;
}

export const pageInfo = (path?: PagePath) => path ? pages[path] : notFound;
export const pageHref = (base: string, path: PagePath) => base + (path === '/' ? '' : path.slice(1) + '/');
export const escapeHtml = (value: string) => value.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

export function pageMetadata(path: PagePath | undefined, site?: string) {
  const { title, description } = pageInfo(path);
  const url = path && site ? pageHref(site, path) : undefined;
  const tags = [
    ['name', 'description', description],
    ['name', 'robots', url ? 'index, follow' : 'noindex, follow'],
    ['property', 'og:type', 'website'],
    ['property', 'og:site_name', 'Toli Motors'],
    ['property', 'og:title', title],
    ['property', 'og:description', description],
    ['name', 'twitter:card', 'summary_large_image'],
    ['name', 'twitter:title', title],
    ['name', 'twitter:description', description],
  ];
  if (url && site) tags.push(
    ['property', 'og:url', url],
    ['property', 'og:image', site + 'social-share.jpg'],
    ['property', 'og:image:width', '1200'],
    ['property', 'og:image:height', '630'],
    ['property', 'og:image:alt', 'Toli Motors workshop and service bays in Anantapur'],
    ['name', 'twitter:image', site + 'social-share.jpg'],
    ['name', 'twitter:image:alt', 'Toli Motors workshop and service bays in Anantapur'],
  );
  const schema = path === '/' ? {
    '@context': 'https://schema.org',
    '@type': 'AutoRepair',
    name: 'Toli Motors',
    telephone: '+91-8074946335',
    email: 'tolimotorsatp@gmail.com',
    address: {
      '@type': 'PostalAddress', streetAddress: '6-2-806, Ram Nagar, Kovur Nagar, opposite DMart',
      addressLocality: 'Anantapur', addressRegion: 'Andhra Pradesh', postalCode: '515004', addressCountry: 'IN',
    },
    ...(site && { '@id': site + '#workshop', url: site, image: site + 'social-share.jpg' }),
  } : path && url && site ? {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Home', item: site },
      { '@type': 'ListItem', position: 2, name: pages[path].label, item: url },
    ],
  } : undefined;
  return [
    ...tags.map(([type, key, value]) => `<meta data-page-seo ${type}="${key}" content="${escapeHtml(value)}">`),
    url && `<link data-page-seo rel="canonical" href="${escapeHtml(url)}">`,
    schema && `<script data-page-seo type="application/ld+json">${JSON.stringify(schema).replace(/</g, '\\u003c')}</script>`,
  ].filter(Boolean).join('\n');
}
