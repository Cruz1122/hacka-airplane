// Where a launch lands before the tabs open. Each launch starts on the onboarding, which hands over
// to the chat; a link straight into another tab (nevados://group, /group) opens that tab
// instead. Once the tabs are open nothing sends the user back to the onboarding this session.

/** Chat tab path; every other tab path skips the onboarding. */
const CHAT = '/';

export function needsOnboarding(done: boolean, pathname: string): boolean {
  return !done && pathname === CHAT;
}
