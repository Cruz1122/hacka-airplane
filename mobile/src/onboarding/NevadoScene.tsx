// Production renderer: draws a SceneDoc as layered SVG. The Lab, the onboarding and SVG export all
// use this component, so the scene is never duplicated by hand.
import { memo, useId, useState, type ReactNode } from 'react';
import { Platform, StyleSheet, View, type ViewStyle } from 'react-native';
import Svg, {
  Circle,
  ClipPath,
  Defs,
  Ellipse,
  G,
  LinearGradient,
  Path,
  RadialGradient,
  Rect,
  Stop,
} from 'react-native-svg';

import { PetVaporFigure } from '@/ui/pet/PetVaporFigure';
import { blinkAt, PET_PRESET, petFrame } from '@/ui/pet/petCore';
import { useFaceTransition } from '@/ui/pet/useFaceTransition';
import { useReducedMotion } from '@/ui/useReducedMotion';

import { craterOf, resolveColor, ventOf, volcanoOf } from './scene/doc';
import {
  cloudPuffs,
  craterPaths,
  flowerPetals,
  flowerStem,
  frailejonShape,
  lupineShape,
  mistPuffs,
  affineMatrix,
  cameraDelta,
  composeAffine,
  invertAffine,
  parallaxAffine,
  parallaxMatrix,
  ridgeGrass,
  ridgePath,
  ridgeShadePaths,
  rockPaths,
  sceneViewBox,
  snowPaths,
  steamPuffs,
  transformMatrix,
  tuftBlades,
  viewTransform,
  volcanoErosion,
  volcanoPath,
  volcanoShadeAxis,
  volcanoShadePath,
} from './scene/geometry';
import type {
  Body,
  Camera,
  Color,
  CraterBody,
  PetBody,
  SceneDoc,
  SceneObject,
  VolcanoBody,
} from './scene/types';

// Geometry depends only on a body (and, for volcano parts, the volcano body). Idle motions and
// camera moves create new objects every frame but keep those bodies, so their paths are reused.
const geoCache = new WeakMap<object, { dep: object | null; value: unknown }>();
function geo<T>(body: object, dep: object | null, make: () => T): T {
  const hit = geoCache.get(body);
  if (hit && hit.dep === dep) return hit.value as T;
  const value = make();
  geoCache.set(body, { dep, value });
  return value;
}

const volcanoGeo = (v: VolcanoBody) =>
  geo(v, null, () => ({
    silhouette: volcanoPath(v),
    shade: volcanoShadePath(v),
    shadeAxis: volcanoShadeAxis(v),
    erosion: volcanoErosion(v),
  }));

export interface NevadoSceneProps {
  doc: SceneDoc;
  /** Size of the drawing area in points; picks which part of the scene is visible. */
  width: number;
  height: number;
  /**
   * True while the camera moves (transition, swipe). On web each layer then follows the camera as
   * a view transform over SVG drawn at the last resting camera, so camera frames redraw no SVG;
   * when it turns false the SVG is redrawn once at the final camera, sharp. Native ignores it.
   */
  moving?: boolean;
}

/** Volcano that positions a hosted object (snow, crater, steam, pet), as the frame needs it. */
interface Hosted {
  object: SceneObject;
  body: VolcanoBody;
  parallax: number;
  crater: CraterBody | null;
}

const sameCamera = (a: Camera, b: Camera) => a.x === b.x && a.y === b.y && a.zoom === b.zoom;

