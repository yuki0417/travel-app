-- テスト用DBのSQL
CREATE ROLE test_user WITH LOGIN PASSWORD 'test_password';
CREATE DATABASE test_db WITH TEMPLATE = template0 OWNER = test_user ENCODING = 'UTF8' LC_COLLATE = 'ja_JP.UTF-8' LC_CTYPE = 'ja_JP.UTF-8';
\connect test_db
CREATE SCHEMA IF NOT EXISTS public;
GRANT ALL PRIVILEGES on database test_db to test_user;
ALTER USER test_user CREATEDB;
