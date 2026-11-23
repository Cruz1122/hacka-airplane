import { useEffect, useState } from 'react';
import { ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';

import { loadWorld } from '@/core/world';
import { MODELS } from '@/llm/models';
import { modelManager } from '@/llm/modelManager';
import { useSettings } from '@/state/settings';
import { Chip } from '@/ui/Chip';
import { t } from '@/i18n';
import { useColors } from '@/ui/theme';
import { fontSize, radius, spacing } from '@/ui/theme/tokens';

export default function SettingsScreen() {
  const c = useColors();
  const { settings, update } = useSettings();
  const [present, setPresent] = useState<Record<string, boolean>>({});
  const [stations, setStations] = useState<{ id: string; name: string }[]>([]);

  useEffect(() => {
    Promise.all(MODELS.map(async (m) => [m.id, await modelManager.exists(m.id)] as const)).then(
      (r) => setPresent(Object.fromEntries(r)),
      (e) => console.warn('model scan failed', e),
    );
    Promise.resolve(loadWorld()).then((w) => setStations(w.json.stations), (e) => console.warn('world load failed', e));
  }, []);

  if (!settings) return null;
  const h = [styles.h, { color: c.textMuted }];
  return (
    <ScrollView style={{ backgroundColor: c.background }} contentContainerStyle={styles.body}>
      <Text style={h}>{t.model}</Text>
      <View style={styles.wrap}>
        {MODELS.map((m) => (
          <Chip
            key={m.id}
            label={m.label}
            hint={present[m.id] ? t.modelReady : t.modelMissing}
            selected={settings.modelId === m.id}
            onPress={() => update({ modelId: m.id })}
          />
        ))}
      </View>

      <Text style={h}>{t.station}</Text>
      <View style={styles.wrap}>
        <Chip label={t.stationNone} selected={settings.deviceStation === null} onPress={() => update({ deviceStation: null })} />
        {stations.map((s) => (
          <Chip key={s.id} label={s.name} selected={settings.deviceStation === s.id} onPress={() => update({ deviceStation: s.id })} />
        ))}
      </View>

      <Text style={h}>{t.answerMode}</Text>
      <View style={styles.wrap}>
        <Chip label={t.extractive} selected={settings.answerMode === 'extractive'} onPress={() => update({ answerMode: 'extractive' })} />
        <Chip label={t.generate} selected={settings.answerMode === 'generate'} onPress={() => update({ answerMode: 'generate' })} />
      </View>

      <Text style={h}>{t.chat}</Text>
      <View style={styles.wrap}>
        <Chip label={t.chatOn} selected={settings.chat} onPress={() => update({ chat: true })} />
        <Chip label={t.chatOff} selected={!settings.chat} onPress={() => update({ chat: false })} />
      </View>

      <Text style={h}>{t.backend}</Text>
      <View style={styles.wrap}>
        <Chip label={t.backendDevice} selected={settings.backendKind === 'device'} onPress={() => update({ backendKind: 'device' })} />
        <Chip label={t.backendHttp} selected={settings.backendKind === 'http'} onPress={() => update({ backendKind: 'http' })} />
      </View>
      {settings.backendKind === 'http' && (
        <TextInput
          defaultValue={settings.httpUrl}
          onEndEditing={(e) => update({ httpUrl: e.nativeEvent.text.trim() })}
          autoCapitalize="none"
          autoCorrect={false}
          placeholder={t.httpUrl}
          placeholderTextColor={c.textMuted}
          style={[styles.input, { color: c.text, borderColor: c.border, backgroundColor: c.surface }]}
        />
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  body: { padding: spacing.lg, gap: spacing.md },
  h: { fontSize: fontSize.sm, textTransform: 'uppercase', marginTop: spacing.md },
  wrap: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  input: { borderWidth: 1, borderRadius: radius.md, padding: spacing.md, fontSize: fontSize.md },
});
