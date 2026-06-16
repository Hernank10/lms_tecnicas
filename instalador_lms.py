#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
INSTALADOR UNIVERSAL LMS - Django
Instala todo el proyecto LMS en cualquier dispositivo
Sistema operativo: Linux, macOS, Windows
"""

import os
import sys
import platform
import subprocess
import shutil
import json
import urllib.request
import zipfile
import tempfile
from pathlib import Path
import time
import getpass

# Colores para terminal
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

class InstaladorLMS:
    """Instalador universal del proyecto LMS"""
    
    def __init__(self):
        self.sistema = platform.system()
        self.arquitectura = platform.machine()
        self.python_version = sys.version_info
        self.ruta_base = Path.cwd()
        self.nombre_proyecto = "lms_tecnicas"
        self.venv_path = None
        self.python_cmd = "python3"
        self.pip_cmd = "pip3"
        
        # Configurar comandos según sistema operativo
        self._configurar_comandos()
        
        print(f"{Colors.CYAN}{'='*60}{Colors.ENDC}")
        print(f"{Colors.GREEN}   🚀 INSTALADOR UNIVERSAL LMS - DJANGO{Colors.ENDC}")
        print(f"{Colors.CYAN}{'='*60}{Colors.ENDC}")
        print(f"\n{Colors.YELLOW}📋 Información del sistema:{Colors.ENDC}")
        print(f"   - Sistema operativo: {self.sistema}")
        print(f"   - Arquitectura: {self.arquitectura}")
        print(f"   - Python: {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}")
        print(f"   - Carpeta base: {self.ruta_base}")
        print("")
    
    def _configurar_comandos(self):
        """Configura los comandos según el sistema operativo"""
        if self.sistema == "Windows":
            self.python_cmd = "python"
            self.pip_cmd = "pip"
            self.venv_cmd = "venv"
            self.activate_cmd = "Scripts\\activate"
            self.cmd_separator = "&"
        else:
            self.python_cmd = "python3"
            self.pip_cmd = "pip3"
            self.venv_cmd = "venv"
            self.activate_cmd = "source venv/bin/activate"
            self.cmd_separator = "&&"
    
    def imprimir_paso(self, paso, descripcion):
        """Imprime un paso con formato"""
        print(f"\n{Colors.BLUE}📌 PASO {paso}: {descripcion}{Colors.ENDC}")
        print(f"{Colors.CYAN}{'-'*50}{Colors.ENDC}")
    
    def ejecutar_comando(self, comando, descripcion=None):
        """Ejecuta un comando del sistema"""
        if descripcion:
            print(f"   🔧 {descripcion}...")
        
        try:
            if isinstance(comando, str):
                # Para comandos con pipes o múltiples comandos
                if "|" in comando or "&&" in comando or ";" in comando:
                    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
                else:
                    resultado = subprocess.run(comando.split(), capture_output=True, text=True)
            else:
                resultado = subprocess.run(comando, capture_output=True, text=True)
            
            if resultado.returncode != 0:
                if resultado.stderr:
                    print(f"{Colors.RED}   ❌ Error: {resultado.stderr.strip()}{Colors.ENDC}")
                return False
            
            if resultado.stdout:
                print(f"   ✅ {resultado.stdout.strip()[:200]}...")
            return True
            
        except Exception as e:
            print(f"{Colors.RED}   ❌ Error: {e}{Colors.ENDC}")
            return False
    
    def verificar_requisitos(self):
        """Verifica los requisitos del sistema"""
        self.imprimir_paso("1/8", "Verificando requisitos del sistema")
        
        # Verificar Python
        if self.python_version.major < 3:
            print(f"{Colors.RED}❌ Se requiere Python 3.12 o superior{Colors.ENDC}")
            return False
        print(f"   ✅ Python {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro} detectado")
        
        # Verificar pip
        try:
            resultado = subprocess.run([self.pip_cmd, "--version"], capture_output=True, text=True)
            if resultado.returncode == 0:
                print(f"   ✅ Pip detectado")
            else:
                print(f"{Colors.YELLOW}⚠️ Pip no encontrado, se intentará instalar{Colors.ENDC}")
        except:
            print(f"{Colors.YELLOW}⚠️ Pip no encontrado{Colors.ENDC}")
        
        # Verificar git
        try:
            resultado = subprocess.run(["git", "--version"], capture_output=True, text=True)
            if resultado.returncode == 0:
                print(f"   ✅ Git detectado")
            else:
                print(f"{Colors.YELLOW}⚠️ Git no encontrado (opcional){Colors.ENDC}")
        except:
            print(f"{Colors.YELLOW}⚠️ Git no encontrado (opcional){Colors.ENDC}")
        
        # Verificar espacio en disco
        import shutil
        espacio = shutil.disk_usage(self.ruta_base)
        espacio_gb = espacio.free / (1024**3)
        if espacio_gb < 0.5:
            print(f"{Colors.YELLOW}⚠️ Espacio en disco bajo: {espacio_gb:.1f} GB disponibles{Colors.ENDC}")
        else:
            print(f"   ✅ Espacio en disco: {espacio_gb:.1f} GB disponibles")
        
        return True
    
    def crear_estructura(self):
        """Crea la estructura de carpetas del proyecto"""
        self.imprimir_paso("2/8", "Creando estructura de carpetas")
        
        # Crear carpetas
        carpetas = [
            self.nombre_proyecto,
            f"{self.nombre_proyecto}/tecnicas",
            f"{self.nombre_proyecto}/tecnicas/templates",
            f"{self.nombre_proyecto}/tecnicas/static",
            f"{self.nombre_proyecto}/tecnicas/migrations",
            f"{self.nombre_proyecto}/sql",
            f"{self.nombre_proyecto}/sql/backups",
            f"{self.nombre_proyecto}/sql/export",
            f"{self.nombre_proyecto}/sql/reports",
        ]
        
        for carpeta in carpetas:
            Path(carpeta).mkdir(parents=True, exist_ok=True)
            print(f"   ✅ Creada: {carpeta}")
        
        return True
    
    def crear_archivos_base(self):
        """Crea los archivos base del proyecto"""
        self.imprimir_paso("3/8", "Creando archivos base")
        
        archivos = {
            f"{self.nombre_proyecto}/requirements.txt": """Django>=4.2
beautifulsoup4>=4.12
requests>=2.28
""",
            f"{self.nombre_proyecto}/.gitignore": """venv/
__pycache__/
*.pyc
*.sqlite3
*.db
*.log
.DS_Store
*.pyc
migrations/
*.sqlite3-journal
""",
            f"{self.nombre_proyecto}/README.md": """# 📚 LMS Técnicas - Sistema de Aprendizaje Interactivo

Sistema LMS con técnicas educativas para estudiantes.

## 🚀 Instalación Rápida

```bash
python instalador_lms.py
