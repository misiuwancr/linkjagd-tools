CREATE INDEX IF NOT EXISTS tools_public_newest_idx ON tools (publish_status, is_example, created_at);
CREATE INDEX IF NOT EXISTS tools_public_name_idx ON tools (publish_status, is_example, name);
CREATE INDEX IF NOT EXISTS tools_public_price_idx ON tools (publish_status, is_example, pricing_model);
CREATE INDEX IF NOT EXISTS tools_public_license_idx ON tools (publish_status, is_example, license_type);
CREATE INDEX IF NOT EXISTS click_daily_tool_idx ON click_daily (tool_id);
