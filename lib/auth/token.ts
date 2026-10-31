import { SignJWT, jwtVerify } from "jose";
import type { UserRole } from "@/db/schema";

export const SESSION_COOKIE = "linkjagd_session";

export type SessionPayload = {
  sub: string;
  email: string;
  role: UserRole;
};

function secret() {
  const value = process.env.JWT_SECRET;
  if (!value || value.length < 16) return null;
  return new TextEncoder().encode(value);
}

export async function signSession(payload: SessionPayload) {
  const key = secret();
  if (!key) throw new Error("JWT_SECRET fehlt oder ist kürzer als 16 Zeichen.");
  return new SignJWT({ email: payload.email, role: payload.role })
    .setProtectedHeader({ alg: "HS256" })
    .setSubject(payload.sub)
    .setIssuedAt()
    .setExpirationTime("12h")
    .sign(key);
}

export async function readSession(token: string): Promise<SessionPayload | null> {
  const key = secret();
  if (!key) return null;
  try {
    const { payload } = await jwtVerify(token, key);
    const role = payload.role;
    const email = payload.email;
    if ((role !== "admin" && role !== "editor") || typeof email !== "string" || !payload.sub) {
      return null;
    }
    return { sub: payload.sub, email, role };
  } catch {
    return null;
  }
}

export function safeAdminNext(value: string | null | undefined) {
  if (!value || !value.startsWith("/admin")) return "/admin";
  if (value.startsWith("//") || value.startsWith("/admin/login")) return "/admin";
  if (value.includes("\\") || value.includes("://")) return "/admin";
  return value;
}
