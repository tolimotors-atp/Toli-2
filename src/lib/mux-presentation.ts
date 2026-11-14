import * as T from 'three';
import { createMux } from '@/components/three/mux/MuxVehicle';
import { createContactFalloff } from './premium-car/studio-environment';

export const isCodedMuxDock = (mode: string | undefined): mode is 'process' | 'completion' => mode === 'process' || mode === 'completion';

/** One V04 resource set, rendered only in Sections 03/05 by the existing renderer. */
export function createMuxPresentation() {
  const vehicle = createMux(), scene = new T.Scene();
  vehicle.root.rotation.x = -Math.PI / 2;
  scene.add(vehicle.root);
  const camera = new T.PerspectiveCamera(34, 1, .1, 60);
  const fill = new T.HemisphereLight(0xffffff, 0x4d5059, 2.1);
  const key = new T.DirectionalLight(0xffffff, 3.2); key.position.set(-3, 6, 4);
  const rim = new T.DirectionalLight(0xf0f2fa, 2); rim.position.set(4, 3, -3);
  scene.add(fill, key, rim);
  const map = createContactFalloff();
  const floorGeometry = new T.PlaneGeometry(5.5, 2.8);
  const floorMaterial = new T.MeshBasicMaterial({ color: 0x101114, map, transparent: true, opacity: .5, depthWrite: false });
  const floor = new T.Mesh(floorGeometry, floorMaterial); floor.rotation.x = -Math.PI / 2; floor.position.y = .002; scene.add(floor);
  vehicle.root.updateMatrixWorld(true);
  const points: T.Vector3[] = [];
  vehicle.root.traverseVisible(object => {
    if (!(object instanceof T.Mesh)) return;
    const position = object.geometry.getAttribute('position');
    for (let i = 0; i < position.count; i++) points.push(new T.Vector3().fromBufferAttribute(position, i).applyMatrix4(object.matrixWorld));
  });
  const bounds = new T.Box3().setFromPoints(points);
  let framing = '', fits = false;
  const target = bounds.getCenter(new T.Vector3());
  function update(mode: 'process' | 'completion', aspect: number, light: boolean) {
    fill.intensity = light ? 2 : 2.3; floorMaterial.opacity = light ? .42 : .65;
    const next = mode + ':' + aspect;
    if (framing === next) return;
    framing = next;
    camera.aspect = aspect; camera.updateProjectionMatrix();
    const direction = new T.Vector3(mode === 'completion' ? 6 : -6, 2.7, 4.6).normalize();
    const right = new T.Vector3().crossVectors(direction, camera.up).normalize();
    const up = new T.Vector3().crossVectors(right, direction).normalize();
    const tan = Math.tan(T.MathUtils.degToRad(camera.fov / 2));
    let distance = 0;
    // Fit visible surfaces, including mirrors and plates, without the empty box corners.
    for (const point of points) {
      const offset = point.clone().sub(target);
      distance = Math.max(distance, offset.dot(direction) + Math.max(Math.abs(offset.dot(right)) / (tan * aspect), Math.abs(offset.dot(up)) / tan) * 1.08);
    }
    camera.position.copy(target).addScaledVector(direction, distance); camera.lookAt(target); camera.updateMatrixWorld();
    fits = points.every(point => { const p = point.clone().project(camera); return Math.abs(p.x) < 1 && Math.abs(p.y) < 1; });
  }
  return { scene, camera, update,
    frameFits: () => fits,
    dispose() { vehicle.dispose(); map.dispose(); floorGeometry.dispose(); floorMaterial.dispose(); scene.clear(); }
  };
}
