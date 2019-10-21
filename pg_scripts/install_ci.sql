CREATE SCHEMA IF NOT EXISTS django_ci;
CREATE DATABASE test_djangodb WITH TEMPLATE = template0 OWNER = traveladmin ENCODING = 'UTF8' LC_COLLATE = 'ja_JP.UTF-8' LC_CTYPE = 'ja_JP.UTF-8';
GRANT ALL PRIVILEGES on database test_djangodb to traveladmin;
ALTER USER traveladmin CREATEDB;
