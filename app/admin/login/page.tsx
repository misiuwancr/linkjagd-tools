import type { Metadata } from "next";
import { login } from "@/lib/actions/auth";
import { safeAdminNext } from "@/lib/auth/token";
import { sessionSecretStatus } from "@/db/resolve";
import { BrandLockup } from "@/components/brand";

export const metadata: Metadata = {
  title: "Anmeldung",
  robots: { index: false, follow: false },
};

export default function LoginPage({
  searchParams,
}: {
  searchParams: { fehler?: string; next?: string };
}) {
  const locked = sessionSecretStatus() !== "ok";
  return (
    <div className="grid min-h-screen place-items-center px-4 py-16">
      <div className="w-full max-w-md rounded-3xl border border-border bg-card p-6 shadow-card sm:p-8">
        <BrandLockup />
        <h1 className="mt-8 text-2xl font-bold tracking-tight">Redaktion</h1>
        <p className="mt-2 text-sm text-muted-foreground">Nur für freigeschaltete Konten.</p>
        {locked ? (
          <p role="alert" className="mt-4 rounded-xl border border-red-800 bg-red-950 px-3 py-2 text-sm text-red-100">
            Die Redaktion ist zu. JWT_SECRET fehlt oder ist noch der Platzhalter aus der Beispiel-Umgebung.
          </p>
        ) : null}
        {searchParams.fehler === "config" ? (
          <p role="alert" className="mt-4 rounded-xl border border-red-800 bg-red-950 px-3 py-2 text-sm text-red-100">
            Anmeldung abgelehnt, weil kein gültiges JWT_SECRET gesetzt ist.
          </p>
        ) : null}
        {searchParams.fehler && searchParams.fehler !== "config" ? (
          <p role="alert" className="mt-4 rounded-xl border border-red-800 bg-red-950 px-3 py-2 text-sm text-red-100">
            E-Mail oder Passwort stimmt nicht.
          </p>
        ) : null}
        {locked ? null : (
        <form action={login} className="mt-6 grid gap-4">
          <input type="hidden" name="next" value={safeAdminNext(searchParams.next)} />
          <label className="grid gap-1 text-sm font-medium">
            E-Mail
            <input name="email" type="email" autoComplete="username" required className="field" />
          </label>
          <label className="grid gap-1 text-sm font-medium">
            Passwort
            <input name="password" type="password" autoComplete="current-password" required className="field" />
          </label>
          <button type="submit" className="h-11 rounded-xl bg-primary text-sm font-semibold text-primary-foreground">
            Anmelden
          </button>
        </form>
        )}
      </div>
    </div>
  );
}
