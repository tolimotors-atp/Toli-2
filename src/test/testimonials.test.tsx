import { render, screen } from '@testing-library/react';
import { expect, it } from 'vitest';
import Testimonials from '@/components/Testimonials';
import { GOOGLE_REVIEWS_URL } from '@/lib/google-reviews';

it('renders all seven verified excerpts in a keyboard-focusable rail with the Google link', () => {
  render(<Testimonials />);
  const rail = screen.getByRole('list', { name: 'Google review excerpts' });
  expect(rail).toHaveAttribute('tabindex', '0');
  expect(screen.getAllByRole('listitem')).toHaveLength(7);
  expect(screen.getByRole('button', { name: 'Scroll reviews right' })).toHaveAttribute('aria-controls', rail.id);
  expect(screen.getByRole('link', { name: 'View reviews on Google' })).toHaveAttribute('href', GOOGLE_REVIEWS_URL);
  expect(screen.getByText(/83 reviews/)).toHaveTextContent('4.1 out of 5');
});

it.each([GOOGLE_REVIEWS_URL, null])('keeps the review section visible without excerpts (%s)', reviewUrl => {
  render(<Testimonials stories={[]} reviewUrl={reviewUrl} />);
  expect(screen.getByRole('region', { name: 'Customer stories' })).toBeVisible();
  expect(screen.getByRole('heading', { name: 'Google Reviews' })).toBeVisible();
  expect(screen.queryByRole('img')).toBeNull();
  expect(screen.queryByRole('button', { name: 'Scroll reviews right' })).toBeNull();
  const link = screen.queryByRole('link', { name: 'View reviews on Google' });
  if (reviewUrl) expect(link).toHaveAttribute('href', reviewUrl);
  else expect(link).toBeNull();
});
