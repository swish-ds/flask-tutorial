-- Each test will create a new temporary database file and populate some data that will be used in the tests.

INSERT INTO post (title, body, created)
VALUES
  ('test title', 'test' || x'0a' || 'body', '2018-01-01 00:00:00');