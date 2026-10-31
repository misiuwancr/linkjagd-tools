ALTER TABLE affiliate_programs ADD COLUMN program_info_url text;
ALTER TABLE affiliate_programs ADD COLUMN program_presence text NOT NULL DEFAULT 'unknown';

UPDATE affiliate_programs
SET program_presence = 'yes'
WHERE status = 'found';
