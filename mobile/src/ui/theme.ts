import { useColorScheme } from 'react-native';

import { colors } from './theme/tokens';

export function useColors() {
  return useColorScheme() === 'dark' ? colors.dark : colors.light;
}
