-- Nur nach ausdrücklicher Freigabe manuell auf der Zieldatenbank ausführen.
-- Liegt absichtlich außerhalb des automatischen Migrationsverzeichnisses.
CREATE TABLE IF NOT EXISTS tool_votes (
  tool_id text NOT NULL REFERENCES tools(id) ON DELETE CASCADE,
  cookie_hash text NOT NULL,
  ip_hash text NOT NULL,
  created_at integer NOT NULL,
  PRIMARY KEY (tool_id, cookie_hash),
  UNIQUE (tool_id, ip_hash)
);
CREATE TABLE IF NOT EXISTS vote_rate_limits (
  ip_hash text NOT NULL,
  window_start integer NOT NULL,
  attempts integer NOT NULL DEFAULT 1,
  PRIMARY KEY (ip_hash, window_start)
);
