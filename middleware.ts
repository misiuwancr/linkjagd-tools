import { NextResponse, type NextRequest } from "next/server";
import { isProtectedAdminPath } from "@/lib/auth/paths";
import { readSession, safeAdminNext, SESSION_COOKIE } from "@/lib/auth/token";

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  if (!isProtectedAdminPath(pathname)) return NextResponse.next();
  const token = request.cookies.get(SESSION_COOKIE)?.value;
  const session = token ? await readSession(token) : null;
  if (session) return NextResponse.next();
  if (pathname.startsWith("/api/")) {
    return NextResponse.json({ error: "Nicht autorisiert." }, { status: 401 });
  }
  const url = request.nextUrl.clone();
  url.pathname = "/admin/login";
  url.searchParams.set("next", safeAdminNext(pathname));
  return NextResponse.redirect(url);
}

export const config = {
  matcher: ["/admin", "/admin/:path*", "/api/admin/:path*"],
};
