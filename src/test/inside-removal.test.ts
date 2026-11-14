import {expect,it} from 'vitest';
import {readFileSync,existsSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {experienceChapters} from '@/lib/experience-navigation';
it('connects the section stack directly to Gallery without a removed workshop mount',()=>{
 const page=readFileSync('src/pages/Index.tsx','utf8');
 expect(page).toMatch(/<\/SectionStack>\s*<\/Suspense>\s*<Gallery/);
 expect(page).not.toMatch(/Facility|inside-toli/);
 expect(readFileSync('src/components/journey/JourneyProvider.tsx','utf8')).not.toMatch(/facility|workshop\//i);
 expect(existsSync('public/models/toli-workshop-web-v2.glb')).toBe(false);
});
it('retains the six real chapter destinations and bronze navigation',()=>{
 expect(experienceChapters.map(c=>c.id)).toEqual(['hero','services','process','trust','booking','connect']);
 expect(readFileSync('src/components/journey/experience.css','utf8')).toContain('--bronze-main');
});
it('preserves approved artwork and retained static assets',()=>{
 const baseline=JSON.parse(readFileSync('src/test/fixtures/separation-protected.json','utf8')) as Record<string,string>;
 for(const [file,hash] of Object.entries(baseline))expect(createHash('sha256').update(readFileSync(file)).digest('hex'),file).toBe(hash);
});
