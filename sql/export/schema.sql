CREATE TABLE IF NOT EXISTS "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE IF NOT EXISTS "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);
CREATE UNIQUE INDEX "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" ("app_label", "model");
CREATE TABLE IF NOT EXISTS "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE UNIQUE INDEX "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" ("group_id", "permission_id");
CREATE INDEX "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" ("group_id");
CREATE INDEX "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" ("permission_id");
CREATE TABLE IF NOT EXISTS "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);
CREATE UNIQUE INDEX "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" ("content_type_id", "codename");
CREATE INDEX "auth_permission_content_type_id_2f476e4b" ON "auth_permission" ("content_type_id");
CREATE TABLE IF NOT EXISTS "auth_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(150) NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS "tecnicas" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "titulo" varchar(200) NOT NULL, "categoria" varchar(100) NOT NULL, "contenido_html" text NOT NULL, "grado" varchar(50) NULL, "orden" integer NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL);
CREATE TABLE IF NOT EXISTS "usuarios" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "first_name" varchar(150) NOT NULL, "last_name" varchar(150) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "es_profesor" bool NOT NULL, "es_estudiante" bool NOT NULL);
CREATE TABLE IF NOT EXISTS "usuarios_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "usuario_id" bigint NOT NULL REFERENCES "usuarios" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "usuarios_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "usuario_id" bigint NOT NULL REFERENCES "usuarios" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "progreso_estudiante" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "completada" bool NOT NULL, "ultima_respuesta" text NOT NULL, "intentos" integer NOT NULL, "fecha_actualizacion" datetime NOT NULL, "estudiante_id" bigint NOT NULL REFERENCES "usuarios" ("id") DEFERRABLE INITIALLY DEFERRED, "tecnica_id" bigint NOT NULL REFERENCES "tecnicas" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE UNIQUE INDEX "usuarios_groups_usuario_id_group_id_a66c5ef3_uniq" ON "usuarios_groups" ("usuario_id", "group_id");
CREATE INDEX "usuarios_groups_usuario_id_1132ca50" ON "usuarios_groups" ("usuario_id");
CREATE INDEX "usuarios_groups_group_id_18c61092" ON "usuarios_groups" ("group_id");
CREATE UNIQUE INDEX "usuarios_user_permissions_usuario_id_permission_id_474b33a5_uniq" ON "usuarios_user_permissions" ("usuario_id", "permission_id");
CREATE INDEX "usuarios_user_permissions_usuario_id_232fd58d" ON "usuarios_user_permissions" ("usuario_id");
CREATE INDEX "usuarios_user_permissions_permission_id_af615ca1" ON "usuarios_user_permissions" ("permission_id");
CREATE UNIQUE INDEX "progreso_estudiante_estudiante_id_tecnica_id_5d1a4f34_uniq" ON "progreso_estudiante" ("estudiante_id", "tecnica_id");
CREATE INDEX "progreso_estudiante_estudiante_id_d4fd0eec" ON "progreso_estudiante" ("estudiante_id");
CREATE INDEX "progreso_estudiante_tecnica_id_5a3f8e28" ON "progreso_estudiante" ("tecnica_id");
CREATE TABLE IF NOT EXISTS "django_admin_log" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "action_flag" smallint unsigned NOT NULL CHECK ("action_flag" >= 0), "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "usuarios" ("id") DEFERRABLE INITIALLY DEFERRED, "action_time" datetime NOT NULL);
CREATE INDEX "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" ("content_type_id");
CREATE INDEX "django_admin_log_user_id_c564eba6" ON "django_admin_log" ("user_id");
CREATE TABLE IF NOT EXISTS "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);
CREATE INDEX "django_session_expire_date_a5c62663" ON "django_session" ("expire_date");
CREATE TABLE respuestas_ejercicios (
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
CREATE TABLE categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT,
    icono VARCHAR(50)
);
CREATE INDEX idx_progreso_estudiante ON progreso_estudiante(estudiante_id, tecnica_id);
CREATE INDEX idx_tecnica_categoria ON tecnicas(categoria);
CREATE INDEX idx_tecnica_grado ON tecnicas(grado);
