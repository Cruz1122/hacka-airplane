// react-native-web cannot detect a screen reader and its isScreenReaderEnabled always resolves true,
// which would stop every web reply from typing out. Web readers still get the whole reply from the
// bubble's accessible label.
export function useScreenReader(): boolean {
  return false;
}
