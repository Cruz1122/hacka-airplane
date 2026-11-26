// Group sync: a phone is a guide (sees every synced visitor on a line, alerted when one drifts)
// or a visitor (sees its own link to the guides) over the native BLE beacon radio on Android.
import { useFocusEffect } from 'expo-router';
import { type RefObject, useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  Animated,
  BackHandler,
  Easing,
  Platform,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  useWindowDimensions,
  View,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { guides, members, presence } from '@/core/group/groupState';
import { lane } from '@/core/group/lane';
import type { Alert } from '@/core/group/types';
import { createBleTransport, ensureRadioPermissions } from '@/group/bleTransport';
import { guideSession, newMemberId, visitorSession, type Session } from '@/group/session';
import type { GroupTransport } from '@/group/transport';
import { useGroup } from '@/group/useGroup';
import { fill, t } from '@/i18n';
import { setAlertDistance, useAlertDistance } from '@/state/alertDistance';
import { setPetLook, usePetLooks, wornBy, type PetRole } from '@/state/petLook';
import { AppNavBar } from '@/ui/AppNavBar';
import { NAV_BAR_HEIGHT } from '@/ui/CloudNavBar';
import { AlertDistance } from '@/ui/group/AlertDistance';
import { EmptyLane } from '@/ui/group/EmptyLane';
import { GroupAlertBanner } from '@/ui/group/GroupAlertBanner';
import { GroupLane, laneHeightFor, ZoneLegend } from '@/ui/group/GroupLane';
import { RoleChoices } from '@/ui/group/RoleChoices';
import { SignalPulse } from '@/ui/group/SignalPulse';
import { Icon } from '@/ui/icons/Icon';
import type { PetEmotion } from '@/ui/pet/petCore';
import { Pet } from '@/ui/pet/Pet';
import { SecondaryButton } from '@/ui/SecondaryButton';
import { brand, spacing, type } from '@/ui/theme/tokens';
import { useReducedMotion } from '@/ui/useReducedMotion';

import { GroupRadio } from '../../modules/group-radio';

const MAX_COLUMN = 560;
/** The visitor's error background fades in and out over this long. */
const ERROR_FADE_MS = 300;
const g = t.group;

/** Silent fallback when the native BLE radio module is unavailable (e.g. web preview). */
const IDLE_TRANSPORT: GroupTransport = {
  findSyncingGuides: async () => [],
  start: () => () => {},
  setSyncMode() {},
};

type VisitorState = 'searching' | 'near' | 'away' | 'lost';

/** What a visitor phone shows: its link to the guide, never the whole group. */
const VISITOR_SCREEN: Record<
  Exclude<VisitorState, 'searching'>,
  { title: string; body: string; emotion: PetEmotion; error: boolean }
> = {
  near: {
    title: g.visitor.near,
    body: g.visitor.nearBody,
    emotion: 'happy',
    error: false,
  },
  away: {
    title: g.visitor.away,
    body: g.visitor.awayBody,
    emotion: 'surprised',
    error: true,
  },
  lost: {
    title: g.visitor.lost,
    body: g.visitor.lostBody,
    emotion: 'sad',
    error: true,
  },
};

export default function GroupRoute() {
  const transport = useMemo(
    () =>
      GroupRadio
        ? createBleTransport(GroupRadio, {
            defaultGuideName: g.defaultGuide,
            defaultVisitorName: g.defaultVisitor,
          })
        : IDLE_TRANSPORT,
    [],
  );
  const prepareRadio = useCallback(async (): Promise<string | null> => {
    if (!GroupRadio) return null;
    const perm = await ensureRadioPermissions();
    if (perm !== 'granted') return g.permissionsDenied;
    const caps = GroupRadio.capabilities();
    if (!caps.bluetoothOn) return g.bluetoothOff;
    return null;
  }, []);

  const [session, setSession] = useState<Session>({ kind: 'choosing' });
  const chooseBackRef = useRef<(() => boolean) | null>(null);
  const { width } = useWindowDimensions();
  const insets = useSafeAreaInsets();
  const column = Math.min(width, MAX_COLUMN) - 2 * spacing.lg;
  // Content starts under the cloud bar.
  const below = insets.top + NAV_BAR_HEIGHT + spacing.sm;
  const leaveSession = useCallback(() => setSession({ kind: 'choosing' }), []);

  // Android back steps back one level inside Grupo (session -> role chooser, search -> cancel,
  // customizer -> close) instead of jumping straight to Chat. Scoped to focus so pressing back on
  // the Chat tab never stops an active group session.
  useFocusEffect(
    useCallback(() => {
      if (Platform.OS !== 'android') return;
      const sub = BackHandler.addEventListener('hardwareBackPress', () => {
        if (session.kind !== 'choosing') {
          setSession({ kind: 'choosing' });
          return true;
        }
        return chooseBackRef.current?.() ?? false;
      });
      return () => sub.remove();
    }, [session.kind]),
  );

  return (
    <View style={styles.screen}>
      {session.kind === 'visitor' ? (
        <VisitorView
          key={session.self.id}
          transport={transport}
          session={session}
          onPaired={() => setSession({ ...session, link: 'paired' })}
          onCancel={leaveSession}
          top={below}
          bottom={insets.bottom + spacing.xl}
          width={column}
        />
      ) : (
        <ScrollView
          style={styles.scroll}
          contentContainerStyle={[
            styles.content,
            { paddingTop: below, paddingBottom: insets.bottom + spacing.xl },
          ]}
          keyboardShouldPersistTaps="handled"
        >
          <View style={[styles.column, { width: column }]}>
            {session.kind === 'choosing' && (
              <ChooseRole
                transport={transport}
                prepareRadio={prepareRadio}
                onChosen={setSession}
                backRef={chooseBackRef}
                width={column}
              />
            )}
            {session.kind === 'guide' && (
              <GuideView
                key={session.self.id}
                transport={transport}
                session={session}
                width={column}
                onCancel={leaveSession}
              />
            )}
          </View>
        </ScrollView>
      )}
      <AppNavBar active="group" />
    </View>
  );
}

const PICK_BEAT_MS = 190;
const ENTER_MS = 240;

/** Subtle fade + rise when switching between choosing a role and an active session. */
function useEntrance() {
  const reduced = useReducedMotion();
  const [anim] = useState(() => new Animated.Value(reduced ? 1 : 0));
  useEffect(() => {
    if (reduced) {
      anim.setValue(1);
      return;
    }
    const a = Animated.timing(anim, {
      toValue: 1,
      duration: ENTER_MS,
      easing: Easing.out(Easing.cubic),
      useNativeDriver: Platform.OS !== 'web',
    });
    a.start();
    return () => a.stop();
  }, [anim, reduced]);
  return {
    opacity: anim,
    transform: [
      {
        translateY: anim.interpolate({
          inputRange: [0, 1],
          outputRange: [reduced ? 0 : 14, 0],
        }),
      },
    ],
  };
}

function ChooseRole({
  transport,
  prepareRadio,
  onChosen,
  backRef,
  width,
}: {
  transport: GroupTransport;
  prepareRadio: () => Promise<string | null>;
  onChosen: (s: Session) => void;
  backRef: RefObject<(() => boolean) | null>;
  width: number;
}) {
  const reduced = useReducedMotion();
  const entrance = useEntrance();
  const [name, setName] = useState('');
  const [nameFocused, setNameFocused] = useState(false);
  const [picking, setPicking] = useState<PetRole | null>(null);
  const [searching, setSearching] = useState(false);
  const [editing, setEditing] = useState<PetRole | null>(null);
  const [radioError, setRadioError] = useState<string | null>(null);
  const searchAbort = useRef<AbortController | null>(null);
  const pickTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const looks = usePetLooks();

  const cancelSearch = useCallback(() => {
    if (pickTimer.current !== null) {
      clearTimeout(pickTimer.current);
      pickTimer.current = null;
    }
    searchAbort.current?.abort();
    searchAbort.current = null;
    setPicking(null);
    setSearching(false);
  }, []);

  useEffect(
    () => () => {
      if (pickTimer.current !== null) clearTimeout(pickTimer.current);
      searchAbort.current?.abort();
    },
    [],
  );

  useEffect(() => {
    backRef.current = () => {
      if (searching || picking !== null) {
        cancelSearch();
        return true;
      }
      if (editing !== null) {
        setEditing(null);
        return true;
      }
      return false;
    };
    return () => {
      backRef.current = null;
    };
  }, [backRef, searching, picking, editing, cancelSearch]);

  const chooseGuide = async () => {
    const err = await prepareRadio();
    if (err) {
      setPicking(null);
      setRadioError(err);
      return;
    }
    searchAbort.current?.abort();
    const ctrl = new AbortController();
    searchAbort.current = ctrl;
    setSearching(true);
    transport.findSyncingGuides(ctrl.signal).then(
      (found) => {
        if (ctrl.signal.aborted) return;
        searchAbort.current = null;
        onChosen(guideSession(name.trim() || g.defaultGuide, newMemberId(), found));
      },
      (e: unknown) => {
        if (ctrl.signal.aborted) return;
        console.warn('Looking for syncing guides failed; staying on the role chooser.', e);
        searchAbort.current = null;
        setPicking(null);
        setSearching(false);
      },
    );
  };

  const chooseVisitor = async () => {
    const err = await prepareRadio();
    if (err) {
      setPicking(null);
      setRadioError(err);
      return;
    }
    onChosen(visitorSession(name.trim() || g.defaultVisitor, newMemberId()));
  };

  const handleChoose = (role: PetRole) => {
    if (searching || picking !== null) return;
    setRadioError(null);
    setEditing(null);
    const run = () => {
      if (role === 'guide') void chooseGuide();
      else void chooseVisitor();
    };
    if (reduced) {
      run();
      return;
    }
    setPicking(role);
    pickTimer.current = setTimeout(() => {
      pickTimer.current = null;
      run();
    }, PICK_BEAT_MS);
  };

  const busy = searching || picking !== null;

  return (
    <Animated.View style={[styles.block, styles.fill, entrance]}>
      <View style={[styles.heading, styles.chooseHeading]}>
        <Text style={styles.display} accessibilityRole="header">
          {g.chooseTitle}
        </Text>
        <Text style={styles.body}>{g.chooseBody}</Text>
      </View>
      <View style={[styles.inputShell, nameFocused && styles.inputShellFocused]}>
        <TextInput
          value={name}
          onChangeText={setName}
          editable={!busy}
          onFocus={() => setNameFocused(true)}
          onBlur={() => setNameFocused(false)}
          placeholder={g.namePlaceholder}
          placeholderTextColor={brand.inkMuted}
          accessibilityLabel={g.nameLabel}
          accessibilityHint={g.nameHint}
          autoCapitalize="words"
          returnKeyType="done"
          maxLength={24}
          style={styles.input}
        />
      </View>
      {radioError && (
        <Text
          style={styles.errorText}
          accessibilityRole="alert"
          accessibilityLiveRegion="assertive"
        >
          {radioError}
        </Text>
      )}
      <RoleChoices
        looks={looks}
        onLookChange={setPetLook}
        onChoose={handleChoose}
        width={width}
        disabled={busy}
        selected={picking}
        editing={editing}
        onEditingChange={setEditing}
      />
      {searching && (
        <View style={styles.searching} accessibilityLiveRegion="polite">
          <View style={styles.searchingRow}>
            <SignalPulse size={36} />
            <Text style={styles.label}>{g.searchingGuides}</Text>
          </View>
          <SecondaryButton
            label={g.cancelSearch}
            hint={g.cancelSearchHint}
            onPress={cancelSearch}
          />
        </View>
      )}
    </Animated.View>
  );
}

function GuideView({
  transport,
  session,
  width,
  onCancel,
}: {
  transport: GroupTransport;
  session: Extract<Session, { kind: 'guide' }>;
  width: number;
  /** Ends the session; unmounting this view stops the radio. */
  onCancel: () => void;
}) {
  const entrance = useEntrance();
  const { height } = useWindowDimensions();
  const alertMeters = useAlertDistance();
  // A guide's phone always syncs: visitors who bring their phone close join at any time.
  const { state, alerts } = useGroup(transport, session.self, true, alertMeters);
  const look = usePetLooks().guide;
  const view = useMemo(() => lane(state, session.self.id), [state, session.self.id]);
  const names = useMemo(() => new Map(members(state).map((m) => [m.id, m.name])), [state]);
  const nameOf = (a: Alert) => names.get(a.id) ?? '';
  const count = view.dots.length;
  if (count === 0) {
    // Nobody to watch yet: the waiting Pet alone, centred under the bar, and a way back.
    return (
      <Animated.View style={[styles.centered, entrance]}>
        <GroupAlertBanner alerts={alerts} nameOf={nameOf} />
        <EmptyLane wears={wornBy(look, 'guide')} onCancel={onCancel} />
      </Animated.View>
    );
  }
  const laneHeight = Math.max(
    laneHeightFor(count, view.bottom !== null),
    // What the screen leaves under the bar, the banner, the count and the distance card.
    Math.min(640, Math.max(360, height - 420)),
  );
  return (
    <Animated.View style={[styles.block, entrance]}>
      <GroupAlertBanner alerts={alerts} nameOf={nameOf} />
      <View style={styles.countRow} accessible accessibilityLiveRegion="polite">
        <Icon name="users" size={18} color={brand.ink} />
        <Text style={styles.label}>
          {count === 1 ? g.visitorsOne : fill(g.visitorsMany, { n: count })}
        </Text>
      </View>
      <AlertDistance meters={alertMeters} onChange={setAlertDistance} />
      <View style={styles.lanePanel}>
        <GroupLane
          lane={view}
          selfId={session.self.id}
          selfWears={wornBy(look, 'guide')}
          width={width - 2}
          height={laneHeight}
        />
      </View>
      <ZoneLegend />
      <View style={styles.guideFooter}>
        <SecondaryButton label={g.leaveGroup} hint={g.leaveGroupHint} onPress={onCancel} />
      </View>
    </Animated.View>
  );
}

/** Fades 0..1 with the visitor's error state, at once under reduced motion. */
function useErrorFade(on: boolean) {
  const reduced = useReducedMotion();
  const [shown] = useState(() => new Animated.Value(on ? 1 : 0));
  useEffect(() => {
    if (reduced) return shown.setValue(on ? 1 : 0);
    const a = Animated.timing(shown, {
      toValue: on ? 1 : 0,
      duration: ERROR_FADE_MS,
      easing: Easing.inOut(Easing.quad),
      useNativeDriver: Platform.OS !== 'web',
    });
    a.start();
    return () => a.stop();
  }, [on, reduced, shown]);
  return shown;
}

/** Full-screen wine wash behind the visitor's error states. */
function ErrorBackdrop({ shown }: { shown: Animated.Value }) {
  return (
    <Animated.View
      pointerEvents="none"
      style={[StyleSheet.absoluteFill, styles.errorWash, { opacity: shown }]}
    />
  );
}

function VisitorView({
  transport,
  session,
  onPaired,
  onCancel,
  top,
  bottom,
  width,
}: {
  transport: GroupTransport;
  session: Extract<Session, { kind: 'visitor' }>;
  onPaired: () => void;
  /** Ends the visitor session; unmounting this view stops the radio and NFC reader. */
  onCancel: () => void;
  top: number;
  bottom: number;
  width: number;
}) {
  const entrance = useEntrance();
  const { state } = useGroup(transport, session.self, false);
  const worn = wornBy(usePetLooks().visitor, 'visitor');
  const guide = guides(state)[0];
  const paired = session.link === 'paired';
  useEffect(() => {
    if (guide && !paired) onPaired();
  }, [guide, paired, onPaired]);
  const p = presence(state, session.self.id);
  const zone = p.kind === 'tracked' ? p.zone : 'unseen';
  const shown: VisitorState = !paired
    ? 'searching'
    : zone === 'near'
      ? 'near'
      : zone === 'unseen'
        ? 'lost'
        : 'away';
  const screen = shown === 'searching' ? null : VISITOR_SCREEN[shown];
  const error = !!screen?.error;
  const errorFade = useErrorFade(error);
  return (
    <View style={StyleSheet.absoluteFill}>
      <ErrorBackdrop shown={errorFade} />
      <ScrollView
        style={styles.scroll}
        contentContainerStyle={[styles.content, { paddingTop: top, paddingBottom: bottom }]}
      >
        <View style={[styles.column, { width }]}>
          <Animated.View style={[styles.visitorCenter, entrance]}>
            <View
              style={styles.hero}
              aria-hidden
              accessibilityElementsHidden
              importantForAccessibility="no-hide-descendants"
            >
              {screen ? (
                <View style={styles.petCircle}>
                  <View pointerEvents="none" style={[StyleSheet.absoluteFill, styles.petRim]} />
                  {/* The circle, rim included, turns wine with the background. */}
                  <Animated.View
                    pointerEvents="none"
                    style={[
                      StyleSheet.absoluteFill,
                      styles.petCircleError,
                      { opacity: errorFade },
                    ]}
                  />
                  <Pet
                    size={118}
                    emotion={screen.emotion}
                    accessory={worn.accessory}
                    tint={worn.tint}
                  />
                </View>
              ) : (
                <SignalPulse size={160} />
              )}
            </View>
            <View
              style={[styles.heading, styles.visitorHeading]}
              accessibilityLiveRegion={error ? 'assertive' : 'polite'}
            >
              <View style={styles.titleRow}>
                {error && <Icon name="triangleAlert" size={26} color={brand.wine} />}
                <Text
                  style={[styles.display, error && styles.displayError]}
                  accessibilityRole={error ? 'alert' : 'header'}
                >
                  {screen ? screen.title : g.visitor.searchingTitle}
                </Text>
              </View>
              <Text style={[styles.body, error && styles.bodyError]}>
                {screen ? screen.body : g.visitor.searchingBody}
              </Text>
            </View>
            <SecondaryButton
              label={paired ? g.leaveGroup : g.cancelSearch}
              hint={paired ? g.leaveGroupHint : g.cancelSearchHint}
              onPress={onCancel}
            />
          </Animated.View>
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: brand.card },
  scroll: { flex: 1 },
  // Grows to the screen so empty/visitor views centre vertically and role cards share spare height.
  content: { flexGrow: 1, alignItems: 'center' },
  column: { flexGrow: 1, gap: spacing.lg },
  fill: { flexGrow: 1 },
  chooseHeading: { marginTop: spacing.xl + spacing.xs },
  block: { gap: spacing.lg },
  heading: { gap: spacing.sm },
  visitorHeading: { maxWidth: 320, alignItems: 'center' },
  hero: { alignItems: 'center' },
  visitorCenter: {
    flexGrow: 1,
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.xl,
  },
  // The Pet is drawn in card colors, so it sits in a teal circle as on the chat sheet.
  petCircle: {
    width: 160,
    height: 160,
    borderRadius: 80,
    alignItems: 'center',
    justifyContent: 'center',
    overflow: 'hidden',
    backgroundColor: brand.primary,
  },
  petRim: { borderRadius: 80, borderWidth: 4, borderColor: brand.primarySoft },
  // The card-colored Pet on wine is as readable as card on wine text (10.8:1).
  petCircleError: { borderRadius: 80, backgroundColor: brand.wine },
  centered: { flexGrow: 1, alignItems: 'center', justifyContent: 'center', gap: spacing.lg },
  display: { ...type.display, color: brand.ink, textAlign: 'center', flexShrink: 1 },
  displayError: { color: brand.wine },
  titleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.sm,
  },
  body: { ...type.body, color: brand.inkMuted, textAlign: 'center' },
  // inkMuted on wineSoft is 4.3:1, under AA for body text; ink is 7.8:1.
  bodyError: { color: brand.ink },
  errorWash: { backgroundColor: brand.wineSoft },
  // Shares RoleCard's soft bordered surface and glow so the input belongs to the same screen.
  inputShell: {
    borderRadius: 24,
    borderWidth: 2,
    borderColor: brand.primarySoft,
    backgroundColor: brand.card,
    boxShadow: `0 4px 14px ${brand.glow}`,
    outlineColor: brand.primary,
    outlineStyle: 'solid',
    outlineWidth: 0,
    outlineOffset: 3,
  },
  inputShellFocused: { borderColor: brand.primary, outlineWidth: 2 },
  input: {
    ...type.label,
    color: brand.ink,
    minHeight: 54,
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.md,
    textAlignVertical: 'center',
    outlineWidth: 0,
  },
  errorText: { ...type.caption, color: brand.alert, textAlign: 'center' },
  label: { ...type.label, color: brand.ink },
  countRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  lanePanel: {
    borderRadius: 28,
    borderWidth: 1,
    borderColor: brand.cardShade,
    backgroundColor: brand.card,
  },
  guideFooter: { alignItems: 'center', paddingTop: spacing.xs },
  searching: { alignItems: 'center', justifyContent: 'center', gap: spacing.md },
  searchingRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.sm,
  },
});
