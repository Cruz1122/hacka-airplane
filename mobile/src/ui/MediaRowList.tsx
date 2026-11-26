import type { ReactElement } from 'react';
import {
  FlatList,
  Image,
  Platform,
  StyleSheet,
  Text,
  View,
  type ImageSourcePropType,
  type StyleProp,
  type ViewStyle,
} from 'react-native';

import { fill, t } from '@/i18n';
import { brand, fonts, radius, spacing, type } from '@/ui/theme/tokens';
import { useAccessibilityTheme } from '@/ui/useAccessibilityTheme';

export type MediaRowItem = {
  image: ImageSourcePropType;
  subtitle: string;
  description: string;
  creditAuthor: string;
  creditLicense: string;
};

const IMAGE = 168;

function spansOf(source: string): { text: string; bold: boolean }[] {
  const parts: string[] = [];
  let buf = '';
  for (let i = 0; i < source.length; i++) {
    const c = source[i];
    const next = source[i + 1];
    if (c === '\\' && (next === '*' || next === '\\')) {
      buf += next;
      i++;
    } else if (c === '*' && next === '*') {
      parts.push(buf);
      buf = '';
      i++;
    } else {
      buf += c;
    }
  }
  parts.push(buf);
  if (parts.length % 2 === 0) {
    const tail = parts.pop()!;
    parts[parts.length - 1] += `**${tail}`;
  }
  const spans: { text: string; bold: boolean }[] = [];
  parts.forEach((text, i) => {
    if (!text) return;
    const bold = i % 2 === 1;
    const last = spans.at(-1);
    if (last?.bold === bold) last.text += text;
    else spans.push({ text, bold });
  });
  return spans;
}

function Para({ text, web }: { text: string; web: boolean }) {
  const { palette, scaled } = useAccessibilityTheme();
  return (
    <Text style={[web ? styles.bodyWeb : styles.body, scaled.body, { color: palette.ink }]} selectable>
      {spansOf(text).map((s, j) => (
        <Text key={j} style={s.bold ? styles.bold : undefined}>
          {s.text}
        </Text>
      ))}
    </Text>
  );
}

function RichBody({ text }: { text: string }) {
  const paras = text.split(/\n{2,}/);
  const web = Platform.OS === 'web';
  if (web) {
    return paras.map((para, i) => <Para key={i} text={para} web />);
  }
  return (
    <View style={styles.bodyStack}>
      {paras.map((para, i) => (
        <Para key={i} text={para} web={false} />
      ))}
    </View>
  );
}

function Credit({ author, license }: { author: string; license: string }) {
  return (
    <View style={styles.credit} accessible accessibilityLabel={fill(t.trail.photoCredit, { author })}>
      <Text style={styles.creditText} selectable={false} numberOfLines={1}>
        {`${author} · ${license}`}
      </Text>
    </View>
  );
}

function Card({ item, index }: { item: MediaRowItem; index: number }) {
  const { palette, scaled } = useAccessibilityTheme();
  const imageLeft = index % 2 === 0;
  const photo = (
    <View
      style={[
        styles.frame,
        { backgroundColor: palette.cardShade },
        Platform.OS === 'web' && (imageLeft ? styles.floatLeft : styles.floatRight),
      ]}
    >
      <Image
        source={item.image}
        style={styles.image}
        resizeMode="cover"
        accessibilityRole="image"
        accessibilityLabel={item.subtitle}
      />
      <Credit author={item.creditAuthor} license={item.creditLicense} />
    </View>
  );
  const subtitle = (
    <Text style={[styles.subtitle, scaled.title, { color: palette.ink }]} selectable>
      {item.subtitle}
    </Text>
  );
  if (Platform.OS === 'web') {
    return (
      <View>
        {subtitle}
        <View style={styles.flow}>
          {photo}
          <RichBody text={item.description} />
        </View>
      </View>
    );
  }
  return (
    <View>
      {subtitle}
      <View style={[styles.row, { flexDirection: imageLeft ? 'row' : 'row-reverse' }]}>
        {photo}
        <View style={styles.copy}>
          <RichBody text={item.description} />
        </View>
      </View>
    </View>
  );
}

export function MediaRowList({
  items,
  ListHeaderComponent,
  ListFooterComponent,
  contentContainerStyle,
}: {
  items: readonly MediaRowItem[];
  ListHeaderComponent?: ReactElement;
  ListFooterComponent?: ReactElement;
  contentContainerStyle?: StyleProp<ViewStyle>;
}) {
  return (
    <FlatList
      data={items as MediaRowItem[]}
      keyExtractor={(_, index) => String(index)}
      renderItem={({ item, index }) => <Card item={item} index={index} />}
      ItemSeparatorComponent={Separator}
      ListHeaderComponent={ListHeaderComponent}
      ListFooterComponent={ListFooterComponent}
      contentContainerStyle={contentContainerStyle}
      initialNumToRender={8}
      windowSize={7}
      removeClippedSubviews
    />
  );
}

function Separator() {
  return <View style={styles.gap} />;
}

const styles = StyleSheet.create({
  row: {
    alignItems: 'flex-start',
    gap: spacing.lg,
  },
  flow: {
    display: 'block',
    overflow: 'hidden',
  } as unknown as ViewStyle,
  frame: {
    width: IMAGE,
    height: IMAGE,
    overflow: 'hidden',
    borderRadius: radius.md,
    backgroundColor: brand.cardShade,
  },
  image: { width: IMAGE, height: IMAGE },
  // Paragraph boxes run under a float; keep the photo and its credit above them.
  floatLeft: {
    zIndex: 1,
    float: 'left',
    marginRight: spacing.lg,
    marginBottom: spacing.xs,
  } as unknown as ViewStyle,
  floatRight: {
    zIndex: 1,
    float: 'right',
    marginLeft: spacing.lg,
    marginBottom: spacing.xs,
  } as unknown as ViewStyle,
  credit: {
    position: 'absolute',
    right: spacing.xs,
    bottom: spacing.xs,
    maxWidth: IMAGE - spacing.xs * 2,
    borderRadius: radius.pill,
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
    backgroundColor: brand.photoScrim,
  },
  creditText: { ...type.caption, fontFamily: fonts.bold, color: brand.onPrimary, flexShrink: 1 },
  copy: { flex: 1, gap: spacing.sm },
  subtitle: { ...type.title, color: brand.ink, marginBottom: spacing.sm },
  bodyStack: { gap: spacing.sm },
  body: { ...type.body, color: brand.ink },
  bodyWeb: {
    ...type.body,
    color: brand.ink,
    display: 'block',
    marginBottom: spacing.sm,
  } as unknown as ViewStyle,
  bold: { fontFamily: fonts.bold },
  gap: { height: spacing.xl },
});
