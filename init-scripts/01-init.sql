-- Create the database if it doesn't exist
CREATE DATABASE project_k_db;

-- Connect to the database
\c project_k_db

-- Create the user if it doesn't exist and grant privileges
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'project_k_user') THEN

      CREATE ROLE project_k_user LOGIN PASSWORD 'project_k_password';
   END IF;
END
$do$;

-- Grant privileges
ALTER ROLE project_k_user WITH SUPERUSER;
GRANT ALL PRIVILEGES ON DATABASE project_k_db TO project_k_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO project_k_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO project_k_user;

