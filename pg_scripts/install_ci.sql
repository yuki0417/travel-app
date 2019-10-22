-- CREATE ROLE IF NOT EXISTS travel_ci WITH LOGIN PASSWORD 'travel_ci';
CREATE DATABASE test_djangodb_ci WITH TEMPLATE = template0 OWNER = travel_ci ENCODING = 'UTF8' LC_COLLATE = 'ja_JP.UTF-8' LC_CTYPE = 'ja_JP.UTF-8';
\connect test_djangodb_ci
CREATE SCHEMA IF NOT EXISTS django_ci;
GRANT ALL PRIVILEGES on database test_djangodb_ci to travel_ci;
ALTER USER travel_ci CREATEDB;
