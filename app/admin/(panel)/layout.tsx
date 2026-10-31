import type { Metadata } from "next";
import { requireUser } from "@/lib/auth/session";
import { AdminShell } from "@/components/admin/shell";

export const metadata: Metadata = {
  title: "Redaktion",
  robots: { index: false, follow: false },
};

export default async function AdminLayout({ children }: { children: React.ReactNode }) {
  const user = await requireUser("editor");
  return (
    <AdminShell email={user.email} role={user.role}>
      {children}
    </AdminShell>
  );
}
