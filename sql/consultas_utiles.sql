-- ============================================================
-- CONSULTAS ÚTILES PARA EL LMS
-- ============================================================

-- 1. Ver todas las técnicas con sus categorías
SELECT id, titulo, categoria, grado FROM tecnicas ORDER BY id;

-- 2. Contar técnicas por categoría
SELECT categoria, COUNT(*) AS total FROM tecnicas GROUP BY categoria ORDER BY total DESC;

-- 3. Técnicas más recientes
SELECT id, titulo, created_at FROM tecnicas ORDER BY created_at DESC LIMIT 10;

-- 4. Progreso de un estudiante específico (reemplazar 1 por el id)
SELECT 
    t.id,
    t.titulo,
    t.categoria,
    CASE 
        WHEN p.completada = 1 THEN '✅ Completada'
        WHEN p.id IS NOT NULL THEN '⏳ En progreso'
        ELSE '⚪ Sin iniciar'
    END AS estado,
    p.fecha_actualizacion
FROM tecnicas t
LEFT JOIN progreso_estudiante p ON t.id = p.tecnica_id AND p.estudiante_id = 1
ORDER BY t.id;

-- 5. Estadísticas de todos los estudiantes
SELECT 
    u.username,
    u.first_name,
    u.last_name,
    COUNT(p.tecnica_id) AS intentadas,
    SUM(CASE WHEN p.completada = 1 THEN 1 ELSE 0 END) AS completadas,
    ROUND(CAST(SUM(CASE WHEN p.completada = 1 THEN 1 ELSE 0 END) AS FLOAT) / 
          COUNT(p.tecnica_id) * 100, 1) AS porcentaje
FROM usuarios u
JOIN progreso_estudiante p ON u.id = p.estudiante_id
WHERE u.es_estudiante = 1
GROUP BY u.id;

-- 6. Técnicas más completadas por estudiantes
SELECT 
    t.titulo,
    t.categoria,
    COUNT(p.estudiante_id) AS veces_completada
FROM tecnicas t
JOIN progreso_estudiante p ON t.id = p.tecnica_id AND p.completada = 1
GROUP BY t.id
ORDER BY veces_completada DESC
LIMIT 10;

-- 7. Usuarios por rol
SELECT 
    'Estudiante' AS rol,
    COUNT(*) AS total
FROM usuarios
WHERE es_estudiante = 1
UNION ALL
SELECT 
    'Profesor',
    COUNT(*)
FROM usuarios
WHERE es_profesor = 1 OR is_staff = 1;

-- 8. Técnicas con ejercicios (contenido HTML que contiene 'ejercicio')
SELECT id, titulo FROM tecnicas WHERE contenido_html LIKE '%ejercicio%';

-- 9. Técnicas por grado (estándares MEN)
SELECT grado, COUNT(*) AS total FROM tecnicas WHERE grado != '' GROUP BY grado;

-- 10. Resumen general del sistema
SELECT 
    (SELECT COUNT(*) FROM usuarios) AS total_usuarios,
    (SELECT COUNT(*) FROM tecnicas) AS total_tecnicas,
    (SELECT COUNT(DISTINCT categoria) FROM tecnicas) AS total_categorias,
    (SELECT COUNT(*) FROM progreso_estudiante) AS total_progresos,
    (SELECT COUNT(*) FROM progreso_estudiante WHERE completada = 1) AS completadas;
