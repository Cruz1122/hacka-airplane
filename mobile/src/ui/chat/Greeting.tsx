// The chat's first message, shared by the chat and the station's Tumak sheet. While the knowledge
// chat waits for a station QR it also asks for it, with the scan button inside the bubble.
import { fill, t } from '@/i18n';

import { PrimaryButton } from '../PrimaryButton';
import { PET_NAME } from '../pet/petCore';
import { ChatBubble } from './ChatBubble';

const text = fill(t.chatScreen.greeting, { pet: PET_NAME });
const keywords = t.chatScreen.greetingKeywords.map((keyword) => fill(keyword, { pet: PET_NAME }));

export function Greeting({ locked = false, onScan }: { locked?: boolean; onScan?: () => void }) {
  const asks = locked && onScan !== undefined;
  return (
    <ChatBubble
      role="assistant"
      text={asks ? text + '\n\n' + t.knowledge.lockedIntro : text}
      keywords={keywords}
      action={asks ? <PrimaryButton label={t.knowledge.scan} onPress={onScan} /> : undefined}
    />
  );
}
