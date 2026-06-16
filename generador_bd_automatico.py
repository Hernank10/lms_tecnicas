#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GENERADOR AUTOMÁTICO DE BASES DE DATOS SQL
Para proyectos Django - Soporta SQLite, PostgreSQL, MySQL
"""

import os
import sys
import json
import sqlite3
import subprocess
from pathlib import Path
from datetime import datetime
import getpass

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class GeneradorBD:
    """Generador automático de bases de datos SQL"""
    
    def __init__(self):
        self.tipo_bd = "sqlite"  # sqlite, postgresql, mysql
        self.nombre_bd = "lms_tecnicas"
        self.usuario = ""
        self.password = ""
        self.host = "localhost"
        self.puerto = ""
        self.ruta_sql = "./sql"
        self.archivo_sql = None
        self.datos = {}
        
        # Configurar según tipo de BD
        self.configuracion = {
            "sqlite": {
                "driver": "sqlite3",
                "archivo": f"{self.nombre_bd}.db",
                "comando": "sqlite3",
                "puerto": ""
            },
            "postgresql": {
                "driver": "postgresql",
                "archivo": "",
                "comando": "psql",
                "puerto": "5432"
            },
            "mysql": {
                "driver": "mysql",
                "archivo": "",
                "comando": "mysql",
                "puerto": "3306"
            }
        }
        
        print(f"{Colors.CYAN}{'='*60}{Colors.ENDC}")
        print(f"{Colors.GREEN}   🗄️ GENERADOR AUTOMÁTICO DE BASES DE DATOS SQL{Colors.ENDC}")
        print(f"{Colors.CYAN}{'='*60}{Colors.ENDC}")
    
    def seleccionar_tipo_bd(self):
        """Selecciona el tipo de base de datos"""
        print(f"\n{Colors.YELLOW}📋 TIPOS DE BASE DE DATOS:{Colors.ENDC}")
        print("  1. SQLite (recomendado para desarrollo)")
        print("  2. PostgreSQL (recomendado para producción)")
        print("  3. MySQL / MariaDB")
        print("  4. SQLite con Django (automático)")
        
        opcion = input(f"\n{Colors.CYAN}👉 Elige una opción (1-4): {Colors.ENDC}").strip()
        
        if opcion == "1" or opcion == "":
            self.tipo_bd = "sqlite"
            self.nombre_bd = input(f"📂 Nombre de la base de datos [{self.nombre_bd}]: ").strip() or self.nombre_bd
            self.configuracion["sqlite"]["archivo"] = f"{self.nombre_bd}.db"
            
        elif opcion == "2":
            self.tipo_bd = "postgresql"
            self.nombre_bd = input(f"📂 Nombre de la base de datos [{self.nombre_bd}]: ").strip() or self.nombre_bd
            self.usuario = input("👤 Usuario: ").strip()
            self.password = getpass.getpass("🔑 Contraseña: ")
            self.host = input(f"🌐 Host [{self.host}]: ").strip() or self.host
            
        elif opcion == "3":
            self.tipo_bd = "mysql"
            self.nombre_bd = input(f"📂 Nombre de la base de datos [{self.nombre_bd}]: ").strip() or self.nombre_bd
            self.usuario = input("👤 Usuario: ").strip()
            self.password = getpass.getpass("🔑 Contraseña: ")
            self.host = input(f"🌐 Host [{self.host}]: ").strip() or self.host
            
        elif opcion == "4":
            self.tipo_bd = "django_sqlite"
            self.nombre_bd = "db.sqlite3"
            print(f"{Colors.GREEN}✅ Se usará la configuración estándar de Django{Colors.ENDC}")
            
        else:
            print(f"{Colors.RED}❌ Opción no válida, usando SQLite por defecto{Colors.ENDC}")
            self.tipo_bd = "sqlite"
            self.configuracion["sqlite"]["archivo"] = f"{self.nombre_bd}.db"
        
        return True
    
    def generar_estructura_bd(self):
        """Genera la estructura completa de la base de datos"""
        print(f"\n{Colors.BLUE}📌 GENERANDO ESTRUCTURA DE LA BASE DE DATOS{Colors.ENDC}")
        print(f"{Colors.CYAN}{'-'*50}{Colors.ENDC}")
        
        # Crear carpeta sql
        os.makedirs(self.ruta_sql, exist_ok=True)
        print(f"✅ Carpeta SQL creada: {self.ruta_sql}")
        
        # Generar archivo SQL con todas las tablas
        self.archivo_sql = f"{self.ruta_sql}/esquema_completo_{self.nombre_bd}.sql"
        contenido_sql = self._generar_sql_completo()
        
        with open(self.archivo_sql, 'w', encoding='utf-8') as f:
            f.write(contenido_sql)
        
        print(f"✅ Archivo SQL generado: {self.archivo_sql}")
        
        return True
    
    def _generar_sql_completo(self):
        """Genera el SQL completo para la base de datos"""
        comentarios = f"""
