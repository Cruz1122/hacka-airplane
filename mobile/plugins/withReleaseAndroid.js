// Release-only Android build settings, kept in app.json because android/ is generated (CNG).
// 1. Release builds add .release-models/ (staged by scripts/release-android.sh) as an asset dir, so
//    the knowledge models ship inside the APK; debug builds keep side-loading them. The model files
//    stay uncompressed: llama.rn and onnxruntime read copies, and inflating ~700 MB is slow.
// 2. Release builds sign with the upload key named in ~/.gradle/gradle.properties
//    (TUMAK_UPLOAD_STORE_FILE, TUMAK_UPLOAD_STORE_PASSWORD, TUMAK_UPLOAD_KEY_ALIAS,
//    TUMAK_UPLOAD_KEY_PASSWORD). Without them the release build fails instead of falling back to
//    the debug key.
const { withAppBuildGradle } = require('expo/config-plugins');

const MARK = '// @generated withReleaseAndroid';

const ANDROID_BLOCK = `
    ${MARK}
    sourceSets {
        release {
            assets.srcDirs += ["\${projectRoot}/.release-models"]
        }
    }
    androidResources {
        noCompress += ["gguf", "bin", "onnx", "sha256"]
    }
`;

const RELEASE_SIGNING = `
        release {
            ${MARK}
            if (findProperty('TUMAK_UPLOAD_STORE_FILE')) {
                storeFile file(findProperty('TUMAK_UPLOAD_STORE_FILE'))
                storePassword findProperty('TUMAK_UPLOAD_STORE_PASSWORD')
                keyAlias findProperty('TUMAK_UPLOAD_KEY_ALIAS')
                keyPassword findProperty('TUMAK_UPLOAD_KEY_PASSWORD')
            }
        }`;

function patch(src) {
  if (src.includes(MARK)) return src;
  const replace = (from, to) => {
    if (!src.includes(from))
      throw new Error(`withReleaseAndroid: "${from.trim()}" not found in app/build.gradle`);
    src = src.replace(from, to);
  };
  replace('\nandroid {\n', `\nandroid {\n${ANDROID_BLOCK}`);
  replace(
    "            keyPassword 'android'\n        }\n",
    `            keyPassword 'android'\n        }${RELEASE_SIGNING}\n`,
  );
  // Only the release buildType: it is the second `signingConfig signingConfigs.debug`.
  const releaseAt = src.indexOf('        release {\n', src.indexOf('buildTypes {'));
  const debugUse = src.indexOf('signingConfig signingConfigs.debug', releaseAt);
  if (releaseAt < 0 || debugUse < 0) throw new Error('withReleaseAndroid: release buildType not found');
  src = `${src.slice(0, debugUse)}signingConfig signingConfigs.release${src.slice(debugUse + 'signingConfig signingConfigs.debug'.length)}`;
  return src;
}

module.exports = (config) =>
  withAppBuildGradle(config, (c) => {
    c.modResults.contents = patch(c.modResults.contents);
    return c;
  });
module.exports.patch = patch;
