// The web build is for previewing the UI (onboarding, Lab, chat). Expo Router bundles
// every route, so native-only modules that touch TurboModules at import time are swapped for stubs
// on web. Native platforms resolve normally.
const fs = require('fs');
const path = require('path');
const { getDefaultConfig } = require('expo/metro-config');

const config = getDefaultConfig(__dirname);

// expo-sqlite on web (settings live in its kv-store): its worker imports a .wasm file and needs
// SharedArrayBuffer, which the browser allows only with these headers (Expo SDK 58 "Web setup").
// Without them the settings read never resolves and the chat stays on "loading model".
config.resolver.assetExts.push('wasm');

// The web chat (src/llm/knowledgeRuntime.web.ts) fetches the e5 GGUF and the index vectors from
// here, plus wllama's wasm. Only these exact names are served: no path from the URL reaches the disk.
// Dev server only; a static `expo export` has no models.
const manifest = require('./assets/data/knowledge/index.json');
const MODELS = path.resolve(__dirname, '../models/knowledge');
const KNOWLEDGE_FILES = {
  [manifest.embedder.file]: path.join(MODELS, manifest.embedder.file),
  [manifest.vectors.file]: path.join(MODELS, manifest.vectors.file),
  'wllama.wasm': path.resolve(__dirname, 'node_modules/@wllama/wllama/esm/wasm/wllama.wasm'),
};

function serveKnowledgeFile(req, res) {
  const name = decodeURIComponent((req.url ?? '').split('?')[0].slice('/knowledge-files/'.length));
  const file = Object.hasOwn(KNOWLEDGE_FILES, name) ? KNOWLEDGE_FILES[name] : null;
  if (!file || !fs.existsSync(file)) {
    res.statusCode = 404;
    res.end(`not served: ${name}`);
    return;
  }
  res.setHeader(
    'Content-Type',
    name.endsWith('.wasm') ? 'application/wasm' : 'application/octet-stream',
  );
  res.setHeader('Content-Length', fs.statSync(file).size);
  fs.createReadStream(file).pipe(res);
}

config.server.enhanceMiddleware = (middleware) => (req, res, next) => {
  res.setHeader('Cross-Origin-Embedder-Policy', 'credentialless');
  res.setHeader('Cross-Origin-Opener-Policy', 'same-origin');
  if (req.url?.startsWith('/knowledge-files/')) return serveKnowledgeFile(req, res);
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
