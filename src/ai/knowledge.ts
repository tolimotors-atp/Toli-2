import { services } from '@/lib/service-catalog';
// Source: existing service-catalog.ts and Contact.tsx. No inferred hours/prices.
export const knowledge = services.map(({title,desc}) => ({title,desc}));
export const contact = 'Call +91-8074946335 or +91-9908303888, or email tolimotorsatp@gmail.com.';
export const about = 'TOLI Motors is a multi-brand car workshop in Anantapur, Andhra Pradesh, providing vehicle servicing, repairs and care. Our team confirms the service scope and arrangements for your vehicle.';
export const location = '6-2-806, Ram Nagar, Kovur Nagar, opposite DMart, Anantapur, Andhra Pradesh 515004.';
export const greeting = 'Hi. I can help you find TOLI Motors services or start a service request. What do you need help with?';
