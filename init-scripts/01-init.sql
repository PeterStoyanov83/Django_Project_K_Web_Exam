-- Connect to the database
\c project_k_db

-- Grant necessary privileges to the user
ALTER ROLE project_k_user WITH SUPERUSER;
GRANT ALL PRIVILEGES ON DATABASE project_k_db TO project_k_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO project_k_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO project_k_user;

