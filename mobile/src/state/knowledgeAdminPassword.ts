import { scryptAsync } from '@noble/hashes/scrypt.js';
import { bytesToHex, hexToBytes } from '@noble/hashes/utils.js';
import { getRandomBytesAsync } from 'expo-crypto';

import { utf8Bytes } from '@/core/knowledge/qrPatch';

import { knowledgePatchStorage } from './knowledgePatchStorage';

const storage = knowledgePatchStorage('knowledge-admin-password-v1');
const initial = {
  salt: 'a38972375743b8e50a8c08189983e9bc',
  digest: '03a8bcfb3b4385d3f69484e15a67b76b56a91d19911bf2467f89d87642bdcc07',
};
const derive = (password: string, salt: string) =>
  scryptAsync(utf8Bytes(password), utf8Bytes(salt), { N: 32768, r: 8, p: 1, dkLen: 32 });

export const validAdminPassword = (password: string) =>
  Array.from(password).length >= 8 && password.length <= 128 && password.trim().length > 0;

export async function verifyAdminPassword(password: string): Promise<boolean> {
  if (!validAdminPassword(password)) return false;
  const raw = await storage.read();
  const saved = raw === null ? initial : (JSON.parse(raw) as typeof initial);
  if (!/^[a-f0-9]{32}$/.test(saved.salt) || !/^[a-f0-9]{64}$/.test(saved.digest)) {
    throw new Error('Invalid administration credential.');
  }
  const actual = await derive(password, saved.salt);
  const expected = hexToBytes(saved.digest);
  let difference = 0;
  for (let i = 0; i < expected.length; i++) difference |= expected[i] ^ actual[i];
  return difference === 0;
}

export async function setAdminPassword(password: string): Promise<void> {
  if (!validAdminPassword(password)) throw new Error('Invalid administration password.');
  const salt = bytesToHex(await getRandomBytesAsync(16));
  const digest = bytesToHex(await derive(password, salt));
  await storage.write(JSON.stringify({ salt, digest }));
}