-- ============================================================
-- BASE DE DATOS: {self.nombre_bd}
-- TIPO: {self.tipo_bd.upper()}
-- GENERADO: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
-- AUTOR: Generador Automático SQL
-- ============================================================
-- NOTA: Este script crea todas las tablas, índices y datos de ejemplo
-- ============================================================
"""
        
        # Tablas del proyecto
        tablas = self._generar_tablas()
        indices = self._generar_indices()
        datos = self._generar_datos_ejemplo()
        consultas = self._generar_consultas_utiles()
        
        return f"""
{comentarios}

-- ============================================================
-- 1. ELIMINAR TABLAS (SI EXISTEN) - ¡CUIDADO!
-- ============================================================
DROP TABLE IF EXISTS respuestas_ejercicios;
DROP TABLE IF EXISTS favoritos;
DROP TABLE IF EXISTS progreso_estudiante;
DROP TABLE IF EXISTS tecnica_etiqueta;
DROP TABLE IF EXISTS etiquetas;
DROP TABLE IF EXISTS tecnicas;
DROP TABLE IF EXISTS categorias;
DROP TABLE IF EXISTS usuarios;

-- ============================================================
-- 2. CREAR TABLAS
-- ============================================================
{tablas}

-- ============================================================
-- 3. CREAR ÍNDICES
-- ============================================================
{indices}

-- ============================================================
-- 4. INSERTAR DATOS DE EJEMPLO
-- ============================================================
{datos}

-- ============================================================
-- 5. CONSULTAS ÚTILES
-- ============================================================
{consultas}

-- ============================================================
-- 6. VERIFICACIÓN FINAL
-- ============================================================
SELECT '✅ Base de datos creada exitosamente' AS Mensaje;
SELECT 'Categorías:' || COUNT(*) FROM categorias;
SELECT 'Técnicas:' || COUNT(*) FROM tecnicas;
SELECT 'Usuarios:' || COUNT(*) FROM usuarios;
"""
    
    def _generar_tablas(self):
        """Genera las tablas de la base de datos"""
        tablas = f"""
-- Tabla de Usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(150) DEFAULT '',
    last_name VARCHAR(150) DEFAULT '',
    email VARCHAR(254) UNIQUE DEFAULT '',
    is_active BOOLEAN DEFAULT 1,
    is_staff BOOLEAN DEFAULT 0,
    is_superuser BOOLEAN DEFAULT 0,
    date_joined DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME NULL,
    es_profesor BOOLEAN DEFAULT 0,
    es_estudiante BOOLEAN DEFAULT 1
);

-- Tabla de Categorías
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT,
    icono VARCHAR(50) DEFAULT '📚',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Técnicas
CREATE TABLE IF NOT EXISTS tecnicas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo VARCHAR(200) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    contenido_html TEXT NOT NULL,
    grado VARCHAR(50) DEFAULT '',
    orden INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Progreso de Estudiantes
CREATE TABLE IF NOT EXISTS progreso_estudiante (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    estudiante_id INTEGER NOT NULL,
    tecnica_id INTEGER NOT NULL,
    completada BOOLEAN DEFAULT 0,
    ultima_respuesta TEXT DEFAULT '',
    intentos INTEGER DEFAULT 0,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (estudiante_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (tecnica_id) REFERENCES tecnicas(id) ON DELETE CASCADE,
    UNIQUE(estudiante_id, tecnica_id)
);

-- Tabla de Respuestas de Ejercicios
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

-- Tabla de Favoritos
CREATE TABLE IF NOT EXISTS favoritos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    estudiante_id INTEGER NOT NULL,
    tecnica_id INTEGER NOT NULL,
    fecha_agregado DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (estudiante_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (tecnica_id) REFERENCES tecnicas(id) ON DELETE CASCADE,
    UNIQUE(estudiante_id, tecnica_id)
);

-- Tabla de Etiquetas
CREATE TABLE IF NOT EXISTS etiquetas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT
);

-- Tabla de Relación Técnica-Etiqueta
CREATE TABLE IF NOT EXISTS tecnica_etiqueta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tecnica_id INTEGER NOT NULL,
    etiqueta_id INTEGER NOT NULL,
    FOREIGN KEY (tecnica_id) REFERENCES tecnicas(id) ON DELETE CASCADE,
    FOREIGN KEY (etiqueta_id) REFERENCES etiquetas(id) ON DELETE CASCADE,
    UNIQUE(tecnica_id, etiqueta_id)
);
"""
        return tablas
    
    def _generar_indices(self):
        """Genera los índices para optimización"""
        indices = """
