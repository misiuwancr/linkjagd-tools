ALTER TABLE tools ADD COLUMN license_type text NOT NULL DEFAULT 'unknown';
ALTER TABLE tools ADD COLUMN oss_project_url text;
ALTER TABLE tools ADD COLUMN oss_repo_url text;
ALTER TABLE tools ADD COLUMN oss_license text;
ALTER TABLE tools ADD COLUMN oss_operating_systems text NOT NULL DEFAULT '[]';
ALTER TABLE tools ADD COLUMN oss_install_notes text;
ALTER TABLE tools ADD COLUMN use_cases_de text NOT NULL DEFAULT '[]';
ALTER TABLE tools ADD COLUMN tiktok_url text;
ALTER TABLE tools ADD COLUMN instagram_reel_url text;
ALTER TABLE tools ADD COLUMN youtube_short_url text;
ALTER TABLE tools ADD COLUMN editor_rating integer;
ALTER TABLE tools ADD COLUMN last_checked_at integer;
ALTER TABLE tools ADD COLUMN beginner_friendly integer NOT NULL DEFAULT 0;
ALTER TABLE tools ADD COLUMN content_locked integer NOT NULL DEFAULT 0;
ALTER TABLE tools ADD COLUMN missing_fields text NOT NULL DEFAULT '[]';

UPDATE tools
SET license_type = 'open_source', pricing_model = 'free'
WHERE pricing_model = 'open_source';

CREATE TABLE click_daily_v2 (
  tool_id text NOT NULL REFERENCES tools(id) ON DELETE CASCADE,
  program_slot text NOT NULL DEFAULT '',
  target_kind text NOT NULL,
  day text NOT NULL,
  count integer NOT NULL DEFAULT 0,
  PRIMARY KEY (tool_id, target_kind, day, program_slot)
);

INSERT INTO click_daily_v2 (tool_id, program_slot, target_kind, day, count)
SELECT tool_id, program_id, 'affiliate', day, count FROM click_daily;

DROP TABLE click_daily;
ALTER TABLE click_daily_v2 RENAME TO click_daily;
