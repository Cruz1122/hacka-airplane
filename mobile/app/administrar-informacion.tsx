import { useFocusEffect } from 'expo-router';
import { useCallback, useRef, useState, type ComponentRef } from 'react';
import { ScrollView, Text } from 'react-native';

import { t } from '@/i18n';
import { adminStyles as styles } from '@/ui/KnowledgeAdminFields';
import { KnowledgeAdminPanel } from '@/ui/KnowledgeAdminPanel';

const labels = t.knowledgeAdmin;

export default function KnowledgeAdministration() {
  const scroll = useRef<ComponentRef<typeof ScrollView>>(null);
  const goTop = useCallback(() => scroll.current?.scrollTo({ y: 0, animated: false }), []);
  const [lockSignal, setLockSignal] = useState(0);

  useFocusEffect(
    useCallback(
      () => () => {
        setLockSignal((n) => n + 1);
      },
      [],
    ),
  );

  return (
    <ScrollView
      ref={scroll}
      style={styles.screen}
      contentContainerStyle={styles.content}
      keyboardShouldPersistTaps="handled"
    >
      <Text accessibilityRole="header" style={styles.heading}>
        {labels.heading}
      </Text>
      <KnowledgeAdminPanel key={lockSignal} goTop={goTop} />
    </ScrollView>
  );
}
