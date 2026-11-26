// Configuration bottom-sheet panel opened from the right button of CloudNavBar.
// Open saved sources, knowledge administration, the QR knowledge update or the app information.
import Constants from 'expo-constants';
import { router } from 'expo-router';
import { useCallback, useMemo, useRef, useState, type ComponentRef } from 'react';
import { Linking, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';

import { fill, t } from '@/i18n';
import {
  toggleFavoriteSource,
  useFavoriteSources,
  type FavoriteSource,
} from '@/state/favoriteSources';
import { setVerifiedOnly, useVerifiedOnly } from '@/state/verifiedOnly';

import { SwitchRow } from './AccessibilitySheet';
import { BottomSheet } from './BottomSheet';
import { formatSourceLink, SourceFaviconBall, sourcePreviewFor } from './chat/SourceFavicon';
import { Icon, type IconName } from './icons/Icon';
import { KnowledgeAdminPanel } from './KnowledgeAdminPanel';
import { ParkEmblem } from './ParkEmblem';
import { brand, fonts, radius, spacing, type } from './theme/tokens';
import { scaleSize, useAccessibilityTheme } from './useAccessibilityTheme';
import { useReducedMotion } from './useReducedMotion';

const copy = t.settingsPanel;
const sourceCopy = t.chatScreen.sources;
/** Web pages only: a saved source never opens another app or runs a script. */
const WEB_LINK = /^https?:\/\/\S+$/i;

type SettingsView = 'menu' | 'savedSources' | 'knowledgeAdmin' | 'about';

const APP_VERSION = Constants.expoConfig?.version ?? '1.0.0';

export interface SettingsSheetProps {
  open: boolean;
  onClose: () => void;
  bottom?: number;
  reducedMotion?: boolean;
  /** Optional initial subview (useful for tests or deep entry). */
  initialView?: SettingsView;
}

export function SettingsSheet({
  open,
  onClose,
  bottom = 0,
  reducedMotion = false,
  initialView = 'menu',
}: SettingsSheetProps) {
  return (
    <BottomSheetInner
      open={open}
      onClose={onClose}
      bottom={bottom}
      reducedMotion={reducedMotion}
      initialView={initialView}
    />
  );
}

function BottomSheetInner({
  open,
  onClose,
  bottom,
  reducedMotion,
  initialView,
}: Required<SettingsSheetProps>) {
  const [view, setView] = useState<SettingsView>(initialView);
  const [lastRemoved, setLastRemoved] = useState<FavoriteSource | null>(null);

  const handleClose = useCallback(() => {
    setView(initialView);
    setLastRemoved(null);
    onClose();
  }, [initialView, onClose]);

  const handleHardwareBack = useCallback(() => {
    if (view !== 'menu') {
      setView('menu');
      setLastRemoved(null);
      return true;
    }
    return false;
  }, [view]);

  return (
    <BottomSheet
      open={open}
      onClose={handleClose}
      bottom={bottom}
      reducedMotion={reducedMotion}
      onHardwareBack={handleHardwareBack}
    >
      {(close) => (
        <SettingsContent
          view={view}
          onNavigate={(next) => {
            setLastRemoved(null);
            setView(next);
          }}
          lastRemoved={lastRemoved}
          onLastRemoved={setLastRemoved}
          onClose={close}
          reducedMotion={reducedMotion}
        />
      )}
    </BottomSheet>
  );
}

function SettingsContent({
  view,
  onNavigate,
  lastRemoved,
  onLastRemoved,
  onClose,
  reducedMotion,
}: {
  view: SettingsView;
  onNavigate: (next: SettingsView) => void;
  lastRemoved: FavoriteSource | null;
  onLastRemoved: (source: FavoriteSource | null) => void;
  onClose: () => void;
  reducedMotion: boolean;
}) {
  const { palette, scaled, textScale, highContrast, borderWidth } = useAccessibilityTheme();
  const favorites = useFavoriteSources();
  const verifiedOnly = useVerifiedOnly();
  const reduced = useReducedMotion() || reducedMotion;
  const scrollRef = useRef<ComponentRef<typeof ScrollView>>(null);
  const goTop = useCallback(() => scrollRef.current?.scrollTo({ y: 0, animated: false }), []);

  const headerTitle =
    view === 'savedSources'
      ? copy.savedSources.title
      : view === 'knowledgeAdmin'
        ? t.knowledgeAdmin.heading
        : view === 'about'
          ? copy.about.title
          : copy.title;

  const savedSubtitle =
    favorites.length === 0
      ? copy.savedSources.countZero
      : favorites.length === 1
        ? copy.savedSources.countOne
        : fill(copy.savedSources.countMany, { n: favorites.length });

  const handleRemoveFavorite = (item: FavoriteSource) => {
    toggleFavoriteSource({
      id: item.key,
      title: item.title,
      url: item.url,
      date: item.date,
      excerpt: item.excerpt,
    });
    onLastRemoved(item);
  };

  const handleUndoRemove = () => {
    if (!lastRemoved) return;
    toggleFavoriteSource({
      id: lastRemoved.key,
      title: lastRemoved.title,
      url: lastRemoved.url,
      date: lastRemoved.date,
      excerpt: lastRemoved.excerpt,
    });
    onLastRemoved(null);
  };

  return (
    <>
      <View style={styles.header}>
        <View style={styles.titleRow}>
          {view !== 'menu' && (
            <Pressable
              onPress={() => onNavigate('menu')}
              accessibilityRole="button"
              accessibilityLabel={copy.back}
              style={({ pressed }) => [
                styles.backBtn,
                { outlineColor: palette.primary },
                pressed && { backgroundColor: palette.cardShade },
              ]}
            >
              <Icon name="chevronLeft" size={20} color={palette.ink} strokeWidth={2.2} />
            </Pressable>
          )}
          <Text
            style={[styles.title, scaled.title, { color: palette.ink }]}
            accessibilityRole="header"
          >
            {headerTitle}
          </Text>
          {view === 'savedSources' && favorites.length > 0 && (
            <View style={[styles.countBadge, { backgroundColor: palette.cardShade }]} aria-hidden>
              <Text style={[styles.countText, { color: palette.ink }]}>{favorites.length}</Text>
            </View>
          )}
        </View>
        <Pressable
          onPress={onClose}
          accessibilityRole="button"
          accessibilityLabel={copy.close}
          style={({ pressed }) => [
            styles.close,
            { outlineColor: palette.primary },
            pressed && { backgroundColor: palette.cardShade },
          ]}
        >
          <Icon name="x" size={20} color={palette.ink} />
        </Pressable>
      </View>

      <ScrollView
        ref={scrollRef}
        style={styles.list}
        contentContainerStyle={styles.listContent}
        showsVerticalScrollIndicator={false}
        keyboardShouldPersistTaps="handled"
      >
        {view === 'menu' && (
          <>
            <MenuRow
              icon="star"
              iconFilled={favorites.length > 0}
              title={copy.savedSources.title}
              subtitle={savedSubtitle}
              badge={favorites.length > 0 ? String(favorites.length) : undefined}
              onPress={() => onNavigate('savedSources')}
            />
            <View
              style={[
                styles.switchCard,
                {
                  backgroundColor: palette.card,
                  borderColor: highContrast ? palette.ink : palette.cardShade,
                  borderWidth,
                  boxShadow: `0 2px 10px ${palette.glow}`,
                },
              ]}
            >
              <SwitchRow
                title={copy.verifiedOnly.title}
                value={verifiedOnly}
                onToggle={() => setVerifiedOnly(!verifiedOnly)}
                reduced={reduced}
              />
            </View>
            <MenuRow
              icon="bookOpen"
              title={t.knowledgeAdmin.heading}
              subtitle={t.knowledgeAdmin.subtitle}
              onPress={() => onNavigate('knowledgeAdmin')}
            />
            <MenuRow
              icon="camera"
              title={t.qrUpdate.nav}
              subtitle={t.qrUpdate.subtitle}
              onPress={() => {
                onClose();
                router.push('/actualizar');
              }}
            />
            <MenuRow
              icon="info"
              title={copy.about.title}
              subtitle={fill(copy.about.menuSubtitle, { version: APP_VERSION })}
              onPress={() => onNavigate('about')}
            />
          </>
        )}

        {view === 'knowledgeAdmin' && <KnowledgeAdminPanel goTop={goTop} />}

        {view === 'savedSources' && (
          <>
            {lastRemoved && (
              <View
                style={[
                  styles.undoBar,
                  {
                    backgroundColor: palette.cardShade,
                    borderColor: highContrast ? palette.ink : palette.primarySoft,
                    borderWidth,
                  },
                ]}
                accessibilityLiveRegion="polite"
              >
                <Text style={[styles.undoText, scaled.caption, { color: palette.ink }]}>
                  {copy.savedSources.removedNotice}
                </Text>
                <Pressable
                  onPress={handleUndoRemove}
                  hitSlop={6}
                  accessibilityRole="button"
                  accessibilityLabel={copy.savedSources.undo}
                  style={({ pressed }) => [
                    styles.undoBtn,
                    {
                      backgroundColor: pressed ? palette.primaryLight : palette.primary,
                    },
                  ]}
                >
                  <Icon name="rotateCcw" size={13} color={palette.onPrimary} strokeWidth={2.4} />
                  <Text style={[styles.undoBtnText, { color: palette.onPrimary }]}>
                    {copy.savedSources.undo}
                  </Text>
                </Pressable>
              </View>
            )}

            {favorites.length === 0 ? (
              <View
                style={[
                  styles.emptyCard,
                  {
                    backgroundColor: palette.card,
                    borderColor: highContrast ? palette.ink : palette.cardShade,
                    borderWidth,
                    boxShadow: `0 2px 10px ${palette.glow}`,
                  },
                ]}
              >
                <View
                  style={[styles.emptyIcon, { backgroundColor: palette.cardShade }]}
                  aria-hidden
                >
                  <Icon name="star" size={24} color={palette.primary} strokeWidth={2} />
                </View>
                <Text style={[styles.emptyTitle, scaled.label, { color: palette.ink }]}>
                  {copy.savedSources.emptyTitle}
                </Text>
                <Text style={[styles.emptyBody, scaled.body, { color: palette.inkMuted }]}>
                  {copy.savedSources.emptyBody}
                </Text>
              </View>
            ) : (
              favorites.map((item, idx) => (
                <SavedSourceCard
                  key={item.key}
                  source={item}
                  index={idx}
                  onRemove={() => handleRemoveFavorite(item)}
                />
              ))
            )}
          </>
        )}

        {view === 'about' && (
          <>
            <View
              style={[
                styles.heroCard,
                {
                  backgroundColor: palette.card,
                  borderColor: highContrast ? palette.ink : palette.cardShade,
                  borderWidth,
                  boxShadow: `0 2px 10px ${palette.glow}`,
                },
              ]}
            >
              <ParkEmblem size={58} />
              <View style={styles.heroTitleRow}>
                <Text style={[styles.heroTitle, scaled.title, { color: palette.ink }]}>
                  {t.appTitle}
                </Text>
                <View style={[styles.versionPill, { backgroundColor: palette.cardShade }]}>
                  <Text style={[styles.versionText, { color: palette.ink }]}>
                    {fill(copy.about.version, { version: APP_VERSION })}
                  </Text>
                </View>
              </View>
              <Text
                style={[
                  styles.heroPark,
                  {
                    color: palette.primary,
                    fontSize: scaleSize(type.caption.fontSize, textScale),
                    lineHeight: scaleSize(type.caption.lineHeight, textScale),
                  },
                ]}
              >
                {t.parkName}
              </Text>
              <Text style={[styles.heroSummary, scaled.body, { color: palette.inkMuted }]}>
                {copy.about.summary}
              </Text>
            </View>

            <AboutInfoCard
              icon="wifiOff"
              title={copy.about.offlineTitle}
              body={copy.about.offlineBody}
            />
            <AboutInfoCard
              icon="bookOpen"
              title={copy.about.sourcesTitle}
              body={copy.about.sourcesBody}
            />
            <AboutInfoCard
              icon="info"
              title={copy.about.creditsTitle}
              body={copy.about.creditsBody}
            />
          </>
        )}
      </ScrollView>
    </>
  );
}

function MenuRow({
  icon,
  iconFilled = false,
  title,
  subtitle,
  badge,
  onPress,
}: {
  icon: IconName;
  iconFilled?: boolean;
  title: string;
  subtitle: string;
  badge?: string;
  onPress: () => void;
}) {
  const { palette, scaled, highContrast, borderWidth } = useAccessibilityTheme();
  return (
    <Pressable
      onPress={onPress}
      accessibilityRole="button"
      accessibilityLabel={title}
      accessibilityHint={subtitle}
      style={({ pressed }) => [
        styles.menuCard,
        {
          backgroundColor: pressed ? palette.cardShade : palette.card,
          borderColor: highContrast ? palette.ink : palette.cardShade,
          borderWidth,
          boxShadow: `0 2px 10px ${palette.glow}`,
        },
      ]}
    >
      <View
        style={[
          styles.menuIcon,
          { backgroundColor: iconFilled ? palette.primary : palette.cardShade },
        ]}
        aria-hidden
      >
        <Icon
          name={icon}
          size={18}
          color={iconFilled ? palette.onPrimary : palette.ink}
          fill={iconFilled ? palette.onPrimary : 'none'}
          strokeWidth={2}
        />
      </View>
      <View style={styles.menuTexts}>
        <Text style={[styles.menuTitle, scaled.label, { color: palette.ink }]}>{title}</Text>
        <Text style={[styles.menuSubtitle, scaled.caption, { color: palette.inkMuted }]}>
          {subtitle}
        </Text>
      </View>
      {badge ? (
        <View style={[styles.countBadge, { backgroundColor: palette.cardShade }]} aria-hidden>
          <Text style={[styles.countText, { color: palette.ink }]}>{badge}</Text>
        </View>
      ) : null}
      <Icon name="chevronRight" size={18} color={palette.inkMuted} strokeWidth={2.2} />
    </Pressable>
  );
}

function SavedSourceCard({
  source,
  index,
  onRemove,
}: {
  source: FavoriteSource;
  index: number;
  onRemove: () => void;
}) {
  const { palette, textScale, highContrast, borderWidth } = useAccessibilityTheme();
  const url = source.url && WEB_LINK.test(source.url) ? source.url : null;
  const fragment = useMemo(() => formatSourceLink(url ?? undefined), [url]);
  const preview = useMemo(
    () => sourcePreviewFor({ id: source.key, title: source.title, url: source.url }, index),
    [source, index],
  );

  const openLink = () => {
    if (!url) return;
    Linking.openURL(url).catch((e: unknown) =>
      console.warn(`Could not open saved source ${source.key} (${url})`, e),
    );
  };

  return (
    <View
      style={[
        styles.sourceCard,
        {
          backgroundColor: palette.card,
          borderColor: highContrast ? palette.ink : palette.cardShade,
          borderWidth,
          boxShadow: `0 2px 10px ${palette.glow}`,
        },
      ]}
    >
      <View style={styles.cardHead}>
        <SourceFaviconBall preview={preview} size={28} ringColor={palette.cardShade} />
        <View style={styles.cardHeadText}>
          <Text
            style={[
              styles.itemTitle,
              {
                color: palette.ink,
                fontSize: scaleSize(15, textScale),
                lineHeight: scaleSize(20, textScale),
              },
            ]}
          >
            {source.title}
          </Text>
          {fragment ? (
            <Text
              style={[
                styles.linkFragment,
                {
                  color: palette.primary,
                  fontSize: scaleSize(12, textScale),
                  lineHeight: scaleSize(16, textScale),
                },
              ]}
              numberOfLines={1}
              ellipsizeMode="tail"
            >
              {fragment}
            </Text>
          ) : null}
        </View>
      </View>
      {source.excerpt ? (
        <Text
          style={[
            styles.excerpt,
            {
              color: palette.inkMuted,
              fontSize: scaleSize(14, textScale),
              lineHeight: scaleSize(20, textScale),
            },
          ]}
        >
          {source.excerpt}
        </Text>
      ) : null}
      <View style={styles.cardFooter}>
        <View style={styles.dateRow}>
          {source.date ? (
            <>
              <Icon name="clock" size={13} color={palette.inkMuted} strokeWidth={2} />
              <Text style={[styles.date, { color: palette.inkMuted }]}>{source.date}</Text>
            </>
          ) : null}
        </View>
        <View style={styles.actions}>
          <Pressable
            onPress={onRemove}
            hitSlop={4}
            accessibilityRole="button"
            accessibilityState={{ selected: true }}
            accessibilityLabel={fill(sourceCopy.unfavoriteLabel, { title: source.title })}
            style={({ pressed }) => [
              styles.iconAction,
              { backgroundColor: palette.primary },
              pressed && styles.iconActionPressed,
            ]}
          >
            <Icon
              name="star"
              size={16}
              color={palette.onPrimary}
              fill={palette.onPrimary}
              strokeWidth={2}
            />
          </Pressable>
          {url ? (
            <Pressable
              onPress={openLink}
              hitSlop={4}
              accessibilityRole="link"
              accessibilityLabel={fill(sourceCopy.openLabel, { title: source.title })}
              style={({ pressed }) => [
                styles.iconAction,
                { backgroundColor: palette.cardShade },
                pressed && styles.iconActionPressed,
              ]}
            >
              <Icon name="externalLink" size={16} color={palette.ink} strokeWidth={2} />
            </Pressable>
          ) : null}
        </View>
      </View>
    </View>
  );
}

function AboutInfoCard({ icon, title, body }: { icon: IconName; title: string; body: string }) {
  const { palette, scaled, highContrast, borderWidth } = useAccessibilityTheme();
  return (
    <View
      style={[
        styles.aboutCard,
        {
          backgroundColor: palette.card,
          borderColor: highContrast ? palette.ink : palette.cardShade,
          borderWidth,
          boxShadow: `0 2px 10px ${palette.glow}`,
        },
      ]}
    >
      <View style={[styles.menuIcon, { backgroundColor: palette.cardShade }]} aria-hidden>
        <Icon name={icon} size={18} color={palette.ink} strokeWidth={2} />
      </View>
      <View style={styles.aboutTexts}>
        <Text style={[styles.aboutTitle, scaled.label, { color: palette.ink }]}>{title}</Text>
        <Text style={[styles.aboutBody, scaled.caption, { color: palette.inkMuted }]}>{body}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingLeft: 20,
    paddingRight: 10,
    paddingBottom: spacing.md,
    gap: spacing.sm,
  },
  titleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    flexShrink: 1,
  },
  backBtn: {
    width: 44,
    height: 44,
    marginLeft: -12,
    borderRadius: 22,
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    ...type.title,
    color: brand.ink,
    flexShrink: 1,
  },
  countBadge: {
    minWidth: 24,
    height: 22,
    paddingHorizontal: 7,
    borderRadius: radius.pill,
    alignItems: 'center',
    justifyContent: 'center',
  },
  countText: {
    fontFamily: fonts.bold,
    fontSize: 12,
    lineHeight: 16,
    fontVariant: ['tabular-nums'],
  },
  close: {
    width: 44,
    height: 44,
    borderRadius: 22,
    alignItems: 'center',
    justifyContent: 'center',
  },
  list: { flexGrow: 0 },
  listContent: {
    paddingHorizontal: 20,
    paddingTop: spacing.xs,
    paddingBottom: spacing.lg,
    gap: spacing.md,
  },
  menuCard: {
    minHeight: 68,
    borderRadius: 18,
    paddingHorizontal: 14,
    paddingVertical: 12,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  // The switch row brings its own padding and pressed shade; the card only frames it.
  switchCard: {
    borderRadius: 18,
    paddingHorizontal: 14,
    overflow: 'hidden',
  },
  menuIcon: {
    width: 38,
    height: 38,
    borderRadius: 19,
    alignItems: 'center',
    justifyContent: 'center',
  },
  menuTexts: {
    flex: 1,
    gap: 2,
  },
  menuTitle: {
    ...type.label,
  },
  menuSubtitle: {
    ...type.caption,
  },
  undoBar: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: 10,
    borderRadius: 14,
    paddingHorizontal: 12,
    paddingVertical: 8,
  },
  undoText: {
    ...type.caption,
    fontFamily: fonts.medium,
    flex: 1,
  },
  undoBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 5,
    minHeight: 34,
    paddingHorizontal: 12,
    borderRadius: radius.pill,
  },
  undoBtnText: {
    ...type.caption,
    fontFamily: fonts.semibold,
  },
  emptyCard: {
    borderRadius: 18,
    paddingHorizontal: 20,
    paddingVertical: 24,
    alignItems: 'center',
    gap: 8,
  },
  emptyIcon: {
    width: 52,
    height: 52,
    borderRadius: 26,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 4,
  },
  emptyTitle: {
    ...type.label,
    textAlign: 'center',
  },
  emptyBody: {
    ...type.body,
    textAlign: 'center',
  },
  sourceCard: {
    borderRadius: 18,
    paddingHorizontal: 14,
    paddingVertical: 12,
    gap: 10,
  },
  cardHead: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  cardHeadText: {
    flex: 1,
    gap: 2,
  },
  itemTitle: {
    ...type.label,
  },
  linkFragment: {
    ...type.caption,
  },
  excerpt: {
    ...type.body,
  },
  cardFooter: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: spacing.sm,
  },
  dateRow: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 5,
  },
  date: {
    ...type.caption,
    fontSize: 12,
    lineHeight: 16,
    fontVariant: ['tabular-nums'],
  },
  actions: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  iconAction: {
    width: 36,
    height: 36,
    borderRadius: 18,
    alignItems: 'center',
    justifyContent: 'center',
  },
  iconActionPressed: {
    opacity: 0.8,
  },
  heroCard: {
    borderRadius: 18,
    paddingHorizontal: 18,
    paddingVertical: 18,
    alignItems: 'center',
    gap: 6,
  },
  heroTitleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginTop: 4,
  },
  heroTitle: {
    ...type.title,
  },
  versionPill: {
    paddingHorizontal: 9,
    paddingVertical: 3,
    borderRadius: radius.pill,
  },
  versionText: {
    ...type.caption,
    fontFamily: fonts.bold,
    fontSize: 11,
    lineHeight: 15,
    fontVariant: ['tabular-nums'],
  },
  heroPark: {
    fontFamily: fonts.semibold,
    textAlign: 'center',
  },
  heroSummary: {
    ...type.body,
    textAlign: 'center',
    marginTop: 2,
  },
  aboutCard: {
    borderRadius: 18,
    paddingHorizontal: 14,
    paddingVertical: 12,
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 12,
  },
  aboutTexts: {
    flex: 1,
    gap: 3,
  },
  aboutTitle: {
    ...type.label,
  },
  aboutBody: {
    ...type.caption,
  },
});
