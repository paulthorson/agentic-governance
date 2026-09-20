/**
 * Localhost-only gate for /admin metrics.
 *
 * Admin is intentionally open on local hostnames only. Remote identity login
 * is not part of this app. Non-local Host headers fail closed (middleware
 * redirects to public `/`).
 */

/** Hostnames treated as local for admin access. */
const LOCAL_HOSTNAMES = new Set([
  "localhost",
  "127.0.0.1",
  "[::1]",
  "::1",
  "0.0.0.0",
]);

/**
 * Strip port from a Host / X-Forwarded-Host value.
 * IPv6 bracket forms like `[::1]:3000` keep the brackets on the hostname.
 */
export function hostnameFromHostHeader(
  hostHeader: string | null | undefined,
): string | null {
  if (!hostHeader) return null;
  const raw = hostHeader.trim().toLowerCase();
  if (!raw) return null;

  if (raw.startsWith("[")) {
    const end = raw.indexOf("]");
    if (end === -1) return null;
    return raw.slice(0, end + 1);
  }

  const colon = raw.lastIndexOf(":");
  if (colon > -1 && /^\d+$/.test(raw.slice(colon + 1))) {
    return raw.slice(0, colon);
  }
  return raw;
}

/**
 * True when the request Host is localhost / loopback / *.localhost.
 * Empty or missing host → fail closed (false).
 */
export function isLocalAdminHost(
  hostHeader: string | null | undefined,
): boolean {
  const hostname = hostnameFromHostHeader(hostHeader);
  if (!hostname) return false;
  if (LOCAL_HOSTNAMES.has(hostname)) return true;
  // e.g. myapp.localhost (common local DNS convention)
  if (hostname.endsWith(".localhost")) return true;
  return false;
}
