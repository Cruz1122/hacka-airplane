// A photo's credit on its corner, as the chat's gallery shows it: a camera glyph and the author in
// bold on a `photoScrim` pill, one line. The licence is only in the screen-reader label. With a
// `url` it is a link to the photo's source. Place it absolutely inside the photo's frame.
import { Linking, Pressable, StyleSheet, Text } from 'react-native';

import { fill, t } from '@/i18n';

import { Icon } from './icons/Icon';
import { brand, fonts, radius, spacing } from './theme/tokens';

/** Gap between the pill and the photo's edges. */
export const PHOTO_CREDIT_INSET = 6;
const CAMERA_ICON = 11;

export function PhotoCredit({
  author,
  license,
  url,
  maxWidth,
}: {
  author: string;
  license: string;
  /** The photo's source page; without it the pill is not pressable. */
  url?: string;
  maxWidth?: number;
}) {
  const label = fill(t.chatScreen.media.credit, { author, license });
  const open = url
    ? () =>
        Linking.openURL(url).catch((e: unknown) =>
          console.warn(`Could not open photo source (${url})`, e),
        )
    : undefined;
  return (
    <Pressable
      onPress={open}
      disabled={!open}
      hitSlop={6}
      accessible
      accessibilityRole={open ? 'link' : 'text'}
      accessibilityLabel={label}
      style={({ pressed }) => [styles.credit, { maxWidth }, pressed && styles.pressed]}
    >
      <Icon name="camera" size={CAMERA_ICON} color={brand.onPrimary} strokeWidth={2.2} />
      <Text style={styles.author} numberOfLines={1} ellipsizeMode="tail">
        {author}
      </Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  credit: {
    flexDirection: 'row',
    alignItems: 'center',
    alignSelf: 'flex-start',
    gap: spacing.xs,
    paddingLeft: 6,
    paddingRight: 8,
    paddingVertical: 3,
    borderRadius: radius.pill,
    backgroundColor: brand.photoScrim,
  },
  pressed: { opacity: 0.8 },
  author: {
    flexShrink: 1,
    fontFamily: fonts.bold,
    fontSize: 10,
    lineHeight: 13,
    color: brand.onPrimary,
  },
});
