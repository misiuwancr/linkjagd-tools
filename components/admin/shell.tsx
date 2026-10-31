import Link from "next/link";
import { logout } from "@/lib/actions/auth";
import { BrandLockup } from "@/components/brand";

const links = [
  { href: "/admin", label: "Übersicht" },
  { href: "/admin/tools", label: "Tools" },
  { href: "/admin/tools/neu", label: "Neues Tool" },
  { href: "/admin/moderation", label: "Moderation" },
  { href: "/admin/kategorien", label: "Kategorien" },
];

export function AdminShell({
  email,
  role,
  children,
}: {
  email: string;
  role: string;
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-paper">
      <div className="border-b border-border bg-white">
        <div className="page-wrap flex h-16 items-center justify-between gap-4">
          <BrandLockup compact />
          <div className="flex items-center gap-3 text-sm">
            <span className="hidden text-muted-foreground sm:inline">
              {email} · {role === "admin" ? "Admin" : "Redaktion"}
            </span>
            <form action={logout}>
              <button type="submit" className="rounded-full border border-border px-3 py-1.5">
                Abmelden
              </button>
            </form>
          </div>
        </div>
      </div>
      <div className="page-wrap grid gap-8 py-8 lg:grid-cols-[200px_minmax(0,1fr)]">
        <nav aria-label="Redaktion" className="flex flex-wrap gap-2 lg:flex-col">
          {links.map((link) => (
            <Link key={link.href} href={link.href} className="rounded-full px-3 py-2 text-sm font-medium hover:bg-white">
              {link.label}
            </Link>
          ))}
        </nav>
        <div>{children}</div>
      </div>
    </div>
  );
}

export function Flash({ gespeichert, fehler }: { gespeichert?: string; fehler?: string }) {
  if (fehler) {
    return (
      <p role="alert" className="mb-4 rounded-xl bg-red-50 px-4 py-3 text-sm text-red-900">
        {fehler}
      </p>
    );
  }
  if (gespeichert) {
    return (
      <p role="status" className="mb-4 rounded-xl bg-emerald-50 px-4 py-3 text-sm text-emerald-900">
        Gespeichert.
      </p>
    );
  }
  return null;
}
