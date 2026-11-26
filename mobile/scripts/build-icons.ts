// Renders the app icons from the Pet's own geometry (petCore.ts): the happy vapor Pet on the
// teal of its chat circle. Run with `bun scripts/build-icons.ts` from mobile/; needs rsvg-convert.
// Writes assets/images/{icon,android-icon-*,splash-icon,favicon}.png.
import { execFileSync } from 'node:child_process';
import { mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

import { brand } from '../src/ui/theme/tokens';
import { PET_PRESET, copyConfig, petFrame, type PetFrame, type PetStroke } from '../src/ui/pet/petCore';
import { DEFAULT_PALETTE } from '../src/onboarding/scene/preset';

const OUT = join(process.cwd(), 'assets/images');
const BG = brand.primary;

const cfg = copyConfig(PET_PRESET);
cfg.emotion = 'happy';
const frame = petFrame(cfg, {
  time: 0,
  face: cfg.poses.happy,
  blink: 1,
  reduced: true,
});

// Same square window PetCircle uses: the head and the first curl of the tail.
const b = PET_PRESET.body;
const HALF = Math.max(b.width, b.height) * 0.78;
const CROP = { x: b.x - HALF, y: b.y + 4 - HALF, w: HALF * 2, h: HALF * 2 };

function petSvg(f: PetFrame, fill: string, shade: string, solid: boolean): string {
  const headR = (Math.max(b.width * b.scaleX, b.height * b.scaleY) / 2) * 1.25;
  const stroke = (s: PetStroke, color = s.color) =>
    `<path d="${s.d}"${s.transform ? ` transform="${s.transform}"` : ''} stroke="${color}" stroke-width="${s.width}" fill="${s.filled ? color : 'none'}" stroke-linecap="round" stroke-linejoin="round"/>`;
  if (solid) {
    // Monochrome: the silhouette only, face cut out, so the launcher can tint it.
    const g = (
      face: string,
    ) => `<g transform="translate(${f.shiftX} 0)"><g transform="translate(0 ${f.float})">
      <g transform="${f.bodyTransform}"><path d="${f.body}" fill="#fff"/></g>${face}
    </g></g>`;
    const face = `<g transform="${f.features}"><g transform="${f.eyes}">${stroke(f.leftEye, '#000')}${stroke(f.rightEye, '#000')}</g>${stroke(f.mouth, '#000')}</g>`;
    return `<defs><mask id="face" maskUnits="userSpaceOnUse" x="-1000" y="-1000" width="2000" height="2000">${g(face)}</mask></defs>
      <g mask="url(#face)"><rect x="-1000" y="-1000" width="2000" height="2000" fill="#fff"/></g>`;
  }
  const halo = f.vapor
    .map((p) => `<circle cx="${p.x}" cy="${p.y}" r="${p.r}" fill="url(#halo)" opacity="${p.opacity}"/>`)
    .join('');
  const haloShade = f.vapor
    .map(
      (p) =>
        `<circle cx="${p.x + p.r * 0.2 * (1 - 2 * f.turn)}" cy="${p.y + p.r * 0.25}" r="${p.r}" fill="url(#halo-shade)" opacity="${p.opacity}"/>`,
    )
    .join('');
  return `<g transform="translate(${f.shiftX} 0)">
    <defs>
      <radialGradient id="halo" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="${fill}" stop-opacity="0.8"/><stop offset="0.5" stop-color="${fill}" stop-opacity="0.45"/><stop offset="1" stop-color="${fill}" stop-opacity="0"/></radialGradient>
      <radialGradient id="halo-shade" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="${shade}" stop-opacity="0.4"/><stop offset="1" stop-color="${shade}" stop-opacity="0"/></radialGradient>
      <linearGradient id="core" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${fill}"/><stop offset="0.66" stop-color="${fill}" stop-opacity="0.97"/><stop offset="1" stop-color="${fill}" stop-opacity="0"/></linearGradient>
      <radialGradient id="form" gradientUnits="userSpaceOnUse" cx="${f.headX - 10 * (1 - 2 * f.turn)}" cy="${b.y - 14}" r="${headR}"><stop offset="0" stop-color="${shade}" stop-opacity="0"/><stop offset="0.6" stop-color="${shade}" stop-opacity="0"/><stop offset="0.86" stop-color="${shade}" stop-opacity="0.42"/><stop offset="1" stop-color="${shade}" stop-opacity="0"/></radialGradient>
      <radialGradient id="highlight"><stop offset="0" stop-color="#fff" stop-opacity="0.85"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
    </defs>
    <g transform="translate(0 ${f.float})">
      <g transform="${f.bodyTransform}">${halo}${haloShade}
        <path d="${f.body}" fill="url(#core)"/><path d="${f.body}" fill="url(#form)"/>
        <path d="${f.volume}" fill="url(#highlight)" opacity="${f.volumeOpacity}"/>
      </g>
      <g transform="${f.features}"><g transform="${f.eyes}">${stroke(f.leftEye)}${stroke(f.rightEye)}</g>${stroke(f.mouth)}</g>
    </g>
  </g>`;
}

/** `scale`: share of the canvas the crop window fills (adaptive icons keep to the 66% safe zone). */
function svg(opts: { bg?: string; scale: number; solid?: boolean }): string {
  const w = CROP.w / opts.scale;
  const x = CROP.x - (w - CROP.w) / 2;
  const y = CROP.y - (w - CROP.h) / 2;
  const bg = opts.bg ? `<rect x="${x}" y="${y}" width="${w}" height="${w}" fill="${opts.bg}"/>` : '';
  const pet = petSvg(frame, DEFAULT_PALETTE.mist, DEFAULT_PALETTE.cloudShade, !!opts.solid);
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${x} ${y} ${w} ${w}">${bg}${pet}</svg>`;
}

const tmp = mkdtempSync(join(tmpdir(), 'icons-'));
function render(name: string, size: number, content: string) {
  const src = join(tmp, `${name}.svg`);
  writeFileSync(src, content);
  execFileSync('rsvg-convert', ['-w', String(size), '-h', String(size), '-o', join(OUT, name), src]);
}

render('icon.png', 1024, svg({ bg: BG, scale: 0.86 }));
render('android-icon-foreground.png', 1024, svg({ scale: 0.6 }));
render('android-icon-background.png', 1024, svg({ bg: BG, scale: 1 }).replace(/<g[\s\S]*<\/g>/, ''));
render('android-icon-monochrome.png', 1024, svg({ scale: 0.6, solid: true }));
render('splash-icon.png', 512, svg({ scale: 0.6 }));
render('favicon.png', 48, svg({ bg: BG, scale: 0.9 }));
console.log('icons written to', OUT);
