-- ============================================================
-- CREACIÓN DE LA BASE DE DATOS LMS (SQLite)
-- ============================================================

-- Tabla de usuarios (extendida)
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

-- Tabla de técnicas
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

-- Tabla de progreso
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

-- Tabla de respuestas
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

-- Tabla de categorías
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT,
    icono VARCHAR(50)
);

-- Insertar categorías de ejemplo
INSERT OR IGNORE INTO categorias (nombre, descripcion, icono) VALUES 
('Comunicación escrita', 'Técnicas de redacción, APA, coherencia', '📝'),
('Lectura crítica', 'Niveles, tipos textuales, estrategias', '📖'),
('Morfología flexiva', 'Género, número, tiempo, modo, aspecto', '🎭'),
('Derivación', 'Prefijación, sufijación, interfijación, parasíntesis', '⚙️'),
('Formación de palabras', 'Composición, acronimia, siglación', '🧩'),
('Estándares MEN', 'Grados 1° a 11°, ejes de lenguaje', '📘');

-- Índices para optimización
CREATE INDEX IF NOT EXISTS idx_progreso_estudiante ON progreso_estudiante(estudiante_id, tecnica_id);
CREATE INDEX IF NOT EXISTS idx_tecnica_categoria ON tecnicas(categoria);
CREATE INDEX IF NOT EXISTS idx_tecnica_grado ON tecnicas(grado);
