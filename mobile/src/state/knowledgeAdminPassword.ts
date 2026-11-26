import { knowledgePatchStorage } from './knowledgePatchStorage';
import { unlockForGuide } from './parkAccess';

// Plain comparison on purpose: scrypt (N=32768) in pure JS took minutes under Hermes on a
// mid-range phone, so the panel never opened. This only gates the guide's editor on their own
// phone; it is not a security boundary.
const storage = knowledgePatchStorage('knowledge-admin-password-v2');
const INITIAL_PASSWORD = 'cisco123';

export const validAdminPassword = (password: string) =>
  Array.from(password).length >= 8 && password.length <= 128 && password.trim().length > 0;

export async function verifyAdminPassword(password: string): Promise<boolean> {
  if (!validAdminPassword(password)) return false;
  const valid = password === ((await storage.read()) ?? INITIAL_PASSWORD);
  // Only a guide knows it, so the park gate no longer applies to this phone.
  if (valid) unlockForGuide();
  return valid;
}

export async function setAdminPassword(password: string): Promise<void> {
  if (!validAdminPassword(password)) throw new Error('Invalid administration password.');
  await storage.write(password);
}
