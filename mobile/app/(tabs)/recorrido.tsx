import { Redirect } from 'expo-router';

import { onboardingDone } from '@/onboarding/launch';
import { RecorridoScreen } from '@/recorrido/RecorridoScreen';

export default function RecorridoRoute() {
  if (!onboardingDone()) return <Redirect href="/onboarding" />;
  return <RecorridoScreen />;
}
