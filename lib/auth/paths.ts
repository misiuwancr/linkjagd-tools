export function isProtectedAdminPath(pathname: string) {
  if (pathname === "/admin/login" || pathname.startsWith("/admin/login/")) return false;
  if (pathname === "/admin" || pathname.startsWith("/admin/")) return true;
  if (pathname === "/api/admin" || pathname.startsWith("/api/admin/")) return true;
  return false;
}
