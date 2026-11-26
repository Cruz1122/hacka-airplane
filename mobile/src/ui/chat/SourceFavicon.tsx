// Shared source favicon preview ball and URL helpers used by both ChatBubble's stacked badge
// and SourcesSheet's source cards. Renders an offline-safe domain initial underneath, overlaid
// with the site's favicon when reachable.
import { useState } from 'react';
import { Image, StyleSheet, Text, View } from 'react-native';

import { brand, fonts } from '../theme/tokens';

import type { ChatSource } from './citations';

export const MAX_FAVICONS = 3;
const FALLBACK_TONES = [brand.primary, brand.ink, brand.primaryLight] as const;

export interface SourcePreview {
  key: string;
  host?: string;
  letter: string;
  tone: string;
}

export function sourceHost(url?: string): string | undefined {
  if (!url) return undefined;
  try {
    return new URL(url).hostname.replace(/^www\d*\./i, '').toLowerCase();
  } catch {
    return undefined;
  }
}

/** Main display fragment of a web URL: clean host plus readable path, without protocol or query. */
export function formatSourceLink(url?: string): string | null {
  if (!url) return null;
  try {
    const parsed = new URL(url);
    if (parsed.protocol !== 'http:' && parsed.protocol !== 'https:') return null;
    const host = parsed.hostname.replace(/^www\d*\./i, '').toLowerCase();
    const rawPath = parsed.pathname.replace(/\/+$/, '');
    if (!rawPath) return host;
    let decoded = rawPath;
    try {
      decoded = decodeURIComponent(rawPath);
    } catch {
      // Keep raw pathname if percent-encoding is malformed.
    }
    return `${host}${decoded}`;
  } catch {
    return null;
  }
}

export function sourcePreviewFor(source: ChatSource, index = 0): SourcePreview {
  const host = sourceHost(source.url);
  const key = host ?? source.id;
  const letter = (host?.[0] ?? source.title.trim()[0] ?? '•').toUpperCase();
  return { key, host, letter, tone: FALLBACK_TONES[index % FALLBACK_TONES.length] };
}

export function sourcePreviews(sources: readonly ChatSource[]): SourcePreview[] {
  const out: SourcePreview[] = [];
  const seen = new Set<string>();
  for (const s of sources) {
    const host = sourceHost(s.url);
    const key = host ?? s.id;
    if (seen.has(key)) continue;
    seen.add(key);
    out.push(sourcePreviewFor(s, out.length));
    if (out.length >= MAX_FAVICONS) break;
  }
  return out;
}

export function SourceFaviconBall({
  preview,
  size = 18,
  overlap = false,
  ringColor = brand.card,
}: {
  preview: SourcePreview;
  size?: number;
  overlap?: boolean;
  ringColor?: string;
}) {
  const [loaded, setLoaded] = useState(false);
  const [failed, setFailed] = useState(false);
  const faviconUrl =
    preview.host && !failed
      ? `https://www.google.com/s2/favicons?domain=${encodeURIComponent(preview.host)}&sz=64`
      : null;
  const borderWidth = size >= 24 ? 1 : 1.5;
  const inner = size - borderWidth * 2;
  const fontSize = Math.max(9, Math.round(size * 0.46));
  return (
    <View
      style={[
        styles.ball,
        {
          width: size,
          height: size,
          borderRadius: size / 2,
          borderWidth,
          borderColor: ringColor,
          backgroundColor: loaded ? brand.card : preview.tone,
        },
        overlap && styles.overlap,
      ]}
      pointerEvents="none"
    >
      {!loaded && (
        <Text
          style={[styles.letter, { fontSize, lineHeight: fontSize + 2 }]}
          aria-hidden
          accessibilityElementsHidden
          importantForAccessibility="no-hide-descendants"
        >
          {preview.letter}
        </Text>
      )}
      {faviconUrl ? (
        <Image
          source={{ uri: faviconUrl }}
          onLoad={() => setLoaded(true)}
          onError={() => setFailed(true)}
          resizeMode="cover"
          style={[
            styles.image,
            { width: inner, height: inner, borderRadius: inner / 2 },
            !loaded && styles.hidden,
          ]}
        />
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  ball: {
    alignItems: 'center',
    justifyContent: 'center',
    overflow: 'hidden',
  },
  overlap: {
    marginLeft: -6,
  },
  letter: {
    fontFamily: fonts.bold,
    color: brand.onPrimary,
  },
  image: {
    position: 'absolute',
    top: 0,
    left: 0,
  },
  hidden: { opacity: 0 },
});