export function NevadoScene({ doc, width, height, moving = false }: NevadoSceneProps) {
  const prefix = `ns${useId().replace(/[^a-zA-Z0-9]/g, '')}`;
  const vb = sceneViewBox(width, height);
  // The camera the SVG is drawn with: the live one at rest, the last resting one while moving.
  // TODO(follow the camera on native, react-native-svg's Android SvgView draws into a bitmap the
  // size of its view, so a layer moved by its view would show its empty edges; needs layers drawn
  // with a bleed margin, measured on the device first).
  const follow = moving && FOLLOW_CAMERA;
  const [rest, setRest] = useState(doc.camera);
  if (!follow && !sameCamera(rest, doc.camera)) setRest(doc.camera);
  const baked = follow ? rest : doc.camera;
  // One native view per layer: a camera move or a blur is a cheap view transform/filter on it,
  // and an idle motion repaints only its own layer instead of the whole scene.
  return (
    <View style={{ width, height, overflow: 'hidden' }}>
      {doc.layers
        .filter((layer) => layer.visible && layer.id !== 'uiOverlay')
        .map((layer) => {
          const hosted = layer.objects.map((o): Hosted | null => {
            const host = volcanoOf(doc, o.body);
            if (!host) return null;
            const withCrater = o.body.kind === 'steam' || o.body.kind === 'pet';
            return {
              object: host.object,
              body: host.body,
              parallax: host.layer.parallax,
              crater: withCrater ? craterOf(doc, host.object.id) : null,
            };
          });
          const delta = cameraDelta(doc.camera, baked, layer.parallax);
          const { translateX, translateY, scale } = viewTransform(delta, vb, width, height);
          // Hosted objects follow their volcano's depth; when it differs from this layer's, they
          // need the live camera inside the SVG while moving (only after a Lab edit).
          const live = hosted.some((h) => h && h.parallax !== layer.parallax) ? doc.camera : null;
          // Blur is in scene units; the view filter takes points. Android applies it as a GPU
          // RenderEffect (API 31+), web as a CSS filter on the composited layer.
          const blur = layer.blur * (width / vb.width);
          return (
            <View
              key={layer.id}
              style={[
                StyleSheet.absoluteFill,
                WEB_LAYER,
                {
                  opacity: layer.opacity,
                  transform: [{ translateX }, { translateY }, { scale }],
                },
                blur > 0.05 && { filter: `blur(${blur.toFixed(2)}px)` },
              ]}
            >
              <LayerSvg
                layerId={layer.id}
                parallax={layer.parallax}
                objects={layer.objects}
                hosted={hosted}
                bakedX={baked.x}
                bakedY={baked.y}
                bakedZoom={baked.zoom}
                live={live}
                palette={doc.palette}
                prefix={prefix}
                viewBox={`${vb.x} ${vb.y} ${vb.width} ${vb.height}`}
                width={width}
                height={height}
              />
            </View>
          );
        })}
    </View>
  );
}

const FOLLOW_CAMERA = Platform.OS === 'web';
// Composited layers on web, so a transform or filter change does not repaint the layer's SVG.
const WEB_LAYER = (Platform.OS === 'web' ? { willChange: 'transform' } : {}) as ViewStyle;
// A layer moved by its view transform must still show the scene beyond its box (the root clips).
const WEB_SVG = Platform.OS === 'web' ? { overflow: 'visible' as const } : undefined;

interface LayerSvgProps {
  layerId: string;
  parallax: number;
  objects: SceneObject[];
  hosted: (Hosted | null)[];
  bakedX: number;
  bakedY: number;
  bakedZoom: number;
  live: Camera | null;
  palette: Record<string, string>;
  prefix: string;
  viewBox: string;
  width: number;
  height: number;
}

// `hosted` is rebuilt on every scene render; compare what it points to.
function sameLayerSvg(a: LayerSvgProps, b: LayerSvgProps): boolean {
  for (const k of Object.keys(a) as (keyof LayerSvgProps)[]) {
    if (k !== 'hosted' && a[k] !== b[k]) return false;
  }
  return (
    a.hosted.length === b.hosted.length &&
    a.hosted.every((h, i) => {
      const o = b.hosted[i];
      if (!h || !o) return h === o;
      return h.object === o.object && h.parallax === o.parallax && h.crater === o.crater;
    })
  );
}

const LayerSvg = memo(function LayerSvg({
  layerId,
  parallax,
  objects,
  hosted,
  bakedX,
  bakedY,
  bakedZoom,
  live,
  palette,
  prefix,
  viewBox,
  width,
  height,
}: LayerSvgProps) {
  const baked = { x: bakedX, y: bakedY, zoom: bakedZoom };
  // Undo this layer's view transform for objects that move at another depth.
  const unshift = live ? invertAffine(cameraDelta(live, baked, parallax)) : null;
  const cameraAt = (depth: number) =>
    unshift && depth !== parallax
      ? affineMatrix(composeAffine(unshift, parallaxAffine(live!, depth)))
      : parallaxMatrix(baked, depth);
  // One camera group per run of objects at the same depth: a camera change rewrites these few
  // transforms and leaves every (memoized) object untouched.
  const runs: { depth: number; items: ReactNode[] }[] = [];
  objects.forEach((o, i) => {
    const host = hosted[i];
    const depth = host ? host.parallax : parallax;
    let hostTransform = host ? transformMatrix(host.object.transform) : null;
    if (host && o.body.kind === 'pet') {
      // The pet's own transform is an offset from the vent, so scaling it in the Lab
      // grows the pet in place instead of sliding it away from the crater.
      const vent = ventOf(host.body, host.crater);
      hostTransform += ` translate(${vent.x} ${vent.y})`;
    }
    const item = (
      <ObjectFrame
        key={o.id}
        object={o}
        hostTransform={hostTransform}
        palette={palette}
        host={host?.body ?? null}
        crater={host?.crater ?? null}
        prefix={prefix}
      />
    );
    const last = runs[runs.length - 1];
    if (last && last.depth === depth) last.items.push(item);
    else runs.push({ depth, items: [item] });
  });
  return (
    <Svg
      width={width}
      height={height}
      viewBox={viewBox}
      preserveAspectRatio="xMidYMax slice"
      style={WEB_SVG}
    >
      <G id={`layer-${layerId}`}>
        {runs.map((run, i) => (
          <G key={i} transform={cameraAt(run.depth)}>
            {run.items}
          </G>
        ))}
      </G>
    </Svg>
  );
}, sameLayerSvg);

