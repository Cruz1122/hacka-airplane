// The web build is for previewing the UI (onboarding, Lab, chat). Expo Router bundles
// every route, so native-only modules that touch TurboModules at import time are swapped for stubs
// on web. Native platforms resolve normally.
const path = require('path');
const { getDefaultConfig } = require('expo/metro-config');

const config = getDefaultConfig(__dirname);

// expo-sqlite on web (settings live in its kv-store): its worker imports a .wasm file and needs
// SharedArrayBuffer, which the browser allows only with these headers (Expo SDK 58 "Web setup").
// Without them the settings read never resolves and the chat stays on "loading model".
config.resolver.assetExts.push('wasm');
config.server.enhanceMiddleware = (middleware) => (req, res, next) => {
  res.setHeader('Cross-Origin-Embedder-Policy', 'credentialless');
  res.setHeader('Cross-Origin-Opener-Policy', 'same-origin');
  middleware(req, res, next);
};

const WEB_STUBS = {
  'llama.rn': path.resolve(__dirname, 'src/web-stubs/llama-rn.ts'),
  'onnxruntime-react-native': path.resolve(__dirname, 'src/web-stubs/onnxruntime-react-native.ts'),
};

const upstream = config.resolver.resolveRequest;
config.resolver.resolveRequest = (context, moduleName, platform) => {
  if (platform === 'web' && WEB_STUBS[moduleName]) {
    return { type: 'sourceFile', filePath: WEB_STUBS[moduleName] };
  }
  return (upstream ?? context.resolveRequest)(context, moduleName, platform);
};

module.exports = config;
