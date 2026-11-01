-- Noch nicht in migrations/. Wird beim Start nicht ausgeführt.
-- Erst nach ausdrücklicher Freigabe nach migrations/ verschieben oder einmalig auf Turso ausführen.
-- Bestehende Zeilen bleiben erhalten. Neue Spalte ist 1, das entspricht dem heutigen Verhalten (veröffentlicht = indexierbar).
ALTER TABLE tools ADD COLUMN allow_index integer NOT NULL DEFAULT 1;
