-- ============================================================
-- ESQUEMA COMPLETO DE LA BASE DE DATOS LMS
-- ============================================================
-- Generado automáticamente desde la base de datos

PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

-- 1. TABLA DE USUARIOS
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME NULL,
    is_superuser BOOLEAN NOT NULL,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    date_joined DATETIME NOT NULL,
    es_profesor BOOLEAN NOT NULL,
    es_estudiante BOOLEAN NOT NULL
);

-- 2. TABLA DE TÉCNICAS
CREATE TABLE IF NOT EXISTS tecnicas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo VARCHAR(200) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    contenido_html TEXT NOT NULL,
    grado VARCHAR(50) NULL,
    orden INTEGER NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

-- 3. TABLA DE PROGRESO
CREATE TABLE IF NOT EXISTS progreso_estudiante (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    estudiante_id BIGINT NOT NULL,
    tecnica_id BIGINT NOT NULL,
    completada BOOLEAN NOT NULL,
    ultima_respuesta TEXT NOT NULL,
    intentos INTEGER NOT NULL,
    fecha_actualizacion DATETIME NOT NULL,
    FOREIGN KEY (estudiante_id) REFERENCES usuarios (id) ON DELETE CASCADE,
    FOREIGN KEY (tecnica_id) REFERENCES tecnicas (id) ON DELETE CASCADE,
    UNIQUE(estudiante_id, tecnica_id)
);

-- 4. TABLA DE CATEGORÍAS
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT,
    icono VARCHAR(50)
);

-- 5. TABLA DE RESPUESTAS DE EJERCICIOS
CREATE TABLE IF NOT EXISTS respuestas_ejercicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    estudiante_id INTEGER NOT NULL,
    tecnica_id INTEGER NOT NULL,
    respuesta_usuario TEXT,
    respuesta_correcta TEXT,
    es_correcta BOOLEAN DEFAULT 0,
    fecha_respuesta DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (estudiante_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (tecnica_id) REFERENCES tecnicas(id) ON DELETE CASCADE
);

-- 6. TABLA DE FAVORITOS
CREATE TABLE IF NOT EXISTS favoritos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    estudiante_id INTEGER NOT NULL,
    tecnica_id INTEGER NOT NULL,
    fecha_agregado DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (estudiante_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (tecnica_id) REFERENCES tecnicas(id) ON DELETE CASCADE,
    UNIQUE(estudiante_id, tecnica_id)
);

-- 7. TABLA DE ETIQUETAS
CREATE TABLE IF NOT EXISTS etiquetas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(50) UNIQUE NOT NULL
);

-- 8. RELACIÓN TÉCNICA-ETIQUETA
CREATE TABLE IF NOT EXISTS tecnica_etiqueta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tecnica_id INTEGER NOT NULL,
    etiqueta_id INTEGER NOT NULL,
    FOREIGN KEY (tecnica_id) REFERENCES tecnicas(id) ON DELETE CASCADE,
    FOREIGN KEY (etiqueta_id) REFERENCES etiquetas(id) ON DELETE CASCADE,
    UNIQUE(tecnica_id, etiqueta_id)
);

-- 9. TABLA DE GRUPOS DE USUARIOS
CREATE TABLE IF NOT EXISTS usuarios_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id BIGINT NOT NULL,
    group_id INTEGER NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES auth_group(id) ON DELETE CASCADE,
    UNIQUE(usuario_id, group_id)
);

-- 10. TABLA DE PERMISOS DE USUARIOS
CREATE TABLE IF NOT EXISTS usuarios_user_permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id BIGINT NOT NULL,
    permission_id INTEGER NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES auth_permission(id) ON DELETE CASCADE,
    UNIQUE(usuario_id, permission_id)
);

-- 11. ÍNDICES
CREATE INDEX idx_progreso_estudiante ON progreso_estudiante(estudiante_id, tecnica_id);
CREATE INDEX idx_tecnica_categoria ON tecnicas(categoria);
CREATE INDEX idx_tecnica_grado ON tecnicas(grado);
CREATE INDEX idx_progreso_estudiante_estudiante_id ON progreso_estudiante(estudiante_id);
CREATE INDEX idx_progreso_estudiante_tecnica_id ON progreso_estudiante(tecnica_id);

-- 12. VISTA DE ESTADÍSTICAS
CREATE VIEW IF NOT EXISTS estadisticas_estudiantes AS
SELECT 
    u.id AS usuario_id,
    u.username,
    u.first_name,
    u.last_name,
    COUNT(DISTINCT pe.tecnica_id) AS tecnicas_completadas,
    (SELECT COUNT(*) FROM tecnicas) AS total_tecnicas,
    ROUND(CAST(COUNT(DISTINCT pe.tecnica_id) AS FLOAT) / 
          (SELECT COUNT(*) FROM tecnicas) * 100, 1) AS porcentaje
FROM usuarios u
LEFT JOIN progreso_estudiante pe ON u.id = pe.estudiante_id AND pe.completada = 1
WHERE u.es_estudiante = 1
GROUP BY u.id;

COMMIT;
PRAGMA foreign_keys=ON;
