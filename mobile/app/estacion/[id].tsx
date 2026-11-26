import { Redirect, useLocalSearchParams } from 'expo-router';

import { isStationUnlocked } from '@/core/access/parkAccess';
import { StationPage } from '@/recorrido/StationPage';
import { isStationId } from '@/recorrido/stations';
import { useParkAccess } from '@/state/parkAccess';

export default function EstacionRoute() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const { access } = useParkAccess();
  if (!id || Array.isArray(id) || !isStationId(id) || !isStationUnlocked(access, id)) {
    return <Redirect href="/recorrido" />;
  }
  return <StationPage id={id} />;
}
