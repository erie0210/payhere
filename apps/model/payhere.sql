﻿DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER(11) PRIMARY KEY AUTOINCREMENT,
  email VARCHAR(100) UNIQUE NOT NULL,
  password VARCHAR(100) NOT NULL
);

CREATE TABLE post (
  id INTEGER(11) PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER(11) NOT NULL,
  amount INTEGER(11) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title VARCHAR(32) NOT NULL,
  body TEXT,
  deleted INTEGER(11),
  FOREIGN KEY (author_id) REFERENCES user (id)
);