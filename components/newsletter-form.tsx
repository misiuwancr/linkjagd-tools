import { siteConfig } from "@/site.config";
import { subscribeNewsletter } from "@/lib/actions/public";

const messages: Record<string, string> = {
  datenschutz: "Bitte die Einwilligung zur Speicherung der Adresse bestätigen.",
  email: "Die E-Mail-Adresse sieht ungültig aus.",
  bereits: "Diese Adresse ist schon bestätigt.",
  gespeichert: "Der Versand ist gerade fehlgeschlagen. Die Anmeldung gilt erst nach dem Link in der Mail.",
  mail: "Schau in dein Postfach und bestätige die Adresse. Vorher gilt die Anmeldung nicht.",
  bot: "Die Anmeldung wurde verworfen.",
  aus: "Die Anmeldung ist noch nicht geöffnet. Es wurde keine Adresse gespeichert.",
};

export function NewsletterForm({
  notice,
  compact = false,
  returnTo = "/newsletter",
  open,
}: {
  notice?: string;
  compact?: boolean;
  returnTo?: string;
  open: boolean;
}) {
  if (!open) return null;
  return (
    <form id="anmeldung" action={subscribeNewsletter} className={(compact ? "grid gap-3" : "grid max-w-xl gap-3") + " scroll-mt-24"}>
      <input type="hidden" name="zurueck" value={returnTo} />
      <input name="firma" tabIndex={-1} autoComplete="off" className="hidden" aria-hidden="true" />
      <div className="flex flex-col gap-2 sm:flex-row">
        <label className="sr-only" htmlFor="newsletter-email">
          E-Mail
        </label>
        <input
          id="newsletter-email"
          name="email"
          type="email"
          required
          autoComplete="email"
          placeholder="deine@adresse.de"
          className="field h-14 flex-1 text-base"
        />
        <button type="submit" className="h-14 rounded-xl bg-primary px-6 text-base font-bold text-primary-foreground">
          Newsletter abonnieren
        </button>
      </div>
      <label className="flex items-start gap-2 text-sm leading-6 text-muted-foreground">
        <input name="datenschutz" type="checkbox" value="ja" required className="mt-1" />
        <span>
          Ich willige ein, dass {siteConfig.name} diese Adresse speichert, bis ich sie bestätige oder widerrufe. Hinweise stehen in der{" "}
          <a href="/datenschutz" className="underline">
            Datenschutzerklärung
          </a>
          . Ohne Bestätigung über den Link in der Mail gilt die Anmeldung nicht.
        </span>
      </label>
      {notice && messages[notice] ? (
        <p role="status" className="text-sm text-foreground">
          {messages[notice]}
        </p>
      ) : null}
    </form>
  );
}