/** The volcano frame (for volcano parts), then the object's own transform. */
// memo: idle motions and tracks give new identities only to the objects they change, so every
// other object (and its SVG subtree) is skipped on a frame.
const ObjectFrame = memo(function ObjectFrame({
  object,
  hostTransform,
  palette,
  host,
  crater,
  prefix,
}: {
  object: SceneObject;
  hostTransform: string | null;
  palette: Record<string, string>;
  host: VolcanoBody | null;
  crater: CraterBody | null;
  prefix: string;
}) {
  const own = (
    <G
      id={`obj-${object.id}`}
      transform={transformMatrix(object.transform)}
      opacity={object.transform.opacity}
    >
      <ObjectBody
        id={object.id}
        body={object.body}
        stroke={object.stroke}
        strokeWidth={object.strokeWidth}
        palette={palette}
        host={host}
        crater={crater}
        prefix={prefix}
      />
    </G>
  );
  return hostTransform ? <G transform={hostTransform}>{own}</G> : own;
});

interface BodyProps {
  id: string;
  body: Body;
  stroke: Color;
  strokeWidth: number;
  palette: Record<string, string>;
  host: VolcanoBody | null;
  crater: CraterBody | null;
  prefix: string;
}

// memo: during an animation most bodies keep their identity, so most of the tree is skipped.
const ObjectBody = memo(function ObjectBody({
  id: objectId,
  body: b,
  stroke: strokeColor,
  strokeWidth,
  palette,
  host,
  crater,
  prefix,
}: BodyProps): ReactNode {
  const c = (color: Color) => resolveColor(palette, color);
  const id = (part: string) => `${prefix}-${objectId}-${part}`;
  const url = (part: string) => `url(#${id(part)})`;
  const stroke = strokeWidth > 0 ? { stroke: c(strokeColor), strokeWidth } : {};

  switch (b.kind) {
    case 'sky':
      return (
        <>
          <Defs>
            <LinearGradient
              id={id('g')}
              x1={0}
              y1={0}
              x2={0}
              y2={b.horizon}
              gradientUnits="userSpaceOnUse"
            >
              <Stop offset="0" stopColor={c(b.top)} />
              <Stop offset={String(b.middleStop)} stopColor={c(b.middle)} />
              <Stop offset="1" stopColor={c(b.bottom)} />
            </LinearGradient>
          </Defs>
          <Rect x={-1400} y={-1400} width={3200} height={3600} fill={url('g')} />
        </>
      );
    case 'sun':
      return (
        <>
          <Defs>
            <RadialGradient id={id('halo')} cx="50%" cy="50%" r="50%">
              <Stop offset="0" stopColor={c(b.halo)} stopOpacity={b.haloStrength} />
              <Stop offset="0.25" stopColor={c(b.halo)} stopOpacity={b.haloStrength * 0.45} />
              <Stop offset="1" stopColor={c(b.halo)} stopOpacity={0} />
            </RadialGradient>
          </Defs>
          <Circle r={b.haloRadius} fill={url('halo')} />
          <Circle r={b.radius} fill={c(b.core)} {...stroke} />
        </>
      );
    case 'cloud': {
      const puffs = geo(b, null, () => cloudPuffs(b));
      const base = (1 - b.flatness) * b.height * 0.6;
      // Soft radial puffs: dense where they overlap, frayed at the rim, grey underneath.
      return (
        <>
          <Defs>
            <RadialGradient id={id('f')} cx="50%" cy="45%" r="50%">
              <Stop offset="0" stopColor={c(b.fill)} stopOpacity={1} />
              <Stop offset="0.7" stopColor={c(b.fill)} stopOpacity={0.9} />
              <Stop offset="1" stopColor={c(b.fill)} stopOpacity={0} />
            </RadialGradient>
            <RadialGradient id={id('s')} cx="50%" cy="50%" r="50%">
              <Stop offset="0" stopColor={c(b.shade)} stopOpacity={0.9} />
              <Stop offset="0.65" stopColor={c(b.shade)} stopOpacity={0.6} />
              <Stop offset="1" stopColor={c(b.shade)} stopOpacity={0} />
            </RadialGradient>
            <ClipPath id={id('clip')}>
              <Rect
                x={-b.width}
                y={-b.height * 3}
                width={b.width * 2}
                height={b.height * 3 + base}
              />
            </ClipPath>
          </Defs>
          <G clipPath={url('clip')}>
            {puffs.map((p, i) => (
              <Circle
                key={`s${i}`}
                cx={p.cx + p.r * 0.1}
                cy={p.cy + p.r * 0.3}
                r={p.r}
                fill={url('s')}
              />
            ))}
            {puffs.map((p, i) => (
              <Circle
                key={`f${i}`}
                cx={p.cx}
                cy={p.cy - p.r * 0.05}
                r={p.r * 1.02}
                fill={url('f')}
                {...stroke}
              />
            ))}
          </G>
        </>
      );
    }
    case 'ridge': {
      const g = geo(b, null, () => ({
        body: ridgePath(b),
        shade: ridgeShadePaths(b),
        grass: ridgeGrass(b),
      }));
      return (
        <>
          <Defs>
            <LinearGradient id={id('g')} x1="0" y1="0" x2="0" y2="1">
              <Stop offset="0" stopColor={c(b.top)} />
              <Stop offset="1" stopColor={c(b.bottom)} />
            </LinearGradient>
            {/* Shadow faces are darkest under the crest and soften toward the base. */}
            <LinearGradient id={id('s')} x1="0" y1="0" x2="0" y2="1">
              <Stop offset="0" stopColor={c(b.shade)} stopOpacity={0.6} />
              <Stop offset="1" stopColor={c(b.shade)} stopOpacity={0.15} />
            </LinearGradient>
          </Defs>
          <Path d={g.body} fill={url('g')} {...stroke} />
          {g.shade.map((d, i) => (
            <Path key={i} d={d} fill={url('s')} />
          ))}
          {g.grass !== '' && (
            <Path
              d={g.grass}
              fill="none"
              stroke={c(b.grassColor)}
              strokeWidth={0.9}
              strokeLinecap="round"
              opacity={0.8}
            />
          )}
        </>
      );
    }
    case 'volcano': {
      const g = volcanoGeo(b);
      return (
        <>
          <Defs>
            <ClipPath id={id('clip')}>
              <Path d={g.silhouette} />
            </ClipPath>
            <LinearGradient
              id={id('g')}
              x1={0}
              y1={-b.height}
              x2={0}
              y2={0}
              gradientUnits="userSpaceOnUse"
            >
              <Stop offset="0" stopColor={c(b.ash)} />
              <Stop offset="0.55" stopColor={c(b.fill)} />
              <Stop offset="1" stopColor={c(b.fill)} />
            </LinearGradient>
            <LinearGradient
              id={id('haze')}
              x1={0}
              y1={-b.height * 0.45}
              x2={0}
              y2={0}
              gradientUnits="userSpaceOnUse"
            >
              <Stop offset="0" stopColor={c(b.haze)} stopOpacity={0} />
              <Stop offset="1" stopColor={c(b.haze)} stopOpacity={0.55} />
            </LinearGradient>
            <LinearGradient id={id('shade')} gradientUnits="userSpaceOnUse" {...g.shadeAxis}>
              <Stop offset="0" stopColor={c(b.shade)} stopOpacity={0} />
              <Stop offset="1" stopColor={c(b.shade)} stopOpacity={0.55} />
            </LinearGradient>
          </Defs>
          <Path d={g.silhouette} fill={url('g')} {...stroke} />
          <G clipPath={url('clip')}>
            <Path d={g.shade} fill={url('shade')} />
            <Path d={g.erosion.ravines} fill={c(b.gully)} opacity={0.5} />
            <Path d={g.erosion.crests} fill={c(b.ash)} opacity={0.4} />
            <Rect
              x={-b.baseWidth}
              y={-b.height * 0.45}
              width={b.baseWidth * 2}
              height={b.height * 0.45 + b.depth}
              fill={url('haze')}
            />
          </G>
        </>
      );
    }
    case 'snowCap': {
      if (!host) return null;
      const v = volcanoGeo(host);
      const s = geo(b, host, () => snowPaths(host, b));
      return (
        <>
          <Defs>
            <ClipPath id={id('vclip')}>
              <Path d={v.silhouette} />
            </ClipPath>
            <ClipPath id={id('sclip')}>
              <Path d={s.field} />
            </ClipPath>
            <LinearGradient id={id('ice')} gradientUnits="userSpaceOnUse" {...v.shadeAxis}>
              <Stop offset="0" stopColor={c(b.ice)} stopOpacity={0} />
              <Stop offset="1" stopColor={c(b.ice)} stopOpacity={0.9} />
            </LinearGradient>
          </Defs>
          <G clipPath={url('vclip')}>
            <Path d={s.patches} fill={c(b.snow)} opacity={0.8} />
            <Path d={s.field} fill={c(b.snow)} {...stroke} />
            <G clipPath={url('sclip')}>
              <Path d={v.shade} fill={url('ice')} />
              <Path d={v.erosion.ravines} fill={c(b.ice)} opacity={0.3} />
              <Path d={s.outcrops} fill={c(host.shade)} opacity={0.5} />
            </G>
          </G>
        </>
      );
    }
    case 'crater': {
      if (!host) return null;
      const s = geo(b, host, () => craterPaths(host, b));
      return (
        <>
          <Path d={s.mouth} fill={c(b.inner)} {...stroke} />
          <Path d={s.wall} fill={c(b.rim)} opacity={0.3} />
          <Path d={s.lip} fill="none" stroke={c(b.rim)} strokeWidth={1.4} strokeLinecap="round" />
        </>
      );
    }
    case 'steam': {
      if (!host) return null;
      const vent = ventOf(host, crater);
      const puffs = steamPuffs(b);
      // Radial-gradient puffs overlap into a translucent plume; no masks, which are costly on Android.
      return (
        <G transform={`translate(${vent.x} ${vent.y})`}>
          <Defs>
            <RadialGradient id={id('f')} cx="50%" cy="50%" r="50%">
              <Stop offset="0" stopColor={c(b.fill)} stopOpacity={0.7} />
              <Stop offset="0.5" stopColor={c(b.fill)} stopOpacity={0.35} />
              <Stop offset="1" stopColor={c(b.fill)} stopOpacity={0} />
            </RadialGradient>
            <RadialGradient id={id('s')} cx="50%" cy="50%" r="50%">
              <Stop offset="0" stopColor={c(b.shade)} stopOpacity={0.45} />
              <Stop offset="1" stopColor={c(b.shade)} stopOpacity={0} />
            </RadialGradient>
          </Defs>
          {puffs.map((p, i) => (
            <Circle
              key={`s${i}`}
              cx={p.x + p.r * 0.16}
              cy={p.y + p.r * 0.2}
              r={p.r}
              fill={url('s')}
              opacity={p.opacity * 0.6}
            />
          ))}
          {puffs.map((p, i) => (
            <Circle
              key={`f${i}`}
              cx={p.x}
              cy={p.y}
              r={p.r}
              fill={url('f')}
              opacity={p.opacity}
              {...stroke}
            />
          ))}
        </G>
      );
    }
    case 'frailejon': {
      const s = geo(b, null, () => frailejonShape(b));
      return (
        <>
          <Path
            d={s.stalks}
            fill="none"
            stroke={c(b.leaf)}
            strokeWidth={1.1}
            strokeLinecap="round"
          />
          <Path d={s.trunk} fill={c(b.trunk)} {...stroke} />
          <Path
            d={s.trunkDark}
            fill="none"
            stroke={c(b.trunkShade)}
            strokeWidth={1.2}
            strokeLinecap="round"
          />
          <Path
            d={s.trunkLight}
            fill="none"
            stroke={c(b.leafLight)}
            strokeWidth={1}
            strokeLinecap="round"
            opacity={0.45}
          />
          <Path d={s.deadLeaves} fill={c(b.trunkShade)} opacity={0.9} />
          <Path d={s.backLeaves} fill={c(b.leaf)} />
          <Path d={s.frontLeaves} fill={c(b.leafLight)} />
          {s.heads.map((h, i) => (
            <Circle key={i} cx={h.cx} cy={h.cy} r={h.r} fill={c(b.flower)} />
          ))}
        </>
      );
    }
    case 'flower':
      return (
        <>
          <Path
            d={flowerStem(b)}
            fill="none"
            stroke={c(b.stem)}
            strokeWidth={1.1}
            strokeLinecap="round"
          />
          <Path d={flowerPetals(b)} fill={c(b.petal)} {...stroke} />
          <Circle cx={0} cy={-b.stemHeight} r={b.petalSize * 0.38} fill={c(b.center)} />
        </>
      );
    case 'lupine': {
      const s = geo(b, null, () => lupineShape(b));
      return (
        <>
          <Path
            d={s.stem}
            fill="none"
            stroke={c(b.leaf)}
            strokeWidth={b.width * 0.08}
            strokeLinecap="round"
          />
          <Path d={s.leaves} fill={c(b.leaf)} {...stroke} />
          {s.florets.map((f, i) => (
            <G key={i}>
              <Ellipse cx={f.x} cy={f.y} rx={f.rx} ry={f.ry} fill={c(b.color)} />
              <Ellipse
                cx={f.x - f.rx * 0.15}
                cy={f.y - f.ry * 0.2}
                rx={f.rx * 0.8}
                ry={f.ry * 0.75}
                fill={c(b.colorLight)}
                opacity={0.25 + 0.75 * f.f}
              />
            </G>
          ))}
        </>
      );
    }
    case 'rock': {
      const s = geo(b, null, () => rockPaths(b));
      return (
        <>
          <Path d={s.body} fill={c(b.fill)} {...stroke} />
          <Path d={s.shade} fill={c(b.shade)} />
          <Path d={s.light} fill={c(b.light)} opacity={0.8} />
        </>
      );
    }
    case 'tuft': {
      const s = geo(b, null, () => tuftBlades(b));
      return (
        <>
          <Path
            d={s.dark}
            fill="none"
            stroke={c(b.shade)}
            strokeWidth={1.2}
            strokeLinecap="round"
          />
          <Path
            d={s.light}
            fill="none"
            stroke={c(b.fill)}
            strokeWidth={1.1}
            strokeLinecap="round"
          />
        </>
      );
    }
    case 'mist': {
      const inner = Math.max(0, Math.min(0.95, (1 - b.diffusion) * 0.8));
      const puffs = geo(b, null, () => mistPuffs(b));
      return (
        <>
          <Defs>
            <RadialGradient id={id('g')} cx="50%" cy="50%" r="50%">
              <Stop offset="0" stopColor={c(b.fill)} stopOpacity={1} />
              <Stop offset={String(inner)} stopColor={c(b.fill)} stopOpacity={0.85} />
              <Stop offset="1" stopColor={c(b.fill)} stopOpacity={0} />
            </RadialGradient>
          </Defs>
          {puffs.map((p, i) => (
            <Ellipse key={i} cx={p.cx} cy={p.cy} rx={p.rx} ry={p.ry} fill={url('g')} />
          ))}
        </>
      );
    }
    case 'pet':
      // Geometry and face come from the Pet asset (petCore); the vapor colors come from the scene
      // palette so the Pet matches the clouds around it.
      return <ScenePet body={b} fill={c(b.fill)} shade={c(b.shade)} prefix={id('pet')} />;
    case 'ui':
      return null;
  }
});

/**
 * The scene's Pet. The emotion track steps halfway through a swipe; the face then morphs to the
 * new pose the way the Pet component does (its transition time and easing, from the face on
 * screen), instead of snapping.
 */
function ScenePet({
  body: b,
  fill,
  shade,
  prefix,
}: {
  body: PetBody;
  fill: string;
  shade: string;
  prefix: string;
}) {
  const reduced = useReducedMotion();
  const motion = PET_PRESET.motion;
  const face = useFaceTransition(
    PET_PRESET.poses,
    b.emotion,
    reduced ? 0 : motion.transition,
    motion.easing,
  );
  const cfg = { ...PET_PRESET, emotion: b.emotion, voice: b.voice, audio: b.audio };
  const frame = petFrame(cfg, {
    time: b.clock,
    face,
    blink: blinkAt(b.clock, motion.blinkInterval),
  });
  return <PetVaporFigure config={cfg} frame={frame} fill={fill} shade={shade} prefix={prefix} />;
}