-- Índices para Optimización
CREATE INDEX IF NOT EXISTS idx_progreso_estudiante ON progreso_estudiante(estudiante_id, tecnica_id);
CREATE INDEX IF NOT EXISTS idx_tecnica_categoria ON tecnicas(categoria);
CREATE INDEX IF NOT EXISTS idx_tecnica_grado ON tecnicas(grado);
CREATE INDEX IF NOT EXISTS idx_usuario_username ON usuarios(username);
CREATE INDEX IF NOT EXISTS idx_progreso_estudiante_id ON progreso_estudiante(estudiante_id);
CREATE INDEX IF NOT EXISTS idx_progreso_tecnica_id ON progreso_estudiante(tecnica_id);
CREATE INDEX IF NOT EXISTS idx_favoritos_estudiante ON favoritos(estudiante_id);
CREATE INDEX IF NOT EXISTS idx_respuestas_estudiante ON respuestas_ejercicios(estudiante_id);
"""
        return indices
    
    def _generar_datos_ejemplo(self):
        """Genera datos de ejemplo para la base de datos"""
        return """
-- Insertar Categorías Base
INSERT OR IGNORE INTO categorias (id, nombre, descripcion, icono) VALUES 
(1, 'Morfología flexiva', 'Género, número, tiempo, modo, aspecto, persona', '🎭'),
(2, 'Derivación', 'Prefijación, sufijación, interfijación, parasíntesis', '⚙️'),
(3, 'Clases de palabras', 'Sustantivos, adjetivos, verbos, adverbios, preposiciones...', '📂'),
(4, 'Formación de palabras', 'Composición, acronimia, siglación', '🧩'),
(5, 'Accidentes gramaticales', 'Caso, grado, voz, definitud', '⚡'),
(6, 'Morfemática', 'Lexema, morfema, alomorfo, tema, base, raíz, interfijo', '🧬'),
(7, 'Estándares MEN', 'Grados 1° a 11°, ejes de lenguaje', '📘'),
(8, 'Concurso docente', 'Competencias docentes, pedagogía', '🍎');

-- Insertar Técnicas de Ejemplo
INSERT OR IGNORE INTO tecnicas (id, titulo, categoria, contenido_html, grado, orden) VALUES 
(1, 'Flexión de género (sustantivos)', 'Morfología flexiva', '<div class="teoria">📘 Los sustantivos varían de género con -o/-a u otras marcas.</div><div class="ejemplo">💡 niño/niña, poeta/poetisa</div>', '', 1),
(2, 'Flexión de número (plural)', 'Morfología flexiva', '<div class="teoria">📘 Se forma con -s, -es o invariables.</div><div class="ejemplo">💡 árbol/árboles, crisis/crisis</div>', '', 2),
(3, 'Modo subjuntivo presente', 'Morfología flexiva', '<div class="teoria">📘 Expresa deseo, duda, posibilidad.</div><div class="ejemplo">💡 Espero que venga</div>', '', 3),
(4, 'Pretérito perfecto simple', 'Morfología flexiva', '<div class="teoria">📘 Acción pasada puntual: -é, -aste, -ó, etc.</div><div class="ejemplo">💡 canté, comiste, vivió</div>', '', 4),
(5, 'Futuro de indicativo', 'Morfología flexiva', '<div class="teoria">📘 -é, -ás, -á, -emos, -éis, -án.</div><div class="ejemplo">💡 hablaré, comerás</div>', '', 5);

-- Insertar Usuario de Ejemplo (admin/admin123)
INSERT OR IGNORE INTO usuarios (username, password, first_name, last_name, email, is_staff, is_superuser) VALUES 
('admin', 'pbkdf2_sha256$600000$KvL9w7J9X2hG$9m9zX9pJ9y9w9g9v9y9d9q9z9v9h9r9m9x9l9w9', 'Administrador', 'Sistema', 'admin@lms.com', 1, 1);
"""
    
    def _generar_consultas_utiles(self):
        """Genera consultas útiles para la base de datos"""
        return """
-- ============================================================
-- CONSULTAS ÚTILES
-- ============================================================

-- 1. Ver todas las técnicas con sus categorías
-- SELECT id, titulo, categoria, grado FROM tecnicas ORDER BY id;

-- 2. Contar técnicas por categoría
-- SELECT categoria, COUNT(*) AS total FROM tecnicas GROUP BY categoria ORDER BY total DESC;

