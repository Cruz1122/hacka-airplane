import { Redirect, useLocalSearchParams } from 'expo-router';

import { StationPage } from '@/recorrido/StationPage';
import { isStationId } from '@/recorrido/stations';

export default function EstacionRoute() {
  const { id } = useLocalSearchParams<{ id: string }>();
  if (!id || Array.isArray(id) || !isStationId(id)) {
    return <Redirect href="/recorrido" />;
  }
  return <StationPage id={id} />;
}
