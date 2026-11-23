import { router } from 'expo-router';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { Animated, StyleSheet, useWindowDimensions, View } from 'react-native';
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
import { usePlayback, useSwipe } from '@/onboarding/usePlayback';
import { CloudCard } from '@/ui/CloudCard';
import { brand } from '@/ui/theme/tokens';
import { useReducedMotion } from '@/ui/useReducedMotion';

const scene = defaultScene();

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
  const [exit, setExit] = useState<{ time: number | null } | null>(null);
  const play = usePlayback({
    transitionMs: scene.timeline.transitionMs,
    easing: scene.timeline.easing,
    ambient: !exit,
    reduced,
  });
  const swipe = useSwipe(play, width);
  // Tracks change only with progress; idle motions are applied on top every frame. The overlay
  // gets the tracked doc so the idle clock does not re-render the card.
  const tracked = useMemo(() => evaluateTracks(scene, play.progress), [play.progress]);
  const shown = play.time === null ? tracked : applyMotions(tracked, play.time);
  const frozen = useMemo(
    () => exit && (exit.time === null ? tracked : applyMotions(tracked, exit.time)),
    [exit, tracked],
  );
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
  // Reads the idle time through timeNow so the overlay's props stay the same on idle frames.
  const { timeNow } = play;
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
          <SceneCanvas
            doc={frozen ?? shown}
            width={width}
            height={layout.scene}
            moving={play.moving}
          />
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
          doc={tracked}
          progress={play.progress}
          width={width}
          cardHeight={layout.card}
          onGo={play.goTo}
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
