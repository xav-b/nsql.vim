/*
 * init test database
 */

CREATE TABLE IF NOT EXISTS foo (
  id serial PRIMARY KEY,
  bar VARCHAR(100),
  count INT,
  created_at TIMESTAMP default current_timestamp,
  updated_at TIMESTAMP default current_timestamp
)
