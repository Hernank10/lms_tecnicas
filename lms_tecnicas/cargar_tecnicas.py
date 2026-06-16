#!/usr/bin/env python
import os
import re
import sys
import glob
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_tecnicas.settings')
django.setup()

from bs4 import BeautifulSoup
from tecnicas.models import Tecnica

print("🚀 INICIANDO CARGA DE TÉCNICAS")
print("="*50)

def extraer_tecnicas_desde_html(html_path):
    """Extrae técnicas de un archivo HTML"""
    tecnicas = []
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
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
                
                tecnicas.append({
                    'id': tecnica_id,
                    'titulo': nombre,
                    'categoria': categoria,
                    'contenido_html': contenido_html,
                    'grado': grado
                })
                print(f"    ✅ Extraída: #{tecnica_id} - {nombre}")
            except Exception as e:
                print(f"    ⚠️ Error en tarjeta: {e}")
                continue
    except Exception as e:
        print(f"  ❌ Error abriendo archivo: {e}")
    return tecnicas

# Buscar archivos HTML
html_files = glob.glob("*.html")
print(f"\n🔍 Archivos HTML encontrados: {len(html_files)}")

if not html_files:
    print("⚠️ No se encontraron archivos HTML en la carpeta actual.")
    print(f"📂 Carpeta actual: {os.getcwd()}")
    sys.exit(0)

total_tecnicas = 0
for html_file in html_files:
    print(f"\n📄 Procesando: {html_file}")
    tecnicas = extraer_tecnicas_desde_html(html_file)
    
    if not tecnicas:
        print(f"  ⚠️ No se extrajeron técnicas de {html_file}")
        continue
    
    for t in tecnicas:
        # Usar update_or_create con valores por defecto
        obj, creada = Tecnica.objects.update_or_create(
            id=t['id'],
            defaults={
                'titulo': t['titulo'],
                'categoria': t['categoria'],
                'contenido_html': t['contenido_html'],
                'grado': t['grado'],
                'orden': t['id']
            }
        )
        total_tecnicas += 1
        if creada:
            print(f"    ✅ Creada: #{t['id']} - {t['titulo']}")
        else:
            print(f"    🔄 Actualizada: #{t['id']} - {t['titulo']}")
    
    print(f"  ✅ {len(tecnicas)} técnicas procesadas desde {html_file}")

print(f"\n" + "="*50)
print(f"✅ CARGA COMPLETADA")
print(f"   - Técnicas procesadas: {total_tecnicas}")
print(f"   - Total en base de datos: {Tecnica.objects.count()}")
print("="*50)
