import {NextResponse, type NextRequest} from "next/server";
import {isLocalAdminHost, resolveRequestHost} from "@/lib/admin-access";

/**
 * Protect /admin/* — localhost hostnames only.
 * Non-local requests fail closed: redirect to public `/` with a clear notice.
 * Remote identity login is not offered.
 * Host is preferred; client X-Forwarded-Host is ignored unless
 * AG_TRUST_X_FORWARDED_HOST is set. Empty host fails closed.
 */
export function middleware(req: NextRequest) {
  const host = resolveRequestHost(req.headers);

  if (isLocalAdminHost(host)) {
    return NextResponse.next();
  }

  const home = new URL("/", req.nextUrl.origin);
  home.searchParams.set("admin", "local-only");
  return NextResponse.redirect(home);
}

export const config = {
  matcher: ["/admin", "/admin/:path*"],
};