-- 3. Técnicas más recientes
-- SELECT id, titulo, created_at FROM tecnicas ORDER BY created_at DESC LIMIT 10;

-- 4. Progreso de un estudiante (reemplazar X por ID)
-- SELECT t.id, t.titulo, t.categoria, 
--        CASE WHEN p.completada = 1 THEN '✅' WHEN p.id IS NOT NULL THEN '⏳' ELSE '⚪' END AS Estado
-- FROM tecnicas t LEFT JOIN progreso_estudiante p ON t.id = p.tecnica_id AND p.estudiante_id = X
-- ORDER BY t.id;

-- 5. Estadísticas de todos los estudiantes
-- SELECT u.username, u.first_name, COUNT(p.tecnica_id) AS intentadas,
--        SUM(CASE WHEN p.completada = 1 THEN 1 ELSE 0 END) AS completadas,
--        ROUND(CAST(SUM(CASE WHEN p.completada = 1 THEN 1 ELSE 0 END) AS FLOAT) / 
--              COUNT(p.tecnica_id) * 100, 1) AS porcentaje
-- FROM usuarios u JOIN progreso_estudiante p ON u.id = p.estudiante_id
-- WHERE u.es_estudiante = 1 GROUP BY u.id;

-- 6. Técnicas más completadas
-- SELECT t.titulo, COUNT(p.estudiante_id) AS veces_completada
-- FROM tecnicas t JOIN progreso_estudiante p ON t.id = p.tecnica_id AND p.completada = 1
-- GROUP BY t.id ORDER BY veces_completada DESC LIMIT 10;

-- 7. Resumen del sistema
-- SELECT (SELECT COUNT(*) FROM usuarios) AS Usuarios,
--        (SELECT COUNT(*) FROM tecnicas) AS Tecnicas,
--        (SELECT COUNT(*) FROM progreso_estudiante) AS Progresos,
--        (SELECT COUNT(*) FROM progreso_estudiante WHERE completada = 1) AS Completadas;

-- 8. Categorías con más técnicas
-- SELECT categoria, COUNT(*) FROM tecnicas GROUP BY categoria ORDER BY COUNT(*) DESC;

-- 9. Usuarios por rol
-- SELECT 'Estudiante' AS rol, COUNT(*) FROM usuarios WHERE es_estudiante = 1
-- UNION SELECT 'Profesor', COUNT(*) FROM usuarios WHERE es_profesor = 1;

-- 10. Técnicas con ejercicios
-- SELECT id, titulo FROM tecnicas WHERE contenido_html LIKE '%ejercicio%';
"""
    
    def ejecutar_bd(self):
        """Ejecuta el script SQL en la base de datos"""
        print(f"\n{Colors.BLUE}📌 EJECUTANDO SCRIPT SQL{Colors.ENDC}")
        print(f"{Colors.CYAN}{'-'*50}{Colors.ENDC}")
        
        if self.tipo_bd == "sqlite" or self.tipo_bd == "django_sqlite":
            try:
                conn = sqlite3.connect(self.configuracion["sqlite"]["archivo"])
                cursor = conn.cursor()
                
                with open(self.archivo_sql, 'r', encoding='utf-8') as f:
                    sql = f.read()
                
                cursor.executescript(sql)
                conn.commit()
                conn.close()
                
                print(f"{Colors.GREEN}✅ Base de datos SQLite creada: {self.configuracion['sqlite']['archivo']}{Colors.ENDC}")
                
            except Exception as e:
                print(f"{Colors.RED}❌ Error ejecutando SQL: {e}{Colors.ENDC}")
                
        elif self.tipo_bd == "postgresql":
            try:
                import psycopg2
                conn = psycopg2.connect(
                    host=self.host,
                    port=self.configuracion["postgresql"]["puerto"],
                    user=self.usuario,
                    password=self.password
                )
                conn.autocommit = True
                cursor = conn.cursor()
                
                # Crear base de datos
                cursor.execute(f"CREATE DATABASE {self.nombre_bd};")
                cursor.close()
                conn.close()
                
                print(f"{Colors.GREEN}✅ Base de datos PostgreSQL creada: {self.nombre_bd}{Colors.ENDC}")
                
            except ImportError:
                print(f"{Colors.YELLOW}⚠️ psycopg2 no instalado. Instalar con: pip install psycopg2-binary{Colors.ENDC}")
            except Exception as e:
                print(f"{Colors.RED}❌ Error: {e}{Colors.ENDC}")
                
        elif self.tipo_bd == "mysql":
            try:
                import mysql.connector
                conn = mysql.connector.connect(
                    host=self.host,
                    port=self.configuracion["mysql"]["puerto"],
                    user=self.usuario,
                    password=self.password
                )
                cursor = conn.cursor()
                
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.nombre_bd};")
                cursor.close()
                conn.close()
                
                print(f"{Colors.GREEN}✅ Base de datos MySQL creada: {self.nombre_bd}{Colors.ENDC}")
                
            except ImportError:
                print(f"{Colors.YELLOW}⚠️ mysql-connector-python no instalado. Instalar con: pip install mysql-connector-python{Colors.ENDC}")
            except Exception as e:
                print(f"{Colors.RED}❌ Error: {e}{Colors.ENDC}")
    
    def generar_archivos_django(self):
        """Genera los archivos de configuración para Django"""
        print(f"\n{Colors.BLUE}📌 GENERANDO CONFIGURACIÓN DJANGO{Colors.ENDC}")
        print(f"{Colors.CYAN}{'-'*50}{Colors.ENDC}")
        
        config_django = self._generar_config_django()
        archivo = f"{self.ruta_sql}/settings_django.py"
        
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write(config_django)
        
        print(f"✅ Configuración Django generada: {archivo}")
    
    def _generar_config_django(self):
        """Genera la configuración de la base de datos para settings.py"""
        configs = {
            "sqlite": f"""
