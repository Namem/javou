-- 1. Remove permissões padrão que impedem DROP
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public REVOKE ALL ON TABLES FROM helpdesk_user;

-- 2. Troca o owner do schema se ainda for necessário
ALTER SCHEMA public OWNER TO postgres;

-- 3. Dropa o banco e o usuário antigo
DROP DATABASE IF EXISTS helpdesk_db;
DROP ROLE IF EXISTS helpdesk_user;

-- 4. Cria o novo usuário e banco
CREATE USER helpdesk_user WITH PASSWORD '96462191';
CREATE DATABASE helpdesk_db OWNER helpdesk_user;

-- 5. Conecta ao novo banco
\c helpdesk_db

-- 6. Garante o dono do schema e permissões futuras
ALTER SCHEMA public OWNER TO helpdesk_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO helpdesk_user;
GRANT ALL PRIVILEGES ON DATABASE helpdesk_db TO helpdesk_user;
