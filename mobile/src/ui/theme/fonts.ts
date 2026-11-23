// Font files for expo-font, keyed by the family names in tokens.fonts.
import { fonts } from './tokens';

export const FONT_FILES = {
  [fonts.regular]: require('../../../assets/fonts/Manrope-Regular.ttf'),
  [fonts.medium]: require('../../../assets/fonts/Manrope-Medium.ttf'),
  [fonts.semibold]: require('../../../assets/fonts/Manrope-SemiBold.ttf'),
  [fonts.bold]: require('../../../assets/fonts/Manrope-Bold.ttf'),
  [fonts.display]: require('../../../assets/fonts/BricolageGrotesque-Bold.ttf'),
  [fonts.heading]: require('../../../assets/fonts/BricolageGrotesque-SemiBold.ttf'),
};
