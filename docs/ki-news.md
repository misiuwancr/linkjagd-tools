# KI-News pflegen

Auf Wunsch von Michał wird die ursprünglich angekündigte Datei nicht benötigt. `data/ai-news.json` bleibt daher zunächst leer; es werden keine Meldungen erfunden oder aus fremden Texten kopiert.

Neue Einträge benötigen `id`, `title`, `summary`, `category`, `publishedAt` (ISO-Datum mit Zeitzone), `sourceName` und `sourceUrl` (HTTPS). `imageUrl` ist optional und muss auf ein eigenes/lizenziertes lokales oder HTTPS-Bild zeigen; ohne Bild erscheint die eigene neutrale Illustration. Kurze Titel und Zusammenfassungen selbst formulieren, immer zur Originalquelle verlinken. Die Laufzeit prüft die Daten und zeigt zukünftige Einträge erst ab ihrem Veröffentlichungsdatum.

Die Website liest die Datei beim Deployment. Es ist kein automatischer Nachrichtendienst eingerichtet. Der Untertitel verspricht deshalb keine mehrmals täglichen Aktualisierungen. Ein solcher Hinweis darf erst erscheinen, wenn die Redaktion diesen Ablauf tatsächlich betreibt.
