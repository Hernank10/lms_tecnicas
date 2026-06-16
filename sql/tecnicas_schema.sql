CREATE TABLE IF NOT EXISTS "tecnicas" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "titulo" varchar(200) NOT NULL, "categoria" varchar(100) NOT NULL, "contenido_html" text NOT NULL, "grado" varchar(50) NULL, "orden" integer NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL);
CREATE INDEX idx_tecnica_categoria ON tecnicas(categoria);
CREATE INDEX idx_tecnica_grado ON tecnicas(grado);
