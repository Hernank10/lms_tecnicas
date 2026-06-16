#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GENERADOR DE HTMLS EDUCATIVOS
Crea archivos HTML con técnicas de aprendizaje de cualquier categoría
"""

import os
import re
import json
import random
from datetime import datetime

class GeneradorHTMLEducativo:
    """Clase para generar archivos HTML con técnicas educativas"""
    
    def __init__(self, titulo="Técnicas Educativas", autor="LMS Generator"):
        self.titulo = titulo
        self.autor = autor
        self.tecnicas = []
        self.categorias = {}
        self.html_template = ""
        self.total_tecnicas = 0
        
    def agregar_tecnica(self, id, nombre, categoria, teoria, ejemplo, ejercicio, respuesta, grado=""):
        """Agrega una técnica al generador"""
        tecnica = {
            'id': id,
            'nombre': nombre,
            'categoria': categoria,
            'teoria': teoria,
            'ejemplo': ejemplo,
            'ejercicio': ejercicio,
            'respuesta': respuesta,
            'grado': grado
        }
        self.tecnicas.append(tecnica)
        
        if categoria not in self.categorias:
            self.categorias[categoria] = 0
        self.categorias[categoria] += 1
        self.total_tecnicas = len(self.tecnicas)
        
        return self
    
    def agregar_tecnicas_desde_lista(self, lista_tecnicas):
        for t in lista_tecnicas:
            self.agregar_tecnica(**t)
        return self
    
    def generar_html(self, nombre_archivo=None):
        if not nombre_archivo:
            nombre_archivo = f"tecnicas_{len(self.tecnicas)}_{datetime.now().strftime('%Y%m%d')}.html"
        
        html = self._generar_header()
        html += self._generar_body()
        html += self._generar_footer()
        
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ HTML generado: {nombre_archivo}")
        print(f"   Técnicas: {len(self.tecnicas)}")
        print(f"   Categorías: {len(self.categorias)}")
        return nombre_archivo
    
    def _generar_header(self):
        return f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.titulo} - {len(self.tecnicas)} técnicas</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            background: linear-gradient(145deg, #f0f4fa 0%, #e2e9f2 100%);
            font-family: 'Segoe UI', Roboto, sans-serif;
            padding: 2rem 1.5rem;
            color: #1a2e40;
        }}
        .container {{ max-width: 1500px; margin: 0 auto; }}
        .hero {{
            text-align: center;
            margin-bottom: 2rem;
            border-bottom: 3px solid #0f6b3a;
            width: 100%;
        }}
        .hero h1 {{
            font-size: 2.5rem;
            background: linear-gradient(135deg, #0f6b3a, #2a9d6e);
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
            font-weight: 800;
        }}
        .hero p {{ font-size: 1.1rem; color: #2d5a3b; margin-top: 0.5rem; font-style: italic; }}
        .stats {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            background: white;
            padding: 0.8rem 1.5rem;
            border-radius: 60px;
            margin: 1.5rem 0 2rem;
            gap: 1rem;
            box-shadow: 0 5px 12px rgba(0,0,0,0.05);
        }}
        .badge {{
            background: #0f6b3a;
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 40px;
            font-weight: bold;
            font-size: 0.9rem;
        }}
        .progress-area {{
            display: flex;
            gap: 1.5rem;
            align-items: baseline;
            font-weight: 500;
        }}
        .progress-bar-container {{
            width: 180px;
            height: 8px;
            background-color: #cfe3d9;
            border-radius: 10px;
            overflow: hidden;
        }}
        .progress-fill {{ width: 0%; height: 100%; background-color: #0f6b3a; transition: width 0.3s; }}
        .filter-bar {{
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin-bottom: 2rem;
            justify-content: center;
        }}
        .filter-bar input, .filter-bar select {{
            padding: 12px 20px;
            border: none;
            border-radius: 50px;
            background: white;
            font-size: 1rem;
            outline: none;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }}
        .filter-bar input {{ flex: 2; min-width: 220px; }}
        .cards-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); gap: 1.8rem; }}
        .card {{
            background: white;
            border-radius: 2rem;
            overflow: hidden;
            box-shadow: 0 12px 24px -12px rgba(0,0,0,0.2);
            transition: 0.2s;
            border: 1px solid #cde0d6;
            display: flex;
            flex-direction: column;
        }}
        .card:hover {{ transform: translateY(-5px); }}
        .card-header {{ background: #e8f3ed; padding: 1rem 1.5rem; border-bottom: 1px solid #cde0d6; }}
        .card-header h3 {{ font-size: 1.25rem; font-weight: 700; color: #1a5a3a; }}
        .category-tag {{
            display: inline-block;
            background: #cfe3d9;
            padding: 0.2rem 0.8rem;
            border-radius: 40px;
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            margin-top: 0.5rem;
            color: #1a5a3a;
        }}
        .grade-tag {{
            display: inline-block;
            background: #0f6b3a;
            color: white;
            padding: 0.2rem 0.8rem;
            border-radius: 40px;
            font-size: 0.65rem;
            font-weight: 600;
            margin-top: 0.5rem;
            margin-left: 0.5rem;
        }}
        .card-body {{ padding: 1.2rem 1.5rem; flex-grow: 1; }}
        .teoria {{
            background: #f4faf7;
            padding: 0.7rem;
            border-radius: 20px;
            margin-bottom: 1rem;
            font-size: 0.9rem;
            border-left: 5px solid #0f6b3a;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
        }}
        .ejemplo {{
            background: #edf6f1;
            padding: 0.5rem 0.8rem;
            border-radius: 16px;
            margin: 0.7rem 0;
            font-family: monospace;
            color: #1a5a3a;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
        }}
        .btn-speak {{
            background: #0f6b3a;
            border: none;
            color: white;
            border-radius: 50px;
            padding: 4px 12px;
            font-size: 0.7rem;
            cursor: pointer;
        }}
        .btn-speak:hover {{ background: #1a8a4a; }}
        .ejercicio-area {{ background: #f8fbf9; padding: 0.7rem; border-radius: 20px; margin: 0.8rem 0; }}
        .ejercicio-text {{ font-style: italic; margin-bottom: 0.6rem; font-weight: 500; }}
        .input-group {{ display: flex; gap: 0.5rem; flex-wrap: wrap; margin: 0.5rem 0; }}
        .input-group input {{ flex: 2; padding: 8px 12px; border: 1px solid #cde0d6; border-radius: 30px; font-size: 0.85rem; outline: none; }}
        .check-btn {{ background: #0f6b3a; color: white; border: none; padding: 8px 16px; border-radius: 30px; cursor: pointer; font-weight: bold; }}
        .check-btn:hover {{ background: #1a8a4a; }}
        .feedback {{ font-size: 0.8rem; margin-top: 5px; font-weight: 500; }}
        .feedback.correct {{ color: #0f6b3a; }}
        .feedback.incorrect {{ color: #c23b22; }}
        .hidden-answer {{
            display: none;
            background: #e0f0e6;
            border-radius: 20px;
            padding: 0.6rem 1rem;
            margin-top: 0.5rem;
            border-left: 4px solid #0f6b3a;
            font-size: 0.85rem;
        }}
        .answer-hint {{
            background: #cfe3ed;
            border-radius: 24px;
            padding: 0.6rem 1rem;
            margin-top: 0.6rem;
            font-size: 0.85rem;
            cursor: pointer;
            transition: 0.1s;
            text-align: center;
            font-weight: 500;
            color: #1e4155;
        }}
        .answer-hint:hover {{ background: #b2cfdf; }}
        .reset-card-btn {{
            margin-top: 8px;
            background: none;
            border: none;
            color: #5c8a6e;
            cursor: pointer;
            font-size: 0.7rem;
            text-decoration: underline;
        }}
        .footer-note {{ margin-top: 3rem; text-align: center; font-size: 0.85rem; color: #5c8a6e; border-top: 1px solid #cde0d6; padding-top: 2rem; }}
        .status-icon {{ font-size: 0.8rem; display: inline-block; margin-left: 8px; }}
        @media (max-width: 700px) {{
            .stats {{ flex-direction: column; align-items: center; }}
            .cards-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
<div class="container">
    <div class="hero">
        <h1>{self.titulo}</h1>
        <p>Generado por {self.autor} · {len(self.tecnicas)} técnicas educativas</p>
    </div>
    <div class="stats">
        <span>📚 Inventario: <strong>{len(self.tecnicas)}</strong> entradas</span>
        <div class="progress-area">
            <span>🏆 Progreso:</span>
            <div class="progress-bar-container"><div class="progress-fill" id="globalProgressFill"></div></div>
            <span id="progressPercent">0%</span>
        </div>
        <span class="badge">✍️ teoría + ejemplo + ejercicio interactivo</span>
    </div>
    <div class="filter-bar">
        <input type="text" id="searchInput" placeholder="🔍 Buscar...">
        <select id="categorySelect">
            <option value="all">📌 Todas las categorías</option>'''
    
    def _generar_body(self):
        body = ''
        categorias_ordenadas = sorted(self.categorias.keys())
        for cat in categorias_ordenadas:
            body += f'\n            <option value="{cat}">{cat}</option>'
        
        body += '''
        </select>
    </div>
    <div id="cardsContainer" class="cards-grid">'''
        
        for t in self.tecnicas:
            body += self._generar_card(t)
        
        return body
    
    def _generar_card(self, t):
        id_html = t['id']
        nombre = t['nombre']
        categoria = t['categoria']
        teoria = t['teoria'].replace('"', '&quot;')
        ejemplo = t['ejemplo'].replace('"', '&quot;')
        ejercicio = t['ejercicio'].replace('"', '&quot;')
        respuesta = t['respuesta'].replace('"', '&quot;')
        grado = t.get('grado', '')
        
        grado_html = f'<span class="grade-tag">📘 {grado}</span>' if grado else ''
        
        return f'''
        <div class="card" data-id="{id_html}">
            <div class="card-header">
                <h3>#{id_html} · {nombre} <span id="status-{id_html}" class="status-icon"></span></h3>
                <span class="category-tag">{categoria}</span>
                {grado_html}
            </div>
            <div class="card-body">
                <div class="teoria">
                    <span>📘 {teoria}</span>
                    <button class="btn-speak" data-text="{teoria}">🔊 Leer</button>
                </div>
                <div class="ejemplo">
                    <span>💡 {ejemplo}</span>
                    <button class="btn-speak-ejemplo btn-speak" data-text="{ejemplo}">🔊 Leer ejemplo</button>
                </div>
                <div class="ejercicio-area">
                    <div class="ejercicio-text">✏️ Ejercicio: {ejercicio}</div>
                    <div class="input-group">
                        <input type="text" id="input-{id_html}" placeholder="Escribe tu respuesta...">
                        <button class="check-btn" data-id="{id_html}">Comprobar</button>
                    </div>
                    <div id="feedback-{id_html}" class="feedback"></div>
                    <div class="answer-hint" data-id="{id_html}">🔎 Mostrar respuesta sugerida</div>
                    <div id="answer-{id_html}" class="hidden-answer">✅ {respuesta}</div>
                    <button class="reset-card-btn" data-id="{id_html}">⟳ Reiniciar ejercicio</button>
                </div>
            </div>
        </div>'''
    
    def _generar_footer(self):
        return f'''
    </div>
    <div class="footer-note">✅ Generado automáticamente · {len(self.tecnicas)} técnicas con teoría, ejemplo y ejercicio interactivo.</div>
</div>
<script>
// ============================================================
// PROGRESO Y FUNCIONES INTERACTIVAS
// ============================================================
let userProgress = JSON.parse(localStorage.getItem('techProgress')) || {{}};

function updateGlobalProgress() {{
    let completed = Object.values(userProgress).filter(v=>v===true).length;
    let total = {len(self.tecnicas)};
    let percent = Math.round((completed/total)*100);
    let fill = document.getElementById('globalProgressFill');
    let percentSpan = document.getElementById('progressPercent');
    if(fill) fill.style.width = percent+'%';
    if(percentSpan) percentSpan.innerText = percent+'%';
}}

function setStatus(id, ok){{
    let span = document.getElementById(`status-${{id}}`);
    if(span) span.innerHTML = ok ? ' ✅' : '';
    userProgress[id] = ok;
    localStorage.setItem('techProgress', JSON.stringify(userProgress));
    updateGlobalProgress();
}}

function checkAnswer(id, userAns, correctAns, inputEl, fbEl){{
    let normUser = userAns.trim().toLowerCase().replace(/[¿¡]/g,'');
    let normCorr = correctAns.trim().toLowerCase().replace(/[¿¡]/g,'');
    let ok = normUser === normCorr;
    fbEl.innerHTML = ok ? '✓ ¡Correcto!' : `✗ Incorrecto. Respuesta: "${{correctAns}}"`;
    fbEl.className = `feedback ${{ok ? 'correct' : 'incorrect'}}`;
    inputEl.disabled = true;
    inputEl.style.backgroundColor = '#f0f0f0';
    setStatus(id, ok);
}}

function resetCard(id, inputEl, fbEl){{
    inputEl.disabled = false;
    inputEl.value = '';
    inputEl.style.backgroundColor = 'white';
    fbEl.innerHTML = '';
    fbEl.className = 'feedback';
    setStatus(id, false);
}}

function speakText(text){{
    if('speechSynthesis' in window){{
        speechSynthesis.cancel();
        let utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'es-ES';
        utterance.rate = 0.9;
        speechSynthesis.speak(utterance);
    }} else alert("Voz no soportada.");
}}

function renderCards(){{
    let searchTerm = document.getElementById('searchInput').value.toLowerCase();
    let cat = document.getElementById('categorySelect').value;
    let cards = document.querySelectorAll('.card');
    cards.forEach(card => {{
        let title = card.querySelector('h3')?.innerText?.toLowerCase() || '';
        let category = card.querySelector('.category-tag')?.innerText?.toLowerCase() || '';
        let theory = card.querySelector('.teoria')?.innerText?.toLowerCase() || '';
        let match = (cat === 'all' || category === cat) && 
                   (title.includes(searchTerm) || category.includes(searchTerm) || theory.includes(searchTerm));
        card.style.display = match ? 'flex' : 'none';
    }});
}}

// Event listeners
document.getElementById('searchInput').addEventListener('input', renderCards);
document.getElementById('categorySelect').addEventListener('change', renderCards);
updateGlobalProgress();

// Configurar todas las tarjetas
document.querySelectorAll('.card').forEach(card => {{
    const id = card.getAttribute('data-id');
    const answerDiv = card.querySelector(`#answer-${{id}}`);
    const answer = answerDiv?.innerText || '';
    const hintBtn = card.querySelector(`.answer-hint[data-id="${{id}}"]`);
    const resetBtn = card.querySelector(`.reset-card-btn[data-id="${{id}}"]`);
    const inputEl = card.querySelector(`#input-${{id}}`);
    const checkBtn = card.querySelector(`.check-btn[data-id="${{id}}"]`);
    const fbEl = card.querySelector(`#feedback-${{id}}`);
    const speakBtns = card.querySelectorAll('.btn-speak');
    
    // Botones de voz
    speakBtns.forEach(btn => {{
        btn.addEventListener('click', () => {{
            const text = btn.getAttribute('data-text');
            if(text) speakText(text);
        }});
    }});
    
    // Mostrar respuesta
    if(hintBtn) {{
        hintBtn.addEventListener('click', () => {{
            if(answerDiv) {{
                if(answerDiv.style.display === 'none' || answerDiv.style.display === '') {{
                    answerDiv.style.display = 'block';
                    hintBtn.textContent = '🙈 Ocultar respuesta';
                }} else {{
                    answerDiv.style.display = 'none';
                    hintBtn.textContent = '🔎 Mostrar respuesta sugerida';
                }}
            }}
        }});
    }}
    
    // Comprobar ejercicio
    if(checkBtn && inputEl && fbEl) {{
        checkBtn.addEventListener('click', () => {{
            if(!inputEl.disabled) {{
                checkAnswer(id, inputEl.value, answer, inputEl, fbEl);
                checkBtn.disabled = true;
            }}
        }});
        // Enter key
        inputEl.addEventListener('keypress', (e) => {{
            if(e.key === 'Enter' && !inputEl.disabled) {{
                checkBtn.click();
            }}
        }});
    }}
    
    // Reiniciar ejercicio
    if(resetBtn && inputEl && fbEl) {{
        resetBtn.addEventListener('click', () => {{
            resetCard(id, inputEl, fbEl);
            if(checkBtn) checkBtn.disabled = false;
        }});
    }}
    
    // Cargar estado previo
    if(userProgress[id] && inputEl && checkBtn) {{
        inputEl.disabled = true;
        inputEl.style.backgroundColor = '#f0f0f0';
        checkBtn.disabled = true;
    }}
}});

console.log('✅ HTML educativo cargado correctamente');
</script>
</body>
</html>'''
        return footer


def generar_tecnicas_ejemplo():
    """Genera 100 técnicas de ejemplo"""
    tecnicas = []
    
    # Técnicas de morfología
    morfologia = [
        ("Flexión de género", "Los sustantivos varían de género con -o/-a", "niño/niña, poeta/poetisa", "Femenino de 'actor'", "actriz"),
        ("Flexión de número", "Se forma con -s, -es o invariables", "árbol/árboles, crisis/crisis", "Plural de 'jabalí'", "jabalíes"),
        ("Modo subjuntivo", "Expresa deseo, duda, posibilidad", "Espero que venga", "Conjuga 'temer' 3ª singular", "tema"),
    ]
    
    for i, (nombre, teoria, ejemplo, ejercicio, respuesta) in enumerate(morfologia, 1):
        tecnicas.append({
            'id': i, 'nombre': nombre, 'categoria': "Morfología flexiva",
            'teoria': teoria, 'ejemplo': ejemplo, 'ejercicio': ejercicio,
            'respuesta': respuesta, 'grado': ""
        })
    
    # Técnicas de gramática
    gramatica = [
        ("Oración simple", "Sujeto + predicado", "El niño juega", "Sujeto de 'Cantan los pájaros'", "los pájaros"),
        ("Complemento directo", "Recibe la acción", "Vi a Juan → Lo vi", "Reemplaza CD: 'Compré manzanas'", "Las compré"),
    ]
    
    for i, (nombre, teoria, ejemplo, ejercicio, respuesta) in enumerate(gramatica, len(tecnicas)+1):
        tecnicas.append({
            'id': i, 'nombre': nombre, 'categoria': "Gramática",
            'teoria': teoria, 'ejemplo': ejemplo, 'ejercicio': ejercicio,
            'respuesta': respuesta, 'grado': ""
        })
    
    # Completar hasta 100
    while len(tecnicas) < 100:
        idx = len(tecnicas) + 1
        tecnicas.append({
            'id': idx,
            'nombre': f"Técnica educativa {idx}",
            'categoria': "Educación general",
            'teoria': f"Teoría de la técnica {idx}: concepto fundamental",
            'ejemplo': f"Ejemplo de la técnica {idx}: aplicación práctica",
            'ejercicio': f"Describe la técnica {idx}",
            'respuesta': f"Respuesta sugerida para la técnica {idx}",
            'grado': ""
        })
    
    return tecnicas


def main():
    print("="*60)
    print("   🚀 GENERADOR DE HTMLS EDUCATIVOS")
    print("="*60)
    
    generador = GeneradorHTMLEducativo(titulo="100 Técnicas Educativas", autor="Hernank10")
    tecnicas = generar_tecnicas_ejemplo()
    generador.agregar_tecnicas_desde_lista(tecnicas)
    generador.generar_html()
    
    print("\n✅ ¡HTML generado exitosamente!")

if __name__ == "__main__":
    main()
