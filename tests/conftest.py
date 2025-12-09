import sys
import os

# Récupère le chemin du dossier racine du projet
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Ajoute ce chemin à PYTHONPATH
sys.path.insert(0, ROOT_DIR)

