// Knowledge administration panel used inside SettingsSheet's bottom sheet (and the deep-link
// route): eight-cell OTP password gate, password change flow, park access hours/QRs, and entry manager.
import { useCallback, useEffect, useRef, useState } from 'react';
import { AppState, Pressable, StyleSheet, Text, View } from 'react-native';

import { t } from '@/i18n';
import {
  setAdminPassword,
  validAdminPassword,
  verifyAdminPassword,
} from '@/state/knowledgeAdminPassword';

import { Icon } from './icons/Icon';
import { AdminButton, adminStyles } from './KnowledgeAdminFields';
import { KnowledgeManager } from './KnowledgeManager';
import { OTP_PASSWORD_LENGTH, OtpPasswordInput } from './OtpPasswordInput';
import { ParkAccessAdmin } from './ParkAccessAdmin';
import { SecondaryButton } from './SecondaryButton';
import { brand, fonts, radius, spacing, type } from './theme/tokens';
import { useAccessibilityTheme } from './useAccessibilityTheme';

const labels = t.knowledgeAdmin;

export interface KnowledgeAdminPanelProps {
  goTop: () => void;
}

export function KnowledgeAdminPanel({ goTop }: KnowledgeAdminPanelProps) {
  const { palette, scaled, borderWidth } = useAccessibilityTheme();
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
    if (working) return;
    setChanging(!changing);
    setPassword('');
    setNext('');
    setRepeat('');
    setNotice('');
    setError(false);
  }

  return (
    <View style={styles.root}>
      {unlocked && !changing ? (
        <>
          <View style={adminStyles.row}>
            <AdminButton label={labels.change} onPress={togglePassword} />
            <AdminButton label={labels.lock} onPress={lock} />
          </View>
          <ParkAccessAdmin />
          <KnowledgeManager goTop={goTop} />
        </>
      ) : (
        <>
          <OtpPasswordInput
            label={passwordLabel}
            value={password}
            onChangeText={(val) => {
              setPassword(val);
              if (error) {
                setError(false);
                setNotice('');
              }
            }}
            length={OTP_PASSWORD_LENGTH}
            error={error}
            disabled={working}
            autoFocus={!changing}
            autoComplete="current-password"
            onSubmitEditing={() => {
              if (!changing) void submit();
            }}
          />

          {changing && (
            <>
              <OtpPasswordInput
                label={labels.next}
                value={next}
                onChangeText={(val) => {
                  setNext(val);
                  if (error) {
                    setError(false);
                    setNotice('');
                  }
                }}
                length={OTP_PASSWORD_LENGTH}
                error={error}
                disabled={working}
                autoComplete="new-password"
              />
              <OtpPasswordInput
                label={labels.repeat}
                value={repeat}
                onChangeText={(val) => {
                  setRepeat(val);
                  if (error) {
                    setError(false);
                    setNotice('');
                  }
                }}
                length={OTP_PASSWORD_LENGTH}
                error={error}
                disabled={working}
                autoComplete="new-password"
                onSubmitEditing={() => void submit()}
              />
            </>
          )}

          {!!notice && (
            <View
              style={[
                styles.noticeBanner,
                {
                  backgroundColor: error ? palette.wineSoft : palette.cardShade,
                  borderColor: error ? palette.wine : palette.primarySoft,
                  borderWidth,
                },
              ]}
              accessibilityLiveRegion="polite"
            >
              <Icon
                name={error ? 'triangleAlert' : 'circleCheck'}
                size={16}
                color={error ? palette.wine : palette.primary}
                strokeWidth={2.2}
              />
              <Text
                style={[
                  styles.noticeText,
                  scaled.caption,
                  { color: error ? palette.wine : palette.ink },
                ]}
              >
                {notice}
              </Text>
            </View>
          )}

          <View style={styles.actions}>
            <Pressable
              accessibilityRole="button"
              accessibilityLabel={submitLabel}
              accessibilityState={{ disabled: working }}
              disabled={working}
              onPress={() => void submit()}
              style={({ pressed }) => [
                styles.submitBtn,
                {
                  backgroundColor: pressed ? palette.primary : palette.ink,
                  borderColor: palette.primary,
                },
                working && styles.submitDisabled,
              ]}
            >
              <Text style={[styles.submitLabel, scaled.label, { color: palette.onPrimary }]}>
                {submitLabel}
              </Text>
            </Pressable>
            {changing && <SecondaryButton label={t.qrUpdate.cancel} onPress={togglePassword} />}
          </View>
        </>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  root: {
    gap: spacing.lg,
  },
  noticeBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    borderRadius: radius.md,
    paddingHorizontal: 12,
    paddingVertical: 10,
  },
  noticeText: {
    ...type.caption,
    fontFamily: fonts.medium,
    flex: 1,
  },
  actions: {
    gap: spacing.sm,
  },
  submitBtn: {
    minHeight: 48,
    borderRadius: 14,
    borderWidth: 1,
    paddingHorizontal: spacing.lg,
    alignItems: 'center',
    justifyContent: 'center',
  },
  submitDisabled: {
    opacity: 0.6,
  },
  submitLabel: {
    ...type.label,
    color: brand.onPrimary,
  },
});
