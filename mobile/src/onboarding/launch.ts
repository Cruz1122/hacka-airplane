// Every launch opens on the onboarding (the user's call): the chat route redirects there until the
// onboarding hands over. Module state, so it resets with each app start (and each JS reload).
let handedOver = false;

export const onboardingDone = (): boolean => handedOver;

export function markOnboardingDone(): void {
  handedOver = true;
}
