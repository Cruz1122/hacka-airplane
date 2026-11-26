// Native fallback required by Expo Router for app/lab.web.tsx. The Lab is a desktop web editor.
import { Link } from 'expo-router';
import { StyleSheet, Text, View } from 'react-native';

export default function LabNative() {
  return (
    <View style={styles.root}>
      <Text style={styles.text}>
        El Onboarding Lab corre en el navegador: `npx expo start --web` y abre /lab.
      </Text>
      <Link href="/onboarding" style={styles.link}>
        Ver el onboarding
      </Link>
    </View>
  );
}

const styles = StyleSheet.create({
  root: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 24,
    gap: 16,
  },
  text: { fontSize: 16, textAlign: 'center' },
  link: { fontSize: 16, color: '#293D70', fontWeight: '700' },
});
