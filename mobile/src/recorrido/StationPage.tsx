import * as ImagePicker from 'expo-image-picker';
import { router } from 'expo-router';
import { useMemo, useState } from 'react';
import { Image, Pressable, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { t } from '@/i18n';
import { Icon } from '@/ui/icons/Icon';
import { MediaRowList, type MediaRowItem } from '@/ui/MediaRowList';
import { brand, spacing, type } from '@/ui/theme/tokens';
import { useAccessibilityTheme } from '@/ui/useAccessibilityTheme';

import { STAGE_FAB, StageTumak } from './StageTumak';
import type { StationId } from './stations';
import { trailPhoto } from './trailPhotos';

function goTrail() {
  router.replace('/recorrido');
}

export function StationPage({ id }: { id: StationId }) {
  const { palette, scaled } = useAccessibilityTheme();
  const insets = useSafeAreaInsets();
  const paras = t.trail.pages[id];
  const [shot, setShot] = useState<string | null>(null);
  const [camMsg, setCamMsg] = useState<string | null>(null);

  const items = useMemo<MediaRowItem[]>(
    () =>
      paras.map((page, i) => {
        const photo = trailPhoto(id, i);
        return {
          image: photo.source,
          subtitle: page.subtitle,
          description: page.body,
          creditAuthor: photo.author,
          creditLicense: photo.license,
          creditUrl: photo.url,
        };
      }),
    [id, paras],
  );

  const takePhoto = async () => {
    try {
      const permission = await ImagePicker.requestCameraPermissionsAsync();
      if (!permission.granted) {
        setCamMsg(t.trail.camera.denied);
        return;
      }
      const result = await ImagePicker.launchCameraAsync({
        mediaTypes: ['images'],
        quality: 0.8,
      });
      if (result.canceled) return;
      const uri = result.assets[0]?.uri;
      if (!uri) {
        setCamMsg(t.trail.camera.unavailable);
        return;
      }
      setShot(uri);
      setCamMsg(null);
    } catch {
      setCamMsg(t.trail.camera.unavailable);
    }
  };

  return (
    <View style={[styles.root, { backgroundColor: palette.card, paddingTop: insets.top }]}>
      <Pressable
        accessibilityRole="button"
        accessibilityLabel={t.trail.back}
        onPress={goTrail}
        hitSlop={8}
        style={styles.back}
      >
        <Icon name="chevronLeft" size={22} color={palette.ink} />
        <Text style={[styles.backLabel, scaled.label, { color: palette.ink }]} selectable={false}>
          {t.trail.back}
        </Text>
      </Pressable>
      <MediaRowList
        items={items}
        contentContainerStyle={{
          paddingHorizontal: spacing.xl,
          paddingTop: spacing.md,
          paddingBottom: insets.bottom + spacing.xl + STAGE_FAB,
        }}
        ListHeaderComponent={
          <Text style={[styles.heading, scaled.display, { color: palette.ink }]} selectable>
            {t.trail.stations[id].name}
          </Text>
        }
        ListFooterComponent={
          <>
            <Text style={[styles.source, scaled.caption, { color: palette.inkMuted }]} selectable>
              {t.trail.source}
            </Text>
            <CameraBlock shot={shot} camMsg={camMsg} onTake={takePhoto} />
          </>
        }
      />
      <StageTumak id={id} insetBottom={insets.bottom + spacing.md} />
    </View>
  );
}

function CameraBlock({
  shot,
  camMsg,
  onTake,
}: {
  shot: string | null;
  camMsg: string | null;
  onTake: () => void;
}) {
  const { palette, scaled } = useAccessibilityTheme();
  return (
    <View style={styles.cam}>
      {shot ? (
        <Image
          source={{ uri: shot }}
          style={[styles.shot, { backgroundColor: palette.cardShade }]}
          resizeMode="cover"
          accessibilityRole="image"
          accessibilityLabel={t.trail.camera.capturedA11y}
        />
      ) : null}
      <Pressable
        accessibilityRole="button"
        accessibilityLabel={t.trail.camera.take}
        onPress={onTake}
        style={[styles.camBtn, { backgroundColor: palette.primary }]}
      >
        <Icon name="camera" size={28} color={palette.onPrimary} />
      </Pressable>
      <Text
        style={[styles.camHint, scaled.caption, { color: palette.inkMuted }]}
        selectable={false}
      >
        {t.trail.camera.take}
      </Text>
      {camMsg ? (
        <Text
          style={[styles.camHint, scaled.caption, { color: palette.inkMuted }]}
          selectable={false}
        >
          {camMsg}
        </Text>
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: brand.card },
  back: {
    minHeight: 44,
    paddingHorizontal: spacing.md,
    flexDirection: 'row',
    alignItems: 'center',
    alignSelf: 'flex-start',
    gap: spacing.xs,
  },
  backLabel: { ...type.label, color: brand.ink },
  heading: {
    ...type.display,
    color: brand.ink,
    textAlign: 'center',
    marginBottom: spacing.lg,
  },
  source: { ...type.caption, color: brand.inkMuted, marginTop: spacing.lg },
  cam: {
    marginTop: spacing.xl,
    alignItems: 'center',
    gap: spacing.sm,
  },
  shot: {
    width: '100%',
    aspectRatio: 1,
    marginBottom: spacing.sm,
    backgroundColor: brand.cardShade,
  },
  camBtn: {
    width: 72,
    height: 72,
    borderRadius: 36,
    backgroundColor: brand.primary,
    alignItems: 'center',
    justifyContent: 'center',
  },
  camHint: { ...type.caption, color: brand.inkMuted, textAlign: 'center' },
});