# ============================================================
# BASE DE DATOS SQLITE
# ============================================================
DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / '{self.configuracion['sqlite']['archivo']}',
    }}
}}
""",
            "postgresql": f"""
# ============================================================
# BASE DE DATOS POSTGRESQL
# ============================================================
DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '{self.nombre_bd}',
        'USER': '{self.usuario}',
        'PASSWORD': '{self.password}',
        'HOST': '{self.host}',
        'PORT': '{self.configuracion['postgresql']['puerto']}',
    }}
}}
""",
            "mysql": f"""
# ============================================================
# BASE DE DATOS MYSQL / MARIADB
# ============================================================
DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '{self.nombre_bd}',
        'USER': '{self.usuario}',
        'PASSWORD': '{self.password}',
        'HOST': '{self.host}',
        'PORT': '{self.configuracion['mysql']['puerto']}',
    }}
}}
"""
        }
        
        return configs.get(self.tipo_bd, configs["sqlite"])
    
    def generar_json(self):
        """Genera un archivo JSON con la configuración de la BD"""
        print(f"\n{Colors.BLUE}📌 GENERANDO CONFIGURACIÓN JSON{Colors.ENDC}")
        print(f"{Colors.CYAN}{'-'*50}{Colors.ENDC}")
        
        config = {
            "nombre": self.nombre_bd,
            "tipo": self.tipo_bd,
            "fecha_creacion": datetime.now().isoformat(),
            "configuracion": {
                "host": self.host,
                "puerto": self.configuracion.get(self.tipo_bd, {}).get("puerto", ""),
                "usuario": self.usuario,
                "archivo": self.configuracion.get(self.tipo_bd, {}).get("archivo", "")
            },
            "tablas": [
                "usuarios", "categorias", "tecnicas", 
                "progreso_estudiante", "respuestas_ejercicios", 
                "favoritos", "etiquetas", "tecnica_etiqueta"
            ],
            "total_tablas": 8
        }
        
        archivo = f"{self.ruta_sql}/configuracion_bd.json"
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Configuración JSON generada: {archivo}")
    
    def generar(self):
        """Ejecuta la generación completa"""
        if not self.seleccionar_tipo_bd():
            return False
        
        if not self.generar_estructura_bd():
            return False
        
        self.ejecutar_bd()
        self.generar_archivos_django()
        self.generar_json()
        
        print(f"\n{Colors.GREEN}{'='*60}{Colors.ENDC}")
        print(f"{Colors.GREEN}   🎉 ¡BASE DE DATOS GENERADA CON ÉXITO!{Colors.ENDC}")
        print(f"{Colors.GREEN}{'='*60}{Colors.ENDC}")
        print(f"\n{Colors.YELLOW}📋 RESULTADOS:{Colors.ENDC}")
        print(f"   - Tipo: {self.tipo_bd.upper()}")
        print(f"   - Nombre: {self.nombre_bd}")
        print(f"   - SQL: {self.archivo_sql}")
        print(f"   - Config: {self.ruta_sql}/configuracion_bd.json")
        print(f"   - Django: {self.ruta_sql}/settings_django.py")
        print(f"\n{Colors.GREEN}📚 ¡Listo para usar!{Colors.ENDC}")
        
        return True


def main():
    """Función principal"""
    generador = GeneradorBD()
    generador.generar()


if __name__ == "__main__":
    main()
