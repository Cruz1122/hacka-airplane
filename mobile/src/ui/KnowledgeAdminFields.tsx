import type { ReactNode } from 'react';
import { Pressable, StyleSheet, Text, TextInput, View, type TextInputProps } from 'react-native';

import { brand, radius, spacing, type } from './theme/tokens';

export function AdminButton({
  label,
  onPress,
  primary = false,
  disabled = false,
}: {
  label: string;
  onPress: () => void;
  primary?: boolean;
  disabled?: boolean;
}) {
  return (
    <Pressable
      accessibilityRole="button"
      accessibilityState={{ disabled }}
      disabled={disabled}
      onPress={onPress}
      style={({ pressed }) => [
        styles.button,
        primary && styles.primary,
        (disabled || pressed) && styles.dim,
      ]}
    >
      <Text style={[styles.label, primary && styles.onPrimary]}>{label}</Text>
    </Pressable>
  );
}

export function AdminField({ label, ...props }: TextInputProps & { label: string }) {
  return (
    <View style={styles.field}>
      <Text style={styles.label}>{label}</Text>
      <TextInput
        accessibilityLabel={label}
        placeholderTextColor={brand.inkMuted}
        {...props}
        style={[styles.input, props.multiline && styles.multiline, props.style]}
      />
    </View>
  );
}

export function AdminPanel({ children }: { children: ReactNode }) {
  return <View style={styles.panel}>{children}</View>;
}

export const adminStyles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: brand.card },
  content: {
    width: '100%',
    maxWidth: 680,
    alignSelf: 'center',
    padding: spacing.xl,
    gap: spacing.md,
  },
  heading: { ...type.display, color: brand.ink },
  title: { ...type.title, color: brand.ink },
  body: { ...type.body, color: brand.ink },
  note: { ...type.caption, color: brand.inkMuted },
  error: { color: brand.wine },
  row: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  list: { gap: spacing.sm },
  separator: { height: StyleSheet.hairlineWidth, backgroundColor: brand.primarySoft },
});

const styles = StyleSheet.create({
  button: {
    borderRadius: radius.md,
    backgroundColor: brand.cardShade,
    minHeight: 44,
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.md,
    justifyContent: 'center',
  },
  primary: { backgroundColor: brand.ink },
  dim: { opacity: 0.6 },
  label: { ...type.label, color: brand.ink },
  onPrimary: { color: brand.onPrimary },
  field: { gap: spacing.xs },
  input: {
    ...type.body,
    color: brand.ink,
    backgroundColor: brand.card,
    minHeight: 44,
    borderRadius: radius.md,
    borderWidth: 1,
    borderColor: brand.primary,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
  },
  multiline: { minHeight: 68, textAlignVertical: 'top' },
  panel: {
    padding: spacing.lg,
    gap: spacing.md,
    backgroundColor: brand.cardShade,
    borderRadius: radius.lg,
  },
});
