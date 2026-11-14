import fs from 'node:fs';
import sharp from 'sharp';

const dir = 'src/assets/hero';
const pairs = [
  ['garage-grounded-wide-1600.webp', 'garage-grounded-wide-1600-blur.webp'],
  ['garage-daylight-wide-1600.webp', 'garage-daylight-wide-1600-blur.webp'],
];

for (const [src, out] of pairs) {
  const meta = await sharp(`${dir}/${src}`).metadata();
  const w = meta.width, h = meta.height;
  // Slight overscale before blurring so the softened edge never shows as a fringe.
  const big = await sharp(`${dir}/${src}`).resize({ width: Math.round(w * 1.1), height: Math.round(h * 1.1), fit: 'fill' })
    .blur(20).toBuffer();
  await sharp(big)
    .extract({ left: Math.round(w * 0.05), top: Math.round(h * 0.05), width: w, height: h })
    .webp({ quality: 82 })
    .toFile(`${dir}/${out}`);
  console.log(out, Math.round(fs.statSync(`${dir}/${out}`).size / 1024) + 'KB', `${w}x${h}`);
}
