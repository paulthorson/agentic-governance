import {NextResponse, type NextRequest} from "next/server";
import {isLocalAdminHost} from "@/lib/admin-access";

/**
 * Protect /admin/* — localhost hostnames only.
 * Non-local requests fail closed: redirect to public `/` with a clear notice.
 * Remote identity login is not offered.
 */
export function middleware(req: NextRequest) {
  const host =
    req.headers.get("x-forwarded-host")?.split(",")[0]?.trim() ||
    req.headers.get("host");

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
