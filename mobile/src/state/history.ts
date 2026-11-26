import * as SQLite from 'expo-sqlite';
import { useCallback, useState } from 'react';

export interface HistoryRow {
  id: number;
  at: number;
  kind: string; // tool name: register_visit | report_emergency
  args: string; // JSON
  result: string; // JSON
}

let dbPromise: Promise<SQLite.SQLiteDatabase> | null = null;
function db() {
  dbPromise ??= SQLite.openDatabaseAsync('nevados.db').then(async (d) => {
    await d.execAsync(
      'CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY AUTOINCREMENT, at INTEGER NOT NULL, kind TEXT NOT NULL, args TEXT NOT NULL, result TEXT NOT NULL)',
    );
    return d;
  });
  return dbPromise;
}

export async function recordEffect(kind: string, args: unknown, result: unknown) {
  const d = await db();
  await d.runAsync(
    'INSERT INTO history (at, kind, args, result) VALUES (?, ?, ?, ?)',
    Date.now(),
    kind,
    JSON.stringify(args ?? {}),
    JSON.stringify(result ?? {}),
  );
}

export async function listHistory(): Promise<HistoryRow[]> {
  const d = await db();
  return d.getAllAsync<HistoryRow>('SELECT * FROM history ORDER BY id DESC LIMIT 200');
}

export function useHistory() {
  const [rows, setRows] = useState<HistoryRow[]>([]);
  const refresh = useCallback(() => {
    listHistory().then(setRows, (e) => console.warn('history load failed', e));
  }, []);
  return { rows, refresh };
}
