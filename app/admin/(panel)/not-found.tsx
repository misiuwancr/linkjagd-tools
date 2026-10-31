import Link from "next/link";

export default function AdminNotFound() {
  return (
    <div>
      <h1 className="text-3xl font-bold tracking-tight">Eintrag nicht gefunden.</h1>
      <Link href="/admin/tools" className="mt-4 inline-block text-sm underline">
        Zurück zu den Tools
      </Link>
    </div>
  );
}
