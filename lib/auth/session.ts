import { cookies } from "next/headers";
import { eq } from "drizzle-orm";
import { redirect } from "next/navigation";
import { users, type UserRole } from "@/db/schema";
import { getDb } from "@/db/client";
import { roleAllows } from "@/lib/auth/roles";
import { readSession, SESSION_COOKIE } from "@/lib/auth/token";

export function sessionCookieOptions() {
  return {
    httpOnly: true,
    sameSite: "lax" as const,
    secure: process.env.NODE_ENV === "production",
    path: "/",
    maxAge: 60 * 60 * 12,
  };
}

export async function getSession() {
  const token = cookies().get(SESSION_COOKIE)?.value;
  if (!token) return null;
  return readSession(token);
}

export async function assertUser(minimum: UserRole = "editor") {
  const session = await getSession();
  if (!session) return { ok: false as const, error: "Nicht autorisiert." };
  const database = await getDb();
  const user = await database.query.users.findFirst({
    where: eq(users.id, session.sub),
  });
  if (!user) return { ok: false as const, error: "Nicht autorisiert." };
  if (!roleAllows(user.role, minimum)) {
    return { ok: false as const, error: "Dafür reicht deine Rolle nicht." };
  }
  return { ok: true as const, user };
}

export async function requireUser(minimum: UserRole = "editor") {
  const result = await assertUser(minimum);
  if (!result.ok) redirect("/admin/login");
  return result.user;
}
