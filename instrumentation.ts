export async function register() {
  // Bewusst ohne Datenbank. Admin-Bootstrap läuft beim Login.
  // Die Kategorie-Umsortierung ist `npm run db:reclassify`, nicht Teil des Boots.
  // Ein Timeout gegen Turso in diesem Hook bricht sonst den ganzen Server ab.
}
