import * as ImagePicker from 'expo-image-picker';
import { useRouter } from 'expo-router';
import { useCallback, useEffect, useRef, useState } from 'react';
import {
  ActivityIndicator,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';

import {
  collectKnowledgeQr,
  QR_LIMIT,
  type KnowledgePatch,
  type KnowledgeQrSeries,
} from '@/core/knowledge/qrPatch';
import { fill, t } from '@/i18n';
import { markOnboardingDone } from '@/onboarding/launch';
import {
  bluetoothShareAvailable,
  findBluetoothShares,
  receiveBluetoothShare,
  type ShareOffer,
} from '@/state/knowledgeShare';
import { applyKnowledgePatches } from '@/state/useKnowledge';
import { SignalPulse } from '@/ui/group/SignalPulse';
import { Icon } from '@/ui/icons/Icon';
import { InfoCard } from '@/ui/InfoCard';
import { PrimaryButton } from '@/ui/PrimaryButton';
import { QrCamera, readQrImage } from '@/ui/QrCamera';
import { SecondaryButton } from '@/ui/SecondaryButton';
import { radius, spacing } from '@/ui/theme/tokens';
import { useAccessibilityTheme } from '@/ui/useAccessibilityTheme';

const labels = t.qrUpdate;
const message = (error: unknown) => (error instanceof Error ? error.message : labels.failed);
const signal = (rssi: number) =>
  rssi > -65 ? labels.signalStrong : rssi > -82 ? labels.signalMedium : labels.signalWeak;

/** One nearby phone offering an update; the settings menu row's look. */
function OfferRow({ offer, onPress }: { offer: ShareOffer; onPress: () => void }) {
  const { palette, scaled, highContrast, borderWidth } = useAccessibilityTheme();
  const title = fill(labels.offerTitle, { count: offer.count });
  const subtitle = fill(labels.offerSignal, { signal: signal(offer.rssi) });
  return (
    <Pressable
      accessibilityRole="button"
      accessibilityLabel={title}
      accessibilityHint={subtitle}
      onPress={onPress}
      style={({ pressed }) => [
        styles.offer,
        {
          backgroundColor: pressed ? palette.cardShade : palette.card,
          borderColor: highContrast ? palette.ink : palette.cardShade,
          borderWidth,
          boxShadow: `0 2px 10px ${palette.glow}`,
        },
      ]}
    >
      <View style={[styles.tile, { backgroundColor: palette.primary }]} aria-hidden>
        <Icon name="bluetooth" size={20} color={palette.onPrimary} />
      </View>
      <View style={styles.offerTexts}>
        <Text style={[scaled.label, { color: palette.ink }]}>{title}</Text>
        <Text style={[scaled.caption, { color: palette.inkMuted }]}>{subtitle}</Text>
      </View>
      <Icon name="chevronRight" size={18} color={palette.inkMuted} strokeWidth={2.2} />
    </Pressable>
  );
}

export default function UpdateKnowledgeScreen() {
  const router = useRouter();
  const { palette, scaled, borderWidth } = useAccessibilityTheme();
  const locked = useRef(false);
  const pending = useRef<KnowledgeQrSeries>(undefined);
  const [camera, setCamera] = useState(false);
  const [raw, setRaw] = useState('');
  const [patches, setPatches] = useState<KnowledgePatch[]>();
  const [progress, setProgress] = useState<{ read: number; total: number }>();
  const [failure, setFailure] = useState('');
  const [working, setWorking] = useState(false);
  const [done, setDone] = useState('');
  const [bluetooth] = useState(bluetoothShareAvailable);
  const [offers, setOffers] = useState<ShareOffer[]>();
  const stopFind = useRef<() => void>(undefined);

  const endFind = useCallback(() => {
    stopFind.current?.();
    stopFind.current = undefined;
    setOffers(undefined);
  }, []);
  useEffect(() => endFind, [endFind]);

  const scan = useCallback((text: string) => {
    if (locked.current) return;
    locked.current = true;
    setCamera(false);
    setFailure('');
    try {
      const result = collectKnowledgeQr(text.trim(), pending.current);
      setRaw('');
      if ('series' in result) {
        pending.current = result.series;
        setProgress({ read: result.series.parts.size, total: result.series.total });
      } else {
        pending.current = undefined;
        setProgress(undefined);
        setPatches(result.patches);
      }
    } catch (cause) {
      setFailure(message(cause));
    }
  }, []);
  const cameraError = useCallback(() => {
    setCamera(false);
    setFailure(labels.noCamera);
  }, []);
  function resetScan() {
    locked.current = false;
    setFailure('');
  }

  async function findNearby() {
    endFind();
    resetScan();
    setCamera(false);
    setOffers([]);
    // A scan reports each phone several times a second; re-render only when the list changes.
    const heard = (offer: ShareOffer) =>
      setOffers((list) => {
        if (!list) return list;
        const old = list.find((o) => o.address === offer.address);
        if (old && old.session === offer.session && signal(old.rssi) === signal(offer.rssi)) {
          return list;
        }
        return [...list.filter((o) => o.address !== offer.address), offer].sort(
          (a, b) => b.rssi - a.rssi,
        );
      });
    try {
      stopFind.current = await findBluetoothShares(heard);
    } catch (cause) {
      setOffers(undefined);
      setFailure(message(cause));
    }
  }

  async function receive(offer: ShareOffer) {
    endFind();
    setWorking(true);
    setFailure('');
    try {
      setPatches(await receiveBluetoothShare(offer.address));
    } catch (cause) {
      setFailure(message(cause));
    } finally {
      setWorking(false);
    }
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
    } catch (cause) {
      setFailure(message(cause));
    }
  }

  const patch = patches?.length === 1 ? patches[0] : undefined;

  async function apply() {
    if (!patches || working) return;
    setWorking(true);
    setFailure('');
    try {
      const count = await applyKnowledgePatches(patches);
      setDone(
        count === 0
          ? labels.duplicate
          : patches.length > 1
            ? fill(labels.batchUpdated, { count })
            : patch?.op === 'remove'
              ? labels.removed
              : labels.updated,
      );
    } catch (cause) {
      setFailure(message(cause));
    } finally {
      setWorking(false);
    }
  }

  function cancelSeries() {
    pending.current = undefined;
    setProgress(undefined);
    setRaw('');
    resetScan();
  }

  function goToChat() {
    markOnboardingDone();
    router.dismissTo('/');
  }

  const choosing = !patches && !working;
  const details = patch?.op === 'put' ? patch.entry : undefined;
  const applyLabel = patch?.op === 'remove' ? labels.confirm : labels.apply;

  return (
    <ScrollView
      style={{ backgroundColor: palette.card }}
      contentContainerStyle={styles.content}
      keyboardShouldPersistTaps="handled"
    >
      <View style={[styles.badge, { backgroundColor: palette.primary }]} aria-hidden>
        <Icon name="refreshCw" size={26} color={palette.onPrimary} />
      </View>
      <Text accessibilityRole="header" style={[scaled.display, { color: palette.ink }]}>
        {labels.heading}
      </Text>
      <Text style={[scaled.body, { color: palette.inkMuted }]}>{labels.body}</Text>

      {choosing && bluetooth && !offers && (
        <PrimaryButton label={labels.nearby} onPress={() => void findNearby()} />
      )}
      {choosing && offers && (
        <View style={styles.group}>
          <View style={styles.pulse} aria-hidden>
            <SignalPulse size={96} />
          </View>
          <Text
            accessibilityLiveRegion="polite"
            style={[scaled.body, styles.center, { color: palette.inkMuted }]}
          >
            {offers.length ? labels.searching : labels.noOffers}
          </Text>
          {offers.map((offer) => (
            <OfferRow
              key={offer.address + offer.session}
              offer={offer}
              onPress={() => void receive(offer)}
            />
          ))}
          <SecondaryButton label={labels.stopSearch} onPress={endFind} />
        </View>
      )}

      {choosing && progress && (
        <InfoCard
          icon="scanLine"
          title={fill(labels.seriesProgress, { read: progress.read, total: progress.total })}
        >
          <SecondaryButton label={labels.cancelSeries} onPress={cancelSeries} />
        </InfoCard>
      )}

      {choosing && !offers && (
        <View style={styles.group}>
          {bluetooth && (
            <Text style={[scaled.caption, { color: palette.inkMuted }]}>{labels.orQr}</Text>
          )}
          {camera ? (
            <>
              <QrCamera onCode={scan} onError={cameraError} />
              <SecondaryButton label={labels.close} onPress={() => setCamera(false)} />
            </>
          ) : bluetooth ? (
            <SecondaryButton
              label={labels.open}
              onPress={() => {
                resetScan();
                setCamera(true);
              }}
            />
          ) : (
            <PrimaryButton
              label={labels.open}
              onPress={() => {
                resetScan();
                setCamera(true);
              }}
            />
          )}
          <SecondaryButton label={labels.pick} onPress={() => void pickQr()} />
          <TextInput
            style={[
              styles.input,
              scaled.body,
              {
                color: palette.ink,
                borderColor: palette.cardShade,
                borderWidth: borderWidth + 0.5,
              },
            ]}
            accessibilityLabel={labels.code}
            placeholder={labels.paste}
            placeholderTextColor={palette.inkMuted}
            autoCorrect={false}
            autoCapitalize="none"
            value={raw}
            onChangeText={setRaw}
            multiline
            maxLength={QR_LIMIT}
          />
          {!!raw.trim() && (
            <SecondaryButton
              label={labels.read}
              onPress={() => {
                resetScan();
                scan(raw);
              }}
            />
          )}
        </View>
      )}

      {patches && !done && (
        <InfoCard
          icon="bookOpen"
          title={
            patch
              ? patch.op === 'put'
                ? patch.entry.title
                : labels.remove
              : fill(labels.batchSummary, { count: patches.length })
          }
          body={details?.answer}
        >
          {details && (
            <Text style={[scaled.caption, { color: palette.inkMuted }]}>
              {fill(labels.counts, {
                questions: details.questions.length,
                variants: details.variants.length,
              })}
            </Text>
          )}
          {!patch &&
            patches.slice(0, 10).map((item) => (
              <Text key={item.id} style={[scaled.body, { color: palette.ink }]}>
                {item.op === 'put' ? item.entry.title : labels.remove}
              </Text>
            ))}
          <Text style={[scaled.caption, { color: palette.inkMuted }]}>{labels.trust}</Text>
          {!working && (
            <>
              <PrimaryButton label={applyLabel} onPress={() => void apply()} />
              <SecondaryButton
                label={labels.cancel}
                onPress={() => {
                  setPatches(undefined);
                  resetScan();
                }}
              />
            </>
          )}
        </InfoCard>
      )}

      {working && (
        <View style={styles.working}>
          <ActivityIndicator color={palette.primary} />
          <Text style={[scaled.body, { color: palette.inkMuted }]}>
            {patches ? labels.working : labels.receiving}
          </Text>
        </View>
      )}

      {!!failure && <InfoCard icon="triangleAlert" title={labels.failedTitle} body={failure} />}

      {!!done && (
        <InfoCard tone="done" icon="circleCheck" title={done}>
          <PrimaryButton label={labels.back} onPress={goToChat} />
        </InfoCard>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  content: {
    padding: spacing.xl,
    gap: spacing.lg,
    width: '100%',
    maxWidth: 560,
    alignSelf: 'center',
  },
  badge: {
    width: 56,
    height: 56,
    borderRadius: radius.lg,
    alignItems: 'center',
    justifyContent: 'center',
  },
  group: { gap: spacing.md },
  pulse: { alignItems: 'center' },
  center: { textAlign: 'center' },
  offer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
    minHeight: 64,
    padding: spacing.md,
    borderRadius: radius.lg,
  },
  tile: {
    width: 40,
    height: 40,
    borderRadius: radius.md,
    alignItems: 'center',
    justifyContent: 'center',
  },
  offerTexts: { flex: 1, gap: 2 },
  input: { minHeight: 62, borderRadius: radius.md, padding: spacing.md },
  working: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
});
