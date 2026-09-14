/**
 * Admin allowlist for Google SSO.
 *
 * Sole source: ADMIN_EMAILS env (comma-separated). There is no hardcoded
 * operator address. Empty / missing ADMIN_EMAILS → empty allowlist → nobody
 * can sign in (fail closed). Deployer must supply real Google account emails
 * via env. GitHub noreply addresses are not Google accounts and will not work
 * as Google OAuth login identities.
 */

function normalizeEmail(email: string): string {
  return email.trim().toLowerCase();
}

/** Parsed ADMIN_EMAILS env — empty/missing → []. */
export function envAdminEmails(): string[] {
  const raw = process.env.ADMIN_EMAILS;
  if (!raw || !raw.trim()) return [];
  return raw
    .split(",")
    .map((part) => normalizeEmail(part))
    .filter((email) => email.length > 0 && email.includes("@"));
}

/** Effective allowlist: ADMIN_EMAILS only. Empty → nobody. */
export function adminAllowlist(): string[] {
  return [...new Set<string>(envAdminEmails())];
}

export function isAdminEmail(email: string | null | undefined): boolean {
  if (!email) return false;
  const list = adminAllowlist();
  if (list.length === 0) return false; // fail closed
  return list.includes(normalizeEmail(email));
}

/** Hint string for login UI when at least one allowlisted email exists. */
export function primaryAdminEmailHint(): string | null {
  const list = adminAllowlist();
  return list[0] ?? null;
}
