import * as ImagePicker from 'expo-image-picker';
import { useRouter } from 'expo-router';
import { useCallback, useRef, useState } from 'react';
import { ActivityIndicator, Pressable, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';

import { collectKnowledgeQr, QR_LIMIT, type KnowledgePatch, type KnowledgeQrSeries } from '@/core/knowledge/qrPatch';
import { fill, t } from '@/i18n';
import { markOnboardingDone } from '@/onboarding/launch';
import { applyKnowledgePatches } from '@/state/useKnowledge';
import { QrCamera, readQrImage } from '@/ui/QrCamera';
import { brand, type } from '@/ui/theme/tokens';

const labels = t.qrUpdate;
const message = (error: unknown) => error instanceof Error ? error.message : labels.failed;
const noCamera = labels.noCamera;

function Action({ title, onPress, primary = false }: {
  title: string; onPress: () => void; primary?: boolean;
}) {
  return (
    <Pressable accessibilityRole="button" onPress={onPress} style={[styles.action, primary && styles.primary]}>
      <Text style={[styles.actionText, primary && styles.actionPrimaryText]}>{title}</Text>
    </Pressable>
  );
}

export default function UpdateKnowledgeScreen() {
  const router = useRouter();
  const locked = useRef(false);
  const pending = useRef<KnowledgeQrSeries>(undefined);
  const [camera, setCamera] = useState(false);
  const [raw, setRaw] = useState('');
  const [patches, setPatches] = useState<KnowledgePatch[]>();
  const [progress, setProgress] = useState('');
  const [status, setStatus] = useState('');
  const [error, setError] = useState(false);
  const [working, setWorking] = useState(false);
  const [done, setDone] = useState(false);

  const scan = useCallback((text: string) => {
    if (locked.current) return;
    locked.current = true;
    setCamera(false);
    setStatus('');
    setError(false);
    try {
      const result = collectKnowledgeQr(text.trim(), pending.current);
      setRaw('');
      if ('series' in result) {
        pending.current = result.series;
        setProgress(fill(labels.seriesProgress, { read: result.series.parts.size, total: result.series.total }));
      } else {
        pending.current = undefined;
        setProgress('');
        setPatches(result.patches);
      }
    }
    catch (cause) { setError(true); setStatus(message(cause)); }
  }, []);
  const cameraError = useCallback(() => { setCamera(false); setError(true); setStatus(noCamera); }, []);
  function resetScan() {
    locked.current = false;
    setStatus('');
    setError(false);
  }
  async function pickQr() {
    resetScan();
    setCamera(false);
    try {
      const selected = await ImagePicker.launchImageLibraryAsync({ mediaTypes: ['images'] });
      if (selected.canceled) return;
      const uri = selected.assets[0].uri;
      try {
        const data = await readQrImage(uri);
        if (!data) throw new Error(labels.unreadable);
        scan(data);
      } finally {
        if (uri.startsWith('blob:')) URL.revokeObjectURL(uri);
      }
    } catch (cause) { setError(true); setStatus(message(cause)); }
  }
  async function apply() {
    if (!patches || working) return;
    setWorking(true);
    setError(false);
    setStatus('');
    try {
      const count = await applyKnowledgePatches(patches);
      setDone(true);
      setStatus(count === 0 ? labels.duplicate
        : patches.length > 1 ? fill(labels.batchUpdated, { count })
          : patch?.op === 'remove' ? labels.removed : labels.updated);
    } catch (cause) {
      setError(true);
      setStatus(message(cause));
    } finally {
      setWorking(false);
    }
  }

  const patch = patches?.length === 1 ? patches[0] : undefined;
  const applyLabel = patch?.op === 'remove' ? labels.confirm : labels.apply;

  function cancelSeries() {
    pending.current = undefined;
    setProgress('');
    setRaw('');
    resetScan();
  }

  function goToChat() {
    markOnboardingDone();
    router.dismissTo('/');
  }

  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.content} keyboardShouldPersistTaps="handled">
      <Text accessibilityRole="header" style={styles.heading}>{labels.heading}</Text>
      <Text style={styles.body}>{labels.body}</Text>
      {!patches && <>
        {!!progress && <>
          <Text accessibilityLiveRegion="polite" style={styles.body}>{progress}</Text>
          <Action title={labels.cancelSeries} onPress={cancelSeries} />
        </>}
        {camera ? <>
          <QrCamera onCode={scan} onError={cameraError} />
          <Action title={labels.close} onPress={() => setCamera(false)} />
        </> : <Action primary title={labels.open} onPress={() => { resetScan(); setCamera(true); }} />}
        <Action title={labels.pick} onPress={() => void pickQr()} />
        <TextInput style={styles.input} accessibilityLabel={labels.code} placeholder={labels.paste}
          placeholderTextColor={brand.inkMuted} autoCorrect={false} autoCapitalize="none" value={raw} onChangeText={setRaw}
          multiline maxLength={QR_LIMIT} />
        {!!raw.trim() && <Action title={labels.read} onPress={() => { resetScan(); scan(raw); }} />}
      </>}
      {patches && <View style={styles.preview}>
        {patch ? <>
        <Text style={styles.title}>{patch.op === 'put' ? patch.entry.title : labels.remove}</Text>
        <Text style={styles.body}>{patch.id}</Text>
        {patch.op === 'put' && <>
          <Text style={styles.body}>{patch.entry.answer}</Text>
          <Text style={styles.body}>{fill(labels.counts, { questions: patch.entry.questions.length, variants: patch.entry.variants.length })}</Text>
          {[...patch.entry.variants, ...patch.entry.steps, ...patch.entry.more, ...patch.entry.why,
            ...patch.entry.sources.map(({ label, url }) => label + ' · ' + url),
            ...patch.entry.related].map((text, i) => <Text key={i} style={styles.body}>{text}</Text>)}
        </>}
        </> : <>
          <Text style={styles.title}>{fill(labels.batchSummary, { count: patches.length })}</Text>
          {patches.slice(0, 10).map((item) => {
            const title = item.op === 'put' ? item.entry.title : labels.remove;
            return <Text key={item.id} style={styles.body}>{title}</Text>;
          })}
        </>}
        {!done && <Text style={styles.body}>{labels.trust}</Text>}
      </View>}
      {!!status && <Text accessibilityLiveRegion="polite" style={[styles.body, error && styles.error]}>{status}</Text>}
      {working && <View style={styles.progress}>
        <ActivityIndicator color={brand.ink} />
        <Text style={styles.body}>{labels.working}</Text>
      </View>}
      {patches && !working && !done && <>
        <Action primary title={applyLabel} onPress={() => void apply()} />
        <Action title={labels.cancel} onPress={() => { setPatches(undefined); resetScan(); }} />
      </>}
      {done && <Action primary title={labels.back} onPress={goToChat} />}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: brand.card },
  content: { padding: 24, gap: 14, width: '100%', maxWidth: 640, alignSelf: 'center' },
  heading: { ...type.display, color: brand.ink },
  title: { ...type.title, color: brand.ink },
  body: { ...type.body, color: brand.ink },
  action: { alignItems: 'center', padding: 12, borderRadius: 12, backgroundColor: brand.cardShade },
  actionText: { ...type.label, color: brand.ink },
  primary: { backgroundColor: brand.ink },
  actionPrimaryText: { color: brand.onPrimary },
  input: { ...type.body, minHeight: 62, borderWidth: 1, borderColor: brand.primary, borderRadius: 12, padding: 12, color: brand.ink },
  preview: { padding: 16, gap: 8, borderRadius: 16, backgroundColor: brand.cardShade },
  error: { color: brand.wine },
  progress: { flexDirection: 'row', alignItems: 'center', gap: 10 },
});

