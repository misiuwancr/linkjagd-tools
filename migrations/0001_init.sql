CREATE TABLE users (
  id text PRIMARY KEY NOT NULL,
  email text NOT NULL UNIQUE,
  password_hash text NOT NULL,
  role text NOT NULL,
  created_at integer NOT NULL
);

CREATE TABLE categories (
  id text PRIMARY KEY NOT NULL,
  name text NOT NULL,
  slug text NOT NULL UNIQUE,
  description text,
  sort_order integer NOT NULL DEFAULT 0,
  created_at integer NOT NULL,
  updated_at integer NOT NULL
);

CREATE TABLE tags (
  id text PRIMARY KEY NOT NULL,
  name text NOT NULL,
  slug text NOT NULL UNIQUE
);

CREATE TABLE tools (
  id text PRIMARY KEY NOT NULL,
  name text NOT NULL,
  slug text NOT NULL UNIQUE,
  original_url text NOT NULL,
  domain text NOT NULL,
  logo text,
  short_description_de text NOT NULL,
  long_description_de text NOT NULL DEFAULT '',
  features_de text NOT NULL DEFAULT '[]',
  screenshots text NOT NULL DEFAULT '[]',
  pricing_model text NOT NULL DEFAULT 'freemium',
  publish_status text NOT NULL DEFAULT 'draft',
  featured integer NOT NULL DEFAULT 0,
  editorial_rank integer,
  discovery_source text NOT NULL DEFAULT 'manual',
  is_example integer NOT NULL DEFAULT 0,
  search_text text NOT NULL DEFAULT '',
  internal_notes text,
  submitter_email text,
  created_at integer NOT NULL,
  updated_at integer NOT NULL
);

CREATE INDEX tools_domain_idx ON tools (domain);
CREATE INDEX tools_status_idx ON tools (publish_status);
CREATE INDEX tools_created_idx ON tools (created_at);
CREATE INDEX tools_rank_idx ON tools (editorial_rank);

CREATE TABLE tool_categories (
  tool_id text NOT NULL REFERENCES tools(id) ON DELETE CASCADE,
  category_id text NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
  PRIMARY KEY (tool_id, category_id)
);

CREATE INDEX tool_categories_category_idx ON tool_categories (category_id);

CREATE TABLE tool_tags (
  tool_id text NOT NULL REFERENCES tools(id) ON DELETE CASCADE,
  tag_id text NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
  PRIMARY KEY (tool_id, tag_id)
);

CREATE TABLE affiliate_programs (
  id text PRIMARY KEY NOT NULL,
  tool_id text NOT NULL REFERENCES tools(id) ON DELETE CASCADE,
  affiliate_url text,
  network text NOT NULL DEFAULT 'manual',
  partner_program_id text,
  status text NOT NULL DEFAULT 'none_found',
  last_checked_at integer,
  priority integer NOT NULL DEFAULT 0,
  is_active integer NOT NULL DEFAULT 0,
  notes text,
  created_at integer NOT NULL,
  updated_at integer NOT NULL
);

CREATE INDEX affiliate_tool_idx ON affiliate_programs (tool_id);

CREATE TABLE click_daily (
  tool_id text NOT NULL REFERENCES tools(id) ON DELETE CASCADE,
  program_id text NOT NULL REFERENCES affiliate_programs(id) ON DELETE CASCADE,
  day text NOT NULL,
  count integer NOT NULL DEFAULT 0,
  PRIMARY KEY (tool_id, program_id, day)
);

CREATE TABLE news_posts (
  id text PRIMARY KEY NOT NULL,
  title text NOT NULL,
  slug text NOT NULL UNIQUE,
  excerpt text NOT NULL,
  body text NOT NULL DEFAULT '',
  source_name text,
  status text NOT NULL DEFAULT 'draft',
  published_at integer,
  created_at integer NOT NULL,
  updated_at integer NOT NULL
);
