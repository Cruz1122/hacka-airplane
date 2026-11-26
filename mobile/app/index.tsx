import * as ImagePicker from 'expo-image-picker';
import { Redirect, router, useLocalSearchParams } from 'expo-router';
import { useCallback, useMemo, useRef, useState } from 'react';
import { Alert, Platform } from 'react-native';

import { ChatView, type ChatModel } from '@/chat/ChatView';
import { t } from '@/i18n';
import { onboardingDone } from '@/onboarding/launch';
import { toChatRows } from '@/state/knowledgeRows';
import { useKnowledge } from '@/state/useKnowledge';
import { classifyPhoto } from '@/vision/classifyPhoto';

// The knowledge engine has no routing steps or live draft; ChatView's debug props stay empty.
const NO_STEPS: never[] = [];

export default function ChatRoute() {
  // Each launch starts on the onboarding, which replaces itself with this route when it ends.
  if (!onboardingDone()) return <Redirect href="/onboarding" />;
  return <ChatScreen />;
}

function ChatScreen() {
  const { rows, ask, askPhoto, reset, busy, status } = useKnowledge();
  const picking = useRef(false);
  const [photoUri, setPhotoUri] = useState<string>();
  const removePhoto = () => {
    if (Platform.OS === 'web' && photoUri?.startsWith('blob:')) URL.revokeObjectURL(photoUri);
    setPhotoUri(undefined);
  };
  const pickPhoto = async (camera: boolean) => {
    if (picking.current) return;
    picking.current = true;
    try {
      if (camera && !(await ImagePicker.requestCameraPermissionsAsync()).granted) {
        Alert.alert('Cámara sin permiso', 'Puedes elegir una foto de la galería.');
        return;
      }
      const options: ImagePicker.ImagePickerOptions = { mediaTypes: ['images'], quality: 0.75 };
      const result = camera
        ? await ImagePicker.launchCameraAsync(options)
        : await ImagePicker.launchImageLibraryAsync(options);
      if (!result.canceled) {
        removePhoto();
        setPhotoUri(result.assets[0].uri);
      }
    } catch {
      Alert.alert('Foto no disponible', 'Vuelve a abrir la cámara o la galería.');
    } finally {
      picking.current = false;
    }
  };
  const onPhoto = () => {
    if (Platform.OS === 'web') {
      void pickPhoto(false);
      return;
    }
    Alert.alert('Identificar una foto', undefined, [
      { text: 'Cancelar', style: 'cancel' },
      { text: 'Galería', onPress: () => void pickPhoto(false) },
      { text: 'Cámara', onPress: () => void pickPhoto(true) },
    ]);
  };
  // Set by the onboarding so the header continues its last frame exactly.
  const { sceneTime } = useLocalSearchParams<{ sceneTime?: string }>();
  const onSend = useCallback((text: string) => {
    if (photoUri) {
      setPhotoUri(undefined);
      void askPhoto(photoUri, text, () => classifyPhoto(photoUri));
    } else {
      void ask(text);
    }
  }, [ask, askPhoto, photoUri]);
  const messages = useMemo(() => toChatRows(rows, t.knowledge.error), [rows]);
  // Degraded still answers urgent questions (safety rules need no model), so sending stays on.
  const model: ChatModel = { id: 'e5-base', status: status === 'loading' ? 'loading' : 'ready' };
  return (
    <ChatView
      messages={messages}
      busy={busy}
      draft=""
      model={model}
      steps={NO_STEPS}
      state=""
      sceneTime={sceneTime ? Number(sceneTime) : null}
      fadeIn={sceneTime !== undefined}
      onSend={onSend}
      onPhoto={onPhoto}
      photoUri={photoUri}
      onRemovePhoto={removePhoto}
      onReset={() => {
        removePhoto();
        reset();
      }}
      onSettings={() => router.push('/settings')}
      onHistory={() => router.push('/history')}
    />
  );
}
