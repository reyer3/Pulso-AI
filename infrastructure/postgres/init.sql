-- 🗄️ PostgreSQL Development Database Initialization
-- Script ejecutado automáticamente cuando se inicia el container de PostgreSQL

-- Configurar timezone y locale
SET timezone = 'UTC';
SET client_encoding = 'UTF8';

-- =====================================
-- 🔐 CREAR ROLES Y USUARIOS ADICIONALES
-- =====================================

-- El usuario principal ya está creado por variables de entorno:
-- POSTGRES_USER=pulso_user, POSTGRES_PASSWORD=pulso_dev_password, POSTGRES_DB=pulso_dev

-- Usuario de solo lectura para análisis
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'pulso_user_readonly') THEN
        CREATE USER pulso_user_readonly WITH PASSWORD 'readonly_dev_2024';
    END IF;
END $$;

-- Usuario para testing
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'pulso_user_test') THEN
        CREATE USER pulso_user_test WITH PASSWORD 'test_password_2024';
    END IF;
END $$;

-- =====================================
-- 🏗️ CREAR DATABASES ADICIONALES
-- =====================================

-- Database principal ya creada por POSTGRES_DB=pulso_dev

-- Database para testing
SELECT 'CREATE DATABASE pulso_test WITH OWNER = pulso_user_test ENCODING = ''UTF8'' LC_COLLATE = ''en_US.UTF-8'' LC_CTYPE = ''en_US.UTF-8'' TEMPLATE = template0'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'pulso_test')\gexec

-- Database para cada cliente (multi-tenant preparation)
SELECT 'CREATE DATABASE pulso_movistar_dev WITH OWNER = pulso_user ENCODING = ''UTF8'' LC_COLLATE = ''en_US.UTF-8'' LC_CTYPE = ''en_US.UTF-8'' TEMPLATE = template0'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'pulso_movistar_dev')\gexec

SELECT 'CREATE DATABASE pulso_claro_dev WITH OWNER = pulso_user ENCODING = ''UTF8'' LC_COLLATE = ''en_US.UTF-8'' LC_CTYPE = ''en_US.UTF-8'' TEMPLATE = template0'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'pulso_claro_dev')\gexec

-- =====================================
-- 🔑 CONFIGURAR PERMISOS
-- =====================================

-- Conectar a database principal
\c pulso_dev;

-- Crear schemas para organización
CREATE SCHEMA IF NOT EXISTS core;
CREATE SCHEMA IF NOT EXISTS clients;
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS audit;

-- Permisos para usuario principal (pulso_user ya es owner)
GRANT ALL PRIVILEGES ON DATABASE pulso_dev TO pulso_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO pulso_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA core TO pulso_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA clients TO pulso_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA analytics TO pulso_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA audit TO pulso_user;

-- Permisos para usuario de solo lectura
GRANT CONNECT ON DATABASE pulso_dev TO pulso_user_readonly;
GRANT USAGE ON SCHEMA public, core, clients, analytics TO pulso_user_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO pulso_user_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA core TO pulso_user_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA clients TO pulso_user_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA analytics TO pulso_user_readonly;

-- Permisos por defecto para tablas futuras
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO pulso_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA core GRANT ALL ON TABLES TO pulso_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA clients GRANT ALL ON TABLES TO pulso_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA analytics GRANT ALL ON TABLES TO pulso_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA audit GRANT ALL ON TABLES TO pulso_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO pulso_user_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA core GRANT SELECT ON TABLES TO pulso_user_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA clients GRANT SELECT ON TABLES TO pulso_user_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA analytics GRANT SELECT ON TABLES TO pulso_user_readonly;

-- =====================================
-- 🔧 EXTENSIONES ÚTILES
-- =====================================

-- UUID generation (corregido con comillas)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Cryptographic functions
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Full text search
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Time functions
CREATE EXTENSION IF NOT EXISTS btree_gist;

-- =====================================
-- 📊 TABLAS BASE DE DESARROLLO
-- =====================================

-- Tabla de configuración global
CREATE TABLE IF NOT EXISTS core.settings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    key VARCHAR(255) UNIQUE NOT NULL,
    value JSONB NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla de clientes para multi-tenancy
