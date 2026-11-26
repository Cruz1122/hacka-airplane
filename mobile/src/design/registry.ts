// The components the /design workshop can open, in nav order. Each id has a lab in ./labs.
import { t } from '@/i18n';
import type { IconName } from '@/ui/icons/Icon';

export type WorkshopId =
  'composer' | 'bubbles' | 'buttons' | 'indicators' | 'group' | 'foundations';

export interface WorkshopItem {
  id: WorkshopId;
  icon: IconName;
  label: string;
  /** Two-digit position shown in the header ("01"). */
  index: string;
}

const ORDER: { id: WorkshopId; icon: IconName }[] = [
  { id: 'composer', icon: 'textCursorInput' },
  { id: 'bubbles', icon: 'messagesSquare' },
  { id: 'buttons', icon: 'squareMousePointer' },
  { id: 'indicators', icon: 'circleDot' },
  { id: 'group', icon: 'users' },
  { id: 'foundations', icon: 'palette' },
];

export const WORKSHOP_ITEMS: WorkshopItem[] = ORDER.map((item, i) => ({
  ...item,
  label: t.dev.workshop.items[item.id],
  index: String(i + 1).padStart(2, '0'),
}));
