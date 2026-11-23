// "More" button over the chat header and the small menu it opens. A tap outside closes it.
import { useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';

import { brand, type } from '../theme/tokens';

export interface ChatMenuItem {
  label: string;
  onPress: () => void;
}

export function ChatMenu({
  label,
  items,
  top,
  right,
}: {
  label: string;
  items: ChatMenuItem[];
  top: number;
  right: number;
}) {
  const [open, setOpen] = useState(false);
  return (
    <>
      {open && <Pressable style={StyleSheet.absoluteFill} onPress={() => setOpen(false)} />}
      <Pressable
        onPress={() => setOpen((o) => !o)}
        accessibilityRole="button"
        accessibilityLabel={label}
        accessibilityState={{ expanded: open }}
        style={[styles.button, { top, right }]}
      >
        {[0, 1, 2].map((i) => (
          <View key={i} style={styles.dot} />
        ))}
      </Pressable>
      {open && (
        <View style={[styles.menu, { top: top + 52, right }]} accessibilityRole="menu">
          {items.map((item) => (
            <Pressable
              key={item.label}
              accessibilityRole="menuitem"
              onPress={() => {
                setOpen(false);
                item.onPress();
              }}
              style={({ pressed }) => [styles.item, pressed && styles.itemPressed]}
            >
              <Text style={styles.itemText}>{item.label}</Text>
            </Pressable>
          ))}
        </View>
      )}
    </>
  );
}

const styles = StyleSheet.create({
  button: {
    position: 'absolute',
    width: 44,
    height: 44,
    borderRadius: 14,
    backgroundColor: brand.card,
    borderWidth: 1,
    borderColor: brand.cardShade,
    outlineColor: brand.primary,
    flexDirection: 'row',
    gap: 4,
    alignItems: 'center',
    justifyContent: 'center',
  },
  dot: { width: 5, height: 5, borderRadius: 3, backgroundColor: brand.ink },
  menu: {
    position: 'absolute',
    minWidth: 200,
    paddingVertical: 6,
    borderRadius: 16,
    backgroundColor: brand.card,
    borderWidth: 1,
    borderColor: brand.cardShade,
    outlineColor: brand.primary,
  },
  item: { paddingHorizontal: 18, paddingVertical: 13 },
  itemPressed: { backgroundColor: brand.cardShade },
  itemText: { ...type.label, color: brand.ink },
});
