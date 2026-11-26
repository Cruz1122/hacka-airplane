import { router } from 'expo-router';
import { memo, useCallback, useEffect, useMemo, useState } from 'react';
import { Animated, BackHandler, Platform, StyleSheet, useWindowDimensions, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { headerScene } from '@/chat/headerScene';
import { chatLayout } from '@/chat/chatLayout';
import { handoffStyles, handoffTiming } from '@/chat/handoff';
import { PetCircle } from '@/chat/PetCircle';
import { onboardingLayout } from '@/onboarding/layout';
import { SceneCanvas } from '@/onboarding/SceneCanvas';
import { markOnboardingDone } from '@/onboarding/launch';
import { OnboardingOverlay } from '@/onboarding/OnboardingOverlay';
import { defaultScene } from '@/onboarding/scene/preset';
import { applyMotions, evaluateTracks } from '@/onboarding/scene/timeline';
import {
  usePlaybackClock,
  usePlaybackFrame,
  useSwipe,
  type PlaybackClock,
  type PlaybackFrame,
} from '@/onboarding/usePlayback';
import { CloudCard } from '@/ui/CloudCard';
import { brand } from '@/ui/theme/tokens';
import { useReducedMotion } from '@/ui/useReducedMotion';

const scene = defaultScene();

const screenOf = (frame: PlaybackFrame) => Math.round(frame.progress);
const wholeFrame = (frame: PlaybackFrame) => frame;

interface Exit {
  /** Idle-motion time the scene and the chat hold during the handoff. */
  time: number | null;
}

/**
 * The only part of the screen that renders on every playback frame: tracks change with progress,
 * idle motions are applied on top.
 */
const OnboardingScene = memo(function OnboardingScene({
  clock,
  exit,
  width,
  height,
}: {
  clock: PlaybackClock;
  exit: Exit | null;
  width: number;
  height: number;
}) {
  const frame = usePlaybackFrame(clock, wholeFrame);
  const tracked = useMemo(() => evaluateTracks(scene, frame.progress), [frame.progress]);
  const time = exit ? exit.time : frame.time;
  const doc = time === null ? tracked : applyMotions(tracked, time);
  return <SceneCanvas doc={doc} width={width} height={height} moving={frame.moving} />;
});

/** Opens the chat; `time` holds its backdrop on the idle-motion pose the onboarding left. */
function openChat(time: number | null) {
  markOnboardingDone();
  router.replace(time === null ? '/' : { pathname: '/', params: { sceneTime: String(time) } });
}

export default function OnboardingScreen() {
  const window = useWindowDimensions();
  const [size, setSize] = useState<{ width: number; height: number } | null>(null);
  const { width, height } = size ?? window;
  const insets = useSafeAreaInsets();
  const layout = onboardingLayout(width, height, insets.bottom);
  const reduced = useReducedMotion();
  // Set when the last screen's button is pressed: the idle clock stops at `time` and the screen
  // turns into the chat (see src/chat/handoff.ts).
  const [exit, setExit] = useState<Exit | null>(null);
  const clock = usePlaybackClock({
    transitionMs: scene.timeline.transitionMs,
    easing: scene.timeline.easing,
    ambient: !exit,
    reduced,
  });
  const swipe = useSwipe(clock, width);
  // The screen renders when the page it rounds to changes; per-frame motion reaches only the scene
  // (OnboardingScene) and the card's native-driven styles (clock.progressValue).
  const index = usePlaybackFrame(clock, screenOf);
  const position = useMemo(() => ({ value: clock.progressValue, index }), [clock, index]);
  const chatDoc = useMemo(
    () => exit && (exit.time === null ? headerScene : applyMotions(headerScene, exit.time)),
    [exit],
  );
  const chat = useMemo(
    () => chatLayout(headerScene, width, height, { top: insets.top, bottom: insets.bottom }),
    [width, height, insets.top, insets.bottom],
  );
  const cardTop = height - layout.card;
  const [t] = useState(() => new Animated.Value(0));
  const move = useMemo(() => handoffStyles(t, chat, cardTop), [t, chat, cardTop]);
  useEffect(() => {
    if (!exit) return;
    // Runs after the chat's backdrop has mounted under the scene, so that first draw happens
    // before the motion starts instead of stalling its first frames.
    const anim = handoffTiming(t);
    anim.start(({ finished }) => finished && openChat(exit.time));
    return () => anim.stop();
  }, [exit, t]);
  const { timeNow, goTo } = clock;
  useEffect(() => {
    if (Platform.OS !== 'android') return;
    const sub = BackHandler.addEventListener('hardwareBackPress', () => {
      if (exit || index <= 0) return false;
      goTo(index - 1);
      return true;
    });
    return () => sub.remove();
  }, [exit, index, goTo]);
  const leave = useCallback(() => {
    if (exit) return;
    const time = timeNow();
    if (reduced) openChat(time);
    else setExit({ time });
  }, [exit, reduced, timeNow]);
  const { r } = chat.circle;
  return (
    <View
      style={styles.root}
      onLayout={(e) =>
        setSize({
          width: e.nativeEvent.layout.width,
          height: e.nativeEvent.layout.height,
        })
      }
      {...(exit ? null : swipe.panHandlers)}
    >
      <Animated.View style={[{ width, height: layout.scene }, exit && move.scene]}>
        {/* The chat's header scene (no volcano, no Pet) waits underneath the onboarding's. */}
        {chatDoc && (
          <View style={StyleSheet.absoluteFill}>
            <SceneCanvas doc={chatDoc} width={width} height={layout.scene} />
          </View>
        )}
        <Animated.View style={[StyleSheet.absoluteFill, exit && move.volcano]}>
          <OnboardingScene clock={clock} exit={exit} width={width} height={layout.scene} />
        </Animated.View>
      </Animated.View>
      {exit && (
        <Animated.View style={[styles.sheet, { top: cardTop }, move.sheet]}>
          <CloudCard width={width} height={height - chat.sheetTop}>
            {null}
          </CloudCard>
        </Animated.View>
      )}
      <Animated.View
        style={[StyleSheet.absoluteFill, exit && move.copy]}
        pointerEvents={exit ? 'none' : 'box-none'}
      >
        <OnboardingOverlay
          doc={scene}
          progress={position}
          width={width}
          cardHeight={layout.card}
          onGo={clock.goTo}
          onDone={leave}
        />
      </Animated.View>
      {exit && (
        <Animated.View
          pointerEvents="none"
          style={[
            styles.circle,
            { left: chat.circle.x - r, top: chat.circle.y - r, width: r * 2, height: r * 2 },
            move.circle,
          ]}
        >
          <PetCircle x={r} y={r} r={r} voice="idle" ready={false} />
        </Animated.View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: brand.sky, overflow: 'hidden' },
  sheet: { position: 'absolute', left: 0 },
  circle: { position: 'absolute' },
});
