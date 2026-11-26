import { Link } from 'expo-router';
import { Pressable, StyleSheet, Text } from 'react-native';

import { t } from '@/i18n';
import { brand, type } from './theme/tokens';

export function UpdateKnowledgeLink() {
  return (
    <Link href="/actualizar" asChild>
      <Pressable accessibilityRole="link" style={styles.action}>
        <Text style={styles.label}>{t.qrUpdate.launch}</Text>
      </Pressable>
    </Link>
  );
}

const styles = StyleSheet.create({
  action: {
    alignSelf: 'flex-start',
    minHeight: 44,
    justifyContent: 'center',
    paddingHorizontal: 12,
    marginBottom: 8,
    borderRadius: 12,
    backgroundColor: brand.cardShade,
  },
  label: { ...type.caption, color: brand.ink },
});

