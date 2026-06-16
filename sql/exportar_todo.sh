#!/bin/bash
# Script para exportar todos los datos de la base de datos

echo "=========================================="
echo "   EXPORTANDO DATOS DEL LMS"
echo "=========================================="

DB="lms_tecnicas/db.sqlite3"
EXPORT_DIR="sql/export"
BACKUP_DIR="sql/backups"

# Crear carpetas
mkdir -p $EXPORT_DIR $BACKUP_DIR

# 1. Backup de la BD
cp $DB $BACKUP_DIR/db_backup_$(date +%Y%m%d_%H%M%S).sqlite3
echo "✅ Backup creado"

# 2. Exportar a CSV
for table in tecnicas usuarios categorias progreso_estudiante; do
    sqlite3 $DB "SELECT * FROM $table;" > $EXPORT_DIR/${table}.csv
    echo "✅ $table exportado a CSV"
done

# 3. Exportar a SQL (INSERT)
for table in tecnicas categorias; do
    sqlite3 $DB ".mode insert $table" ".output $EXPORT_DIR/${table}_insert.sql" "SELECT * FROM $table;" ".output stdout"
    echo "✅ $table exportado a SQL INSERT"
done

# 4. Exportar esquema
sqlite3 $DB ".schema" > $EXPORT_DIR/schema.sql
echo "✅ Esquema exportado"

# 5. Resumen
echo ""
echo "=========================================="
echo "   RESUMEN DE EXPORTACIÓN"
echo "=========================================="
echo "📁 Backups: $BACKUP_DIR"
echo "📁 Exportaciones: $EXPORT_DIR"
echo ""
echo "Archivos generados:"
ls -la $EXPORT_DIR/
echo ""
echo "✅ Exportación completada"
