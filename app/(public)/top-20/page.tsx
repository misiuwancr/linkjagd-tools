import { redirect } from "next/navigation";

export default function TopPage() {
  redirect("/tools?sort=alphabetisch");
}
