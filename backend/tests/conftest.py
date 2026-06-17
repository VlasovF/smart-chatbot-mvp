import sys
from pathlib import Path

# Добавляем корневую папку backend в PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

print(f"PYTHONPATH updated: {sys.path[0]}")
