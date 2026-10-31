CREATE TABLE IF NOT EXISTS newsletter_subscribers (
  id text PRIMARY KEY NOT NULL,
  email text NOT NULL UNIQUE,
  status text NOT NULL DEFAULT 'pending',
  confirm_token text NOT NULL UNIQUE,
  created_at integer NOT NULL,
  confirmed_at integer
);

CREATE TABLE IF NOT EXISTS site_settings (
  key text PRIMARY KEY NOT NULL,
  value text NOT NULL DEFAULT ''
);

ALTER TABLE news_posts ADD COLUMN cover_image_url text;
ALTER TABLE news_posts ADD COLUMN seo_title text;
ALTER TABLE news_posts ADD COLUMN seo_description text;
