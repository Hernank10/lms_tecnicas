-- ============================================================
-- LIMPIAR DATOS (RESET) - ¡CUIDADO!
-- ============================================================
-- ⚠️ ADVERTENCIA: Este script ELIMINA TODOS LOS DATOS de la base de datos.
-- Se recomienda hacer un backup antes de ejecutarlo.
-- ============================================================

-- Desactivar verificaciones de integridad
PRAGMA foreign_keys=OFF;

-- Eliminar progreso de estudiantes
DELETE FROM progreso_estudiante;

-- Eliminar respuestas de ejercicios
DELETE FROM respuestas_ejercicios;

-- Eliminar favoritos
DELETE FROM favoritos;

-- Eliminar relación técnica-etiqueta
DELETE FROM tecnica_etiqueta;

-- Eliminar etiquetas
DELETE FROM etiquetas;

-- Eliminar técnicas
DELETE FROM tecnicas;

-- Eliminar categorías
DELETE FROM categorias;

-- Eliminar usuarios (¡cuidado!)
DELETE FROM usuarios;

-- Resetear secuencias (auto increment)
DELETE FROM sqlite_sequence WHERE name IN ('tecnicas', 'usuarios', 'progreso_estudiante', 'categorias', 'etiquetas');

-- Reactivar verificaciones
PRAGMA foreign_keys=ON;

-- ============================================================
-- VERIFICACIÓN POST-RESET
-- ============================================================
SELECT '📊 DATOS ACTUALES:' AS '';
SELECT 'Técnicas: ' || COUNT(*) AS resultado FROM tecnicas;
SELECT 'Usuarios: ' || COUNT(*) FROM usuarios;
SELECT 'Categorías: ' || COUNT(*) FROM categorias;
SELECT 'Progresos: ' || COUNT(*) FROM progreso_estudiante;
SELECT '========================================';
SELECT '✅ Base de datos limpia. Lista para recargar datos.';

-- Insertar categorías base (opcional)
INSERT OR IGNORE INTO categorias (nombre, descripcion, icono) VALUES 
('Morfología flexiva', 'Género, número, tiempo, modo, aspecto, persona', '🎭'),
('Derivación', 'Prefijación, sufijación, interfijación, parasíntesis', '⚙️'),
('Clases de palabras', 'Sustantivos, adjetivos, verbos, adverbios, preposiciones...', '📂'),
('Formación de palabras', 'Composición, acronimia, siglación', '🧩'),
('Accidentes gramaticales', 'Caso, grado, voz, definitud', '⚡'),
('Morfemática', 'Lexema, morfema, alomorfo, tema, base, raíz, interfijo', '🧬'),
('Estándares MEN', 'Grados 1° a 11°, ejes de lenguaje', '📘'),
('Concurso docente', 'Competencias docentes, pedagogía', '🍎');

SELECT '✅ Categorías base insertadas.';