CREATE TABLE IF NOT EXISTS clients.client_configs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id VARCHAR(100) UNIQUE NOT NULL,
    client_name VARCHAR(255) NOT NULL,
    database_config JSONB NOT NULL,
    dashboard_config JSONB NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla de auditoría
CREATE TABLE IF NOT EXISTS audit.activity_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id VARCHAR(100),
    user_id VARCHAR(255),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100),
    resource_id VARCHAR(255),
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_activity_log_client_id ON audit.activity_log(client_id);
CREATE INDEX IF NOT EXISTS idx_activity_log_created_at ON audit.activity_log(created_at);
CREATE INDEX IF NOT EXISTS idx_activity_log_action ON audit.activity_log(action);

-- =====================================
-- 🎯 DATOS DE DESARROLLO
-- =====================================

-- Configuración inicial
INSERT INTO core.settings (key, value, description) VALUES
    ('app_version', '"0.1.0"', 'Versión actual de la aplicación'),
    ('maintenance_mode', 'false', 'Modo de mantenimiento activado'),
    ('max_clients', '50', 'Número máximo de clientes simultáneos'),
    ('default_cache_ttl', '300', 'TTL por defecto del cache en segundos')
ON CONFLICT (key) DO NOTHING;

-- Cliente de ejemplo: Movistar Perú
INSERT INTO clients.client_configs (client_id, client_name, database_config, dashboard_config) VALUES
    ('movistar-peru', 'Movistar Perú', 
     '{"type": "bigquery", "project": "mibot-222814", "dataset": "BI_USA", "table": "dash_P3fV4dWNeMkN5RJMhV8e_vw_operativo"}',
     '{"dimensions": {"ejecutivo": {"type": "categorical", "affects": ["cartera", "servicio"]}, "cartera": {"type": "categorical", "values": ["Gestión Temprana", "Altas Nuevas"]}, "servicio": {"type": "categorical", "values": ["MOVIL", "FIJA"]}}, "metrics": {"pdps_por_hora": {"formula": "pdp_count / horas_trabajadas", "thresholds": {"warning": 2, "good": 5}}, "tasa_contactabilidad": {"formula": "(contactos / total_gestiones) * 100", "thresholds": {"poor": 30, "warning": 50, "good": 70}}}}')
ON CONFLICT (client_id) DO NOTHING;

-- =====================================
-- 🔄 FUNCIONES Y TRIGGERS
-- =====================================

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para updated_at
DROP TRIGGER IF EXISTS update_settings_updated_at ON core.settings;
CREATE TRIGGER update_settings_updated_at BEFORE UPDATE ON core.settings 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_client_configs_updated_at ON clients.client_configs;
CREATE TRIGGER update_client_configs_updated_at BEFORE UPDATE ON clients.client_configs 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Función para logging automático de actividad
CREATE OR REPLACE FUNCTION log_activity(
    p_client_id VARCHAR(100),
    p_user_id VARCHAR(255),
    p_action VARCHAR(100),
    p_resource_type VARCHAR(100) DEFAULT NULL,
    p_resource_id VARCHAR(255) DEFAULT NULL,
    p_details JSONB DEFAULT NULL
) RETURNS UUID AS $$
DECLARE
    log_id UUID;
BEGIN
    INSERT INTO audit.activity_log (client_id, user_id, action, resource_type, resource_id, details)
    VALUES (p_client_id, p_user_id, p_action, p_resource_type, p_resource_id, p_details)
    RETURNING id INTO log_id;
    
    RETURN log_id;
END;
$$ LANGUAGE plpgsql;

-- =====================================
-- ✅ VERIFICACIÓN FINAL
-- =====================================

-- Verificar que todo se creó correctamente
DO $$
BEGIN
    RAISE NOTICE '🎉 PostgreSQL development database initialized successfully!';
    RAISE NOTICE '📊 Databases: pulso_dev (main), pulso_test, pulso_movistar_dev, pulso_claro_dev';
    RAISE NOTICE '👥 Users: pulso_user (main), pulso_user_readonly, pulso_user_test';
    RAISE NOTICE '🏗️ Schemas: core, clients, analytics, audit';
    RAISE NOTICE '🔧 Extensions: uuid-ossp, pgcrypto, pg_trgm, btree_gist';
    RAISE NOTICE '🚀 Ready for Pulso-AI development!';
END $$;
