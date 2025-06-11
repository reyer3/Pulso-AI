-- =====================================================
-- 📊 TELEFONICA DATAMART - INITIAL SCHEMA
-- =====================================================
-- Creates basic dimensional schema for Telefónica Perú
-- Support for BigQuery → PostgreSQL ETL pipeline

-- Create schema
CREATE SCHEMA IF NOT EXISTS telefonica;

-- Set default schema for this session
SET search_path = telefonica, public;

-- =====================================================
-- 🏗️ DIMENSIONAL TABLES
-- =====================================================

-- DIM_TIEMPO - Date dimension
CREATE TABLE IF NOT EXISTS dim_tiempo (
    fecha_id SERIAL PRIMARY KEY,
    fecha DATE UNIQUE NOT NULL,
    ano INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    dia INTEGER NOT NULL,
    dia_semana INTEGER NOT NULL, -- 1=Monday, 7=Sunday
    nombre_dia VARCHAR(10) NOT NULL,
    nombre_mes VARCHAR(10) NOT NULL,
    es_fin_semana BOOLEAN NOT NULL DEFAULT FALSE,
    es_feriado BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- DIM_CLIENTE - Customer dimension  
CREATE TABLE IF NOT EXISTS dim_cliente (
    cliente_id SERIAL PRIMARY KEY,
    cod_luna INTEGER UNIQUE NOT NULL,
    cliente VARCHAR(255),
    documento_identidad VARCHAR(20),
    tipo_documento VARCHAR(10),
    linea_servicio VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- DIM_EJECUTIVO - Agent dimension
CREATE TABLE IF NOT EXISTS dim_ejecutivo (
    ejecutivo_id SERIAL PRIMARY KEY,
    ejecutivo VARCHAR(255) UNIQUE NOT NULL,
    tipo_agente VARCHAR(20) NOT NULL DEFAULT 'HUMANO', -- HUMANO, VOICEBOT
    equipo VARCHAR(100),
    supervisor VARCHAR(255),
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- DIM_CANAL - Channel dimension
CREATE TABLE IF NOT EXISTS dim_canal (
    canal_id SERIAL PRIMARY KEY,
    canal VARCHAR(50) UNIQUE NOT NULL, -- CALL, VOICEBOT, WHATSAPP, etc.
    es_automatico BOOLEAN NOT NULL DEFAULT FALSE,
    costo_promedio DECIMAL(10,2),
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- DIM_CARTERA - Portfolio type dimension
CREATE TABLE IF NOT EXISTS dim_cartera (
    cartera_id SERIAL PRIMARY KEY,
    tipo_cartera VARCHAR(100) UNIQUE NOT NULL, -- Gestión Temprana, AN, CF, Regular
    dias_mora_min INTEGER,
    dias_mora_max INTEGER,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- DIM_SERVICIO - Service line dimension
CREATE TABLE IF NOT EXISTS dim_servicio (
    servicio_id SERIAL PRIMARY KEY,
    servicio VARCHAR(50) UNIQUE NOT NULL, -- MOVIL, FIJA
    descripcion TEXT,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- 📈 FACT TABLES
-- =====================================================

-- FACT_GESTIONES - Management activities fact table
-- GRAIN: fecha + hora + ejecutivo + canal + cliente
CREATE TABLE IF NOT EXISTS fact_gestiones (
    gestion_id SERIAL PRIMARY KEY,
    
    -- Foreign keys to dimensions
    fecha_id INTEGER REFERENCES dim_tiempo(fecha_id),
    cliente_id INTEGER REFERENCES dim_cliente(cliente_id),
    ejecutivo_id INTEGER REFERENCES dim_ejecutivo(ejecutivo_id),
    canal_id INTEGER REFERENCES dim_canal(canal_id),
    cartera_id INTEGER REFERENCES dim_cartera(cartera_id),
    servicio_id INTEGER REFERENCES dim_servicio(servicio_id),
    
    -- Business attributes
    hora_gestion TIME NOT NULL,
    contactabilidad VARCHAR(50), -- CONTACTO EFECTIVO, NO CONTACTO, etc.
    tipificacion_original VARCHAR(100),
    tipificacion_homologada VARCHAR(100),
    es_pdp BOOLEAN NOT NULL DEFAULT FALSE,
    es_compromiso BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- Metrics
    duracion_segundos INTEGER DEFAULT 0,
    monto_gestionado DECIMAL(12,2) DEFAULT 0,
    
    -- Audit fields
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- Unique constraint on business key
    UNIQUE(fecha_id, ejecutivo_id, canal_id, cliente_id, hora_gestion)
);

-- FACT_GESTIONES_AGREGADAS - Aggregated daily metrics
-- GRAIN: fecha + ejecutivo + canal
CREATE TABLE IF NOT EXISTS fact_gestiones_agregadas (
    agregacion_id SERIAL PRIMARY KEY,
    
    -- Foreign keys
    fecha_id INTEGER REFERENCES dim_tiempo(fecha_id),
    ejecutivo_id INTEGER REFERENCES dim_ejecutivo(ejecutivo_id),
    canal_id INTEGER REFERENCES dim_canal(canal_id),
    
    -- Aggregated metrics
    total_gestiones INTEGER NOT NULL DEFAULT 0,
    contactos_efectivos INTEGER NOT NULL DEFAULT 0,
    no_contactos INTEGER NOT NULL DEFAULT 0,
    gestiones_pdp INTEGER NOT NULL DEFAULT 0,
    gestiones_compromiso INTEGER NOT NULL DEFAULT 0,
    
    -- Calculated metrics
    tasa_contactabilidad DECIMAL(5,2), -- Percentage
    pdps_por_hora DECIMAL(5,2),
    efectividad DECIMAL(5,2), -- Percentage
    
    -- Time tracking
    duracion_total_segundos INTEGER DEFAULT 0,
    horas_trabajadas DECIMAL(5,2) DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT NOW(),
    
    -- Unique constraint
    UNIQUE(fecha_id, ejecutivo_id, canal_id)
);

-- =====================================================
-- 🔍 INDEXES FOR PERFORMANCE
-- =====================================================

-- Indexes on fact tables for common queries
CREATE INDEX IF NOT EXISTS idx_fact_gestiones_fecha ON fact_gestiones(fecha_id);
CREATE INDEX IF NOT EXISTS idx_fact_gestiones_ejecutivo ON fact_gestiones(ejecutivo_id);
CREATE INDEX IF NOT EXISTS idx_fact_gestiones_canal ON fact_gestiones(canal_id);
CREATE INDEX IF NOT EXISTS idx_fact_gestiones_cliente ON fact_gestiones(cliente_id);
CREATE INDEX IF NOT EXISTS idx_fact_gestiones_fecha_ejecutivo ON fact_gestiones(fecha_id, ejecutivo_id);

CREATE INDEX IF NOT EXISTS idx_fact_agregadas_fecha ON fact_gestiones_agregadas(fecha_id);
CREATE INDEX IF NOT EXISTS idx_fact_agregadas_ejecutivo ON fact_gestiones_agregadas(ejecutivo_id);

-- Indexes on dimension tables
CREATE INDEX IF NOT EXISTS idx_dim_tiempo_fecha ON dim_tiempo(fecha);
CREATE INDEX IF NOT EXISTS idx_dim_cliente_cod_luna ON dim_cliente(cod_luna);
CREATE INDEX IF NOT EXISTS idx_dim_ejecutivo_nombre ON dim_ejecutivo(ejecutivo);

-- =====================================================
-- 📊 INITIAL DATA LOAD
-- =====================================================

-- Insert default time dimension (last 90 days + future 30 days)
INSERT INTO dim_tiempo (fecha, ano, mes, dia, dia_semana, nombre_dia, nombre_mes, es_fin_semana)
SELECT 
    fecha::date,
    EXTRACT(YEAR FROM fecha) AS ano,
    EXTRACT(MONTH FROM fecha) AS mes,
    EXTRACT(DAY FROM fecha) AS dia,
    EXTRACT(DOW FROM fecha) AS dia_semana,
    TO_CHAR(fecha, 'Day') AS nombre_dia,
    TO_CHAR(fecha, 'Month') AS nombre_mes,
    EXTRACT(DOW FROM fecha) IN (0, 6) AS es_fin_semana
FROM generate_series(
    CURRENT_DATE - INTERVAL '90 days',
    CURRENT_DATE + INTERVAL '30 days',
    INTERVAL '1 day'
) AS fecha
ON CONFLICT (fecha) DO NOTHING;

-- Insert default channels
INSERT INTO dim_canal (canal, es_automatico, descripcion) VALUES
    ('CALL', FALSE, 'Llamadas con agente humano'),
    ('VOICEBOT', TRUE, 'Llamadas automatizadas con bot'),
    ('WHATSAPP', FALSE, 'Mensajería WhatsApp'),
    ('SMS', TRUE, 'Mensajes de texto automatizados'),
    ('EMAIL', TRUE, 'Correo electrónico'),
    ('VISITA', FALSE, 'Visita presencial'),
    ('CARTA', FALSE, 'Carta física'),
    ('AUTOATENCION', TRUE, 'Autoatención digital')
ON CONFLICT (canal) DO NOTHING;

-- Insert default service lines
INSERT INTO dim_servicio (servicio, descripcion) VALUES
    ('MOVIL', 'Telefonía móvil'),
    ('FIJA', 'Telefonía fija'),
    ('INTERNET', 'Internet banda ancha'),
    ('TV', 'Televisión por cable')
ON CONFLICT (servicio) DO NOTHING;

-- Insert default portfolio types
INSERT INTO dim_cartera (tipo_cartera, dias_mora_min, dias_mora_max, descripcion) VALUES
    ('Gestión Temprana', 1, 30, 'Clientes con mora reciente'),
    ('Altas Nuevas', 31, 60, 'Nuevos clientes en mora'),
    ('CF', 61, 120, 'Cartera en cobranza firme'),
    ('Regular', 121, 365, 'Cartera regular de cobranza')
ON CONFLICT (tipo_cartera) DO NOTHING;

-- =====================================================
-- 🔐 SECURITY & PERMISSIONS
-- =====================================================

-- Create application user permissions
GRANT USAGE ON SCHEMA telefonica TO pulso_ai;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA telefonica TO pulso_ai;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA telefonica TO pulso_ai;

-- Grant permissions on future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA telefonica 
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO pulso_ai;

-- =====================================================
-- 📝 HELPFUL VIEWS
-- =====================================================

-- View for easy querying with dimension names
CREATE OR REPLACE VIEW v_gestiones_completa AS
SELECT 
    fg.gestion_id,
    dt.fecha,
    fg.hora_gestion,
    de.ejecutivo,
    dc.canal,
    dcl.cod_luna,
    dcl.cliente,
    dcar.tipo_cartera,
    ds.servicio,
    fg.contactabilidad,
    fg.tipificacion_homologada,
    fg.es_pdp,
    fg.es_compromiso,
    fg.duracion_segundos,
    fg.monto_gestionado
FROM fact_gestiones fg
JOIN dim_tiempo dt ON fg.fecha_id = dt.fecha_id
JOIN dim_ejecutivo de ON fg.ejecutivo_id = de.ejecutivo_id
JOIN dim_canal dc ON fg.canal_id = dc.canal_id
JOIN dim_cliente dcl ON fg.cliente_id = dcl.cliente_id
JOIN dim_cartera dcar ON fg.cartera_id = dcar.cartera_id
JOIN dim_servicio ds ON fg.servicio_id = ds.servicio_id;

-- View for aggregated metrics
CREATE OR REPLACE VIEW v_metricas_diarias AS
SELECT 
    dt.fecha,
    de.ejecutivo,
    dc.canal,
    fga.total_gestiones,
    fga.contactos_efectivos,
    fga.gestiones_pdp,
    fga.tasa_contactabilidad,
    fga.pdps_por_hora,
    fga.efectividad,
    fga.horas_trabajadas
FROM fact_gestiones_agregadas fga
JOIN dim_tiempo dt ON fga.fecha_id = dt.fecha_id
JOIN dim_ejecutivo de ON fga.ejecutivo_id = de.ejecutivo_id
JOIN dim_canal dc ON fga.canal_id = dc.canal_id
ORDER BY dt.fecha DESC, fga.total_gestiones DESC;

-- =====================================================
-- ✅ SCHEMA INITIALIZATION COMPLETE
-- =====================================================

-- Verify schema creation
SELECT 
    schemaname,
    tablename,
    tableowner
FROM pg_tables 
WHERE schemaname = 'telefonica'
ORDER BY tablename;

COMMIT;