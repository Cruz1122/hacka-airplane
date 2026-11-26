// Release APKs carry the knowledge model files as uncompressed Android assets under models/
// (plugins/withBundledModels.js, staged by scripts/release-android.sh). llama.rn and onnxruntime
// need real file paths, so the first launch copies them into the app files dir, where
// findSideLoaded looks. Debug builds carry no models/ assets: they keep the side-loaded files.
import { File, Paths } from 'expo-file-system';

const ASSET_DIR = 'asset:///models';
/** Written by the release script: one line per bundled file, `<sha256>  <name>`. */
const STAMP = 'models.sha256';

let inFlight: Promise<void> | null = null;

/**
 * Copies the bundled model files into the files dir when the APK's stamp differs from the last
 * copy (new install or new release), so stale side-loaded or previous-release files are replaced
 * even when their byte size did not change. One copy per process however many callers wait.
 */
export function ensureBundledModels(names: readonly string[]): Promise<void> {
  inFlight ??= copyBundled(names).catch((cause: unknown) => {
    inFlight = null;
    throw new Error('copying the bundled model files failed', { cause });
  });
  return inFlight;
}

async function copyBundled(names: readonly string[]): Promise<void> {
  const stampAsset = new File(`${ASSET_DIR}/${STAMP}`);
  if (!stampAsset.exists) return; // debug build: side-loaded files only
  const stamp = await stampAsset.text();
  const copied = new File(Paths.document, STAMP);
  const allPresent = names.every((n) => new File(Paths.document, n).exists);
  if (allPresent && copied.exists && (await copied.text()) === stamp) return;

  for (const name of names) {
    const part = new File(Paths.document, `${name}.part`);
    if (part.exists) part.delete(); // an interrupted copy from an earlier launch
    await new File(`${ASSET_DIR}/${name}`).copy(part);
    const dest = new File(Paths.document, name);
    if (dest.exists) dest.delete();
    await part.move(dest);
  }
  // Written last: a crash mid-copy leaves the old stamp, so the next launch copies again.
  await copied.write(stamp);
}
