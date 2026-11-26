import { useFocusEffect } from 'expo-router';
import { useCallback, useEffect, useRef, useState, type ComponentRef } from 'react';
import { AppState, ScrollView, Text, View } from 'react-native';

import { t } from '@/i18n';
import {
  setAdminPassword,
  validAdminPassword,
  verifyAdminPassword,
} from '@/state/knowledgeAdminPassword';
import {
  AdminButton,
  AdminField,
  AdminPanel,
  adminStyles as styles,
} from '@/ui/KnowledgeAdminFields';
import { KnowledgeManager } from '@/ui/KnowledgeManager';

const labels = t.knowledgeAdmin;

export default function KnowledgeAdministration() {
  const scroll = useRef<ComponentRef<typeof ScrollView>>(null);
  const goTop = useCallback(() => scroll.current?.scrollTo({ y: 0, animated: false }), []);
  const [unlocked, setUnlocked] = useState(false);
  const [changing, setChanging] = useState(false);
  const [password, setPassword] = useState('');
  const [next, setNext] = useState('');
  const [repeat, setRepeat] = useState('');
  const [notice, setNotice] = useState('');
  const [error, setError] = useState(false);
  const [working, setWorking] = useState(false);
  const epoch = useRef(0);
  const pending = useRef(false);

  const lock = useCallback(() => {
    epoch.current++;
    setUnlocked(false);
    setChanging(false);
    setPassword('');
    setNext('');
    setRepeat('');
    setNotice('');
    setError(false);
  }, []);
  useFocusEffect(useCallback(() => lock, [lock]));
  useEffect(() => {
    const sub = AppState.addEventListener('change', (state) => {
      if (state === 'background') lock();
    });
    return () => sub.remove();
  }, [lock]);

  function fail(text: string) {
    setNotice(text);
    setError(true);
  }

  async function submit() {
    if (pending.current) return;
    if (changing && !validAdminPassword(next)) return fail(labels.min);
    if (changing && next !== repeat) return fail(labels.match);
    const attempt = epoch.current;
    pending.current = true;
    setWorking(true);
    setNotice('');
    setError(false);
    try {
      const valid = await verifyAdminPassword(password);
      if (attempt !== epoch.current) return;
      if (!valid) return fail(labels.incorrect);
      if (changing) {
        await setAdminPassword(next);
        if (epoch.current !== attempt) return;
        lock();
        setNotice(labels.changed);
      } else {
        setPassword('');
        setUnlocked(true);
      }
    } catch {
      if (attempt === epoch.current) fail(labels.error);
    } finally {
      pending.current = false;
      setWorking(false);
    }
  }

  const submitLabel = working ? labels.checking : changing ? labels.savePassword : labels.unlock;
  const passwordLabel = changing ? labels.current : labels.password;
  function togglePassword() {
    setChanging(!changing);
    setPassword('');
    setNext('');
    setRepeat('');
    setNotice('');
    setError(false);
  }

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
      <Text style={styles.body}>{unlocked ? labels.subtitle : labels.hint}</Text>
      {unlocked && !changing ? (
        <>
          <View style={styles.row}>
            <AdminButton label={labels.change} onPress={togglePassword} />
            <AdminButton label={labels.lock} onPress={lock} />
          </View>
          <KnowledgeManager goTop={goTop} />
        </>
      ) : (
        <AdminPanel>
          <AdminField
            label={passwordLabel}
            secureTextEntry
            autoCapitalize="none"
            autoCorrect={false}
            autoComplete="current-password"
            maxLength={128}
            value={password}
            onChangeText={setPassword}
            onSubmitEditing={() => {
              if (!changing) void submit();
            }}
          />
          {changing && (
            <>
              <AdminField
                label={labels.next}
                secureTextEntry
                autoComplete="new-password"
                autoCapitalize="none"
                autoCorrect={false}
                maxLength={128}
                value={next}
                onChangeText={setNext}
              />
              <AdminField
                label={labels.repeat}
                secureTextEntry
                autoComplete="new-password"
                autoCapitalize="none"
                autoCorrect={false}
                maxLength={128}
                value={repeat}
                onChangeText={setRepeat}
              />
              <Text style={styles.note}>{labels.min}</Text>
            </>
          )}
          <AdminButton
            primary
            label={submitLabel}
            disabled={working}
            onPress={() => void submit()}
          />
          {changing && (
            <AdminButton label={t.qrUpdate.cancel} disabled={working} onPress={togglePassword} />
          )}
        </AdminPanel>
      )}
      {!!notice && (
        <Text accessibilityLiveRegion="polite" style={[styles.body, error && styles.error]}>
          {notice}
        </Text>
      )}
    </ScrollView>
  );
}
