// Idempotent fix for onnxruntime-react-native 1.24.3 under Gradle 9 (runs on npm postinstall).
// 1. Gradle 9 removed org.gradle.util.VersionNumber; the check only matters for RN < 0.71 (we are on 0.88).
// 2. Pin the native ORT aar to the JS package version instead of `latest.integration`.
// 3. Drop the legacy unimodule.json: Expo autolinking treats the package as an Expo module because of
//    it and leaves OnnxruntimePackage out of PackageList, so NativeModules.Onnxruntime is null.
const fs = require('fs');
const path = require('path');

const pkgDir = path.join(__dirname, '..', 'node_modules', 'onnxruntime-react-native');
const unimodule = path.join(pkgDir, 'unimodule.json');
if (fs.existsSync(unimodule)) {
  fs.unlinkSync(unimodule);
  console.log('patch-ort: removed', unimodule);
}
const file = path.join(__dirname, '..', 'node_modules', 'onnxruntime-react-native', 'android', 'build.gradle');
if (!fs.existsSync(file)) process.exit(0);
const version = require('onnxruntime-react-native/package.json').version;
const before = fs.readFileSync(file, 'utf8');
const after = before
  .replace(/if \(VersionNumber\.parse\(REACT_NATIVE_VERSION\) < VersionNumber\.parse\("0\.71"\)\)/, 'if (false) /* patched: RN >= 0.71 */')
  .replace(/(com\.microsoft\.onnxruntime:onnxruntime-android(?:-qnn)?):latest\.integration@aar/g, `$1:${version}@aar`);
if (after !== before) {
  fs.writeFileSync(file, after);
  console.log('patch-ort: patched', file);
}
