# Voting freigeben

Das Feature bleibt ohne `ANONYMOUS_VOTING_ENABLED=true` deaktiviert. Der feste Startwert ist keine Besucher-Stimme; angezeigt wird 1 plus die Zahl tatsächlich gespeicherter Stimmen.

1. Michał muss die beiden Tabellen in `migrations/manual/0008_anonymous_votes.sql` ausdrücklich für Produktion freigeben. Die Datei wird von `applyMigrations` nicht geladen. Keine produktive Migration wurde bei der Implementierung ausgeführt.
2. Eine separate Vorschau-Datenbank verwenden: laut DEPLOY.md teilen Vorschau und Produktion bislang Zugangsdaten. Die Migration erst auf einer isolierten Kopie testen, inklusive wiederholter und paralleler Votes.
3. Nach Freigabe Backup erstellen und die SQL-Datei manuell auf der freigegebenen Zieldatenbank anwenden.
4. `VOTE_HASH_SECRET` mit mindestens 32 zufälligen Zeichen als geheime Umgebungsvariable setzen. Nicht ins Repo schreiben. Secret dauerhaft beibehalten, sonst ändern sich die anonymen Zuordnungen.
5. `ANONYMOUS_VOTING_ENABLED=true` setzen und neu bereitstellen. Auf Vercel wird ausschließlich der von Vercel gesetzte IP-Header akzeptiert. Andere Produktionshosts benötigen zuvor eine geprüfte Proxy-Anbindung.

Pro Tool gilt ein Vote je signiertem Cookie und je gehashter IP. Gemeinsam genutzte IPs können deshalb nur einmal pro Tool abstimmen. VPN-Wechsel kann technisch nicht vollständig verhindert werden. Zehn Versuche pro IP und Stunde werden datenbankweit atomar begrenzt; alte Rate-Limit-Zeilen werden nach einem Tag bereinigt. Cookie und IP werden mit HMAC getrennt pseudonymisiert, Roh-IP und Cookie nie gespeichert oder geloggt. Keine Behauptung eindeutiger Personen.

Datenschutztext vor Aktivierung prüfen: Funktionscookie (ein Jahr), pseudonymisierte IP-Zuordnung und Speicherdauer der Stimmen. Bei Bedarf Voting mit der Umgebungsvariable deaktivieren; die Daten bleiben erhalten.
