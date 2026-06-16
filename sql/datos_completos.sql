-- ============================================================
-- DATOS COMPLETOS DEL LMS
-- ============================================================
-- Este archivo contiene todos los datos de la base de datos
-- para restaurar el sistema en caso de ser necesario
-- ============================================================

-- Categorías
INSERT OR IGNORE INTO categorias (id, nombre, descripcion, icono) VALUES 
(1, 'Morfología flexiva', 'Género, número, tiempo, modo, aspecto, persona', '🎭'),
(2, 'Derivación', 'Prefijación, sufijación, interfijación, parasíntesis', '⚙️'),
(3, 'Clases de palabras', 'Sustantivos, adjetivos, verbos, adverbios, preposiciones...', '📂'),
(4, 'Formación de palabras', 'Composición, acronimia, siglación', '🧩'),
(5, 'Accidentes gramaticales', 'Caso, grado, voz, definitud', '⚡'),
(6, 'Morfemática', 'Lexema, morfema, alomorfo, tema, base, raíz, interfijo', '🧬'),
(7, 'Estándares MEN', 'Grados 1° a 11°, ejes de lenguaje', '📘'),
(8, 'Concurso docente', 'Competencias docentes, pedagogía', '🍎'),
(9, 'Yamaha V80', 'Consejos para moto Yamaha V80', '🏍️'),
(10, 'Suzuki Nova', 'Consejos para moto Suzuki Nova 125', '🏍️'),
(11, 'Megane', 'Consejos para Renault Megane 1.6', '🚗'),
(12, 'Rutas Colombia', 'Rutas para viajar en Colombia', '🗺️'),
(13, 'Acampe', 'Consejos para acampar en carretera', '🏕️'),
(14, 'Seguridad', 'Consejos de seguridad vial', '🛡️');

-- ============================================================
-- NOTA: Las técnicas se insertan desde el script cargar_tecnicas.py
-- o desde el archivo datos_tecnicas.sql
-- ============================================================

SELECT '✅ Datos completos listos para cargar.';
