-- ============================================================
-- BASE DE DATOS LMS - CREACIÓN COMPLETA
-- ============================================================
-- Este script crea toda la base de datos desde cero

-- 1. TABLA DE USUARIOS (extendida)
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    email VARCHAR(254) UNIQUE,
    is_active BOOLEAN DEFAULT 1,
    is_staff BOOLEAN DEFAULT 0,
    is_superuser BOOLEAN DEFAULT 0,
    date_joined DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    es_profesor BOOLEAN DEFAULT 0,
    es_estudiante BOOLEAN DEFAULT 1
);

-- 2. TABLA DE TÉCNICAS
CREATE TABLE IF NOT EXISTS tecnicas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo VARCHAR(200) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    contenido_html TEXT NOT NULL,
    grado VARCHAR(50),
    orden INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3. TABLA DE PROGRESO
CREATE TABLE IF NOT EXISTS progreso_estudiante (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    estudiante_id INTEGER NOT NULL,
    tecnica_id INTEGER NOT NULL,
    completada BOOLEAN DEFAULT 0,
    ultima_respuesta TEXT,
    intentos INTEGER DEFAULT 0,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (estudiante_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (tecnica_id) REFERENCES tecnicas(id) ON DELETE CASCADE,
    UNIQUE(estudiante_id, tecnica_id)
);

-- 4. TABLA DE CATEGORÍAS
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT,
    icono VARCHAR(50)
);

-- 5. TABLA DE RESPUESTAS
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

-- 9. ÍNDICES PARA OPTIMIZACIÓN
CREATE INDEX IF NOT EXISTS idx_progreso_estudiante ON progreso_estudiante(estudiante_id, tecnica_id);
CREATE INDEX IF NOT EXISTS idx_tecnica_categoria ON tecnicas(categoria);
CREATE INDEX IF NOT EXISTS idx_tecnica_grado ON tecnicas(grado);

-- 10. INSERTAR CATEGORÍAS BASE
INSERT OR IGNORE INTO categorias (nombre, descripcion, icono) VALUES 
('Morfología flexiva', 'Género, número, tiempo, modo, aspecto, persona', '🎭'),
('Derivación', 'Prefijación, sufijación, interfijación, parasíntesis', '⚙️'),
('Clases de palabras', 'Sustantivos, adjetivos, verbos, adverbios, preposiciones...', '📂'),
('Formación de palabras', 'Composición, acronimia, siglación', '🧩'),
('Accidentes gramaticales', 'Caso, grado, voz, definitud', '⚡'),
('Morfemática', 'Lexema, morfema, alomorfo, tema, base, raíz, interfijo', '🧬'),
('Estándares MEN', 'Grados 1° a 11°, ejes de lenguaje', '📘'),
('Concurso docente', 'Competencias docentes, pedagogía', '🍎');

-- 11. VISTA DE ESTADÍSTICAS
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
