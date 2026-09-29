import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

export type UpdateStatus = {
  checked: boolean;
  current_version: string;
  latest_version: string | null;
  update_available: boolean;
  changelog_url: string;
  releases_url: string;
  checked_at: number | null;
  reason?: string;
  cached?: boolean;
};

/**
 * Read the update-check status written by scripts/check_updates.py
 * (runs/update-check.json, gitignored). Returns null when the check has
 * never run — the banner simply stays hidden.
 */
export function loadUpdateStatus(): UpdateStatus | null {
  const cwd = process.cwd();
  const candidates = [
    join(cwd, "..", "runs", "update-check.json"),
    join(cwd, "runs", "update-check.json"),
  ];
  for (const path of candidates) {
    try {
      if (existsSync(path)) {
        return JSON.parse(readFileSync(path, "utf8")) as UpdateStatus;
      }
    } catch {
      // A corrupt status file is not worth breaking the homepage over.
    }
  }
  return null;
}
