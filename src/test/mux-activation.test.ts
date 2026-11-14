import { describe, expect, it } from 'vitest';
import { createMuxPresentation, isCodedMuxDock } from '@/lib/mux-presentation';

describe('inactive V04 presentation preserved for rollback', () => {
  it('retains the original section guard for an explicit future rollback', () => {
    for (const mode of ['hero', 'services', 'studio', undefined]) expect(isCodedMuxDock(mode)).toBe(false);
    for (const mode of ['process', 'completion']) expect(isCodedMuxDock(mode)).toBe(true);
  });
  it('shares the latest exterior-detail geometry and fits both cameras at every requested viewport', () => {
    const view = createMuxPresentation(), root = view.scene.children[0];
    expect(root.getObjectByName('number-plates')?.children).toHaveLength(2);
    expect(root.getObjectByName('mirrors')?.children).toHaveLength(2);
    expect(root.getObjectByName('doors')?.children.flatMap(side=>side.children)).toHaveLength(4);
    expect(root.getObjectByName('handles')?.children.flatMap(side=>side.children)).toHaveLength(4);
    for (const [w,h] of [[320,568],[360,800],[390,844],[412,915],[768,1024],[1366,768],[1920,1080]]) {
      for (const mode of ['process','completion'] as const) for (const light of [false,true]) {
        view.update(mode,w/h,light); expect(view.frameFits()).toBe(true); expect(view.scene.children[0]).toBe(root);
        expect(Math.sign(view.camera.position.x)).toBe(mode==='process'?-1:1);
      }
    }
    view.dispose(); expect(view.scene.children).toHaveLength(0);
  });
});
