#!/usr/bin/env python
import os
import re
import sys
import glob
import sqlite3
from bs4 import BeautifulSoup

print("🚀 INICIANDO CARGA DE TÉCNICAS")
print("="*50)

# Conectar a la BD
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

def extraer_tecnicas_desde_html(html_path):
    """Extrae técnicas de un archivo HTML"""
    tecnicas = []
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
        
        cards = soup.find_all('div', class_='card')
        print(f"  📄 Encontradas {len(cards)} tarjetas en {html_path}")
        
        for card in cards:
            try:
                header = card.find('div', class_='card-header')
                if not header: continue
                h3 = header.find('h3')
                if not h3: continue
                text = h3.get_text(strip=True)
                match = re.match(r'#(\d+)\s*·\s*(.*)', text)
                if not match: continue
                
                tecnica_id = int(match.group(1))
                nombre = match.group(2).strip()
                
                cat_tag = header.find('span', class_='category-tag')
                categoria = cat_tag.get_text(strip=True) if cat_tag else "Sin categoría"
                
                grado = ""
                grade_tag = header.find('span', class_='grade-tag')
                if grade_tag:
                    grado = grade_tag.get_text(strip=True)
                
                teoria_div = card.find('div', class_='teoria')
                teoria = teoria_div.get_text(separator=' ', strip=True) if teoria_div else ""
                teoria = re.sub(r'Leer teoría', '', teoria)
                teoria = re.sub(r'🔊', '', teoria).strip()
                
                ejemplo_div = card.find('div', class_='ejemplo')
                ejemplo = ejemplo_div.get_text(separator=' ', strip=True) if ejemplo_div else ""
                ejemplo = re.sub(r'Leer ejemplo', '', ejemplo)
                ejemplo = re.sub(r'💡', '', ejemplo).strip()
                
                contenido_html = f"""
                <div class="teoria">{teoria}</div>
                <div class="ejemplo"><strong>Ejemplo:</strong> {ejemplo}</div>
                """
                
                tecnicas.append((tecnica_id, nombre, categoria, contenido_html, grado))
                print(f"    ✅ Extraída: #{tecnica_id} - {nombre}")
                
            except Exception as e:
                print(f"    ⚠️ Error en tarjeta: {e}")
                continue
    except Exception as e:
        print(f"  ❌ Error abriendo {html_path}: {e}")
    
    return tecnicas

# Buscar todos los HTMLs
html_files = glob.glob("*.html")
html_files.extend(glob.glob("*.htm"))

print(f"\n🔍 Buscando archivos HTML...")
print(f"📁 Archivos encontrados: {len(html_files)}")

if not html_files:
    print("\n⚠️ No se encontraron archivos HTML en la carpeta actual.")
    print(f"📂 Carpeta actual: {os.getcwd()}")
    sys.exit(0)

total_tecnicas = 0
archivos_procesados = 0

for html_file in html_files:
    print(f"\n📄 Procesando: {html_file}")
    tecnicas = extraer_tecnicas_desde_html(html_file)
    
    if not tecnicas:
        print(f"  ⚠️ No se extrajeron técnicas de {html_file}")
        continue
    
    for t in tecnicas:
        cursor.execute("""
            INSERT OR REPLACE INTO tecnicas 
            (id, titulo, categoria, contenido_html, grado, orden)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (t[0], t[1], t[2], t[3], t[4], t[0]))
        total_tecnicas += 1
    
    archivos_procesados += 1
    print(f"  ✅ {len(tecnicas)} técnicas cargadas desde {html_file}")

conn.commit()
conn.close()

print(f"\n" + "="*50)
print(f"✅ CARGA COMPLETADA")
print(f"   - Archivos procesados: {archivos_procesados}")
print(f"   - Técnicas cargadas: {total_tecnicas}")
print("="*50)
