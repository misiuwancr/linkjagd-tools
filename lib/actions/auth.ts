"use server";

import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { eq } from "drizzle-orm";
import { users } from "@/db/schema";
import { getDb } from "@/db/client";
import { ensureAdmin } from "@/db/seed";
import { verifyPassword } from "@/lib/auth/password";
import { sessionCookieOptions } from "@/lib/auth/session";
import { safeAdminNext, SESSION_COOKIE, signSession } from "@/lib/auth/token";
import { sessionSecretStatus } from "@/db/resolve";

export async function login(formData: FormData) {
  if (sessionSecretStatus() !== "ok") redirect("/admin/login?fehler=config");
  const email = String(formData.get("email") || "").trim().toLowerCase();
  const password = String(formData.get("password") || "");
  const database = await getDb();
  await ensureAdmin(database);
  const user = await database.query.users.findFirst({ where: eq(users.email, email) });
  const valid = user ? verifyPassword(password, user.passwordHash) : false;
  if (!user || !valid) redirect("/admin/login?fehler=1");
  const token = await signSession({ sub: user.id, email: user.email, role: user.role });
  cookies().set(SESSION_COOKIE, token, sessionCookieOptions());
  redirect(safeAdminNext(String(formData.get("next") || "")));
}

export async function logout() {
  cookies().set(SESSION_COOKIE, "", { ...sessionCookieOptions(), maxAge: 0 });
  redirect("/admin/login");
}
