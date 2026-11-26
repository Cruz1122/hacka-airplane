import * as ImagePicker from 'expo-image-picker';
import { router } from 'expo-router';
import { useMemo, useState } from 'react';
import { Image, Pressable, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { t } from '@/i18n';
import { Icon } from '@/ui/icons/Icon';
import { MediaRowList, type MediaRowItem } from '@/ui/MediaRowList';
import { brand, spacing, type } from '@/ui/theme/tokens';

import type { StationId } from './stations';
import { trailPhoto } from './trailPhotos';

function goTrail() {
  router.replace('/(tabs)/recorrido');
}

export function StationPage({ id }: { id: StationId }) {
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
          creditUrl: photo.url,
          creditAuthor: photo.author,
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
    <View style={[styles.root, { paddingTop: insets.top }]}>
      <Pressable
        accessibilityRole="button"
        accessibilityLabel={t.trail.back}
        onPress={goTrail}
        hitSlop={8}
        style={styles.back}
      >
        <Icon name="chevronLeft" size={22} color={brand.ink} />
        <Text style={styles.backLabel} selectable={false}>
          {t.trail.back}
        </Text>
      </Pressable>
      <MediaRowList
        items={items}
        contentContainerStyle={{
          paddingHorizontal: spacing.xl,
          paddingTop: spacing.md,
          paddingBottom: insets.bottom + spacing.xl,
        }}
        ListHeaderComponent={
          <Text style={styles.heading} selectable={false}>
            {t.trail.stations[id].name}
          </Text>
        }
        ListFooterComponent={
          <CameraBlock shot={shot} camMsg={camMsg} onTake={takePhoto} />
        }
      />
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
  return (
    <View style={styles.cam}>
      {shot ? (
        <Image
          source={{ uri: shot }}
          style={styles.shot}
          resizeMode="cover"
          accessibilityRole="image"
          accessibilityLabel={t.trail.camera.capturedA11y}
        />
      ) : null}
      <Pressable
        accessibilityRole="button"
        accessibilityLabel={t.trail.camera.take}
        onPress={onTake}
        style={styles.camBtn}
      >
        <Icon name="camera" size={28} color={brand.onPrimary} />
      </Pressable>
      <Text style={styles.camHint} selectable={false}>
        {t.trail.camera.take}
      </Text>
      {camMsg ? (
        <Text style={styles.camHint} selectable={false}>
          {camMsg}
        </Text>
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: brand.card, userSelect: 'none' },
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
