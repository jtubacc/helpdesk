# Entorno y reproducción

Entorno observado para la revisión: macOS Darwin arm64, Git 2.54.0, uv 0.12.9, Python 3.14.7, pytest 9.1.1 y Tk 9.0. El manifiesto del proyecto requiere Python >=3.11. Las versiones son observadas en ese entorno; no se afirma compatibilidad con todos los sistemas.

Desde el directorio raíz de una copia limpia, con Python y Tkinter disponibles:

```sh
uv sync --locked
PYTHONDONTWRITEBYTECODE=1 uv run pytest -q -p no:cacheprovider
uv run python main.py
```

`uv sync --locked` y la ejecución de 21 pruebas terminaron con código 0 en una copia limpia del commit e5d8c02. En la rama integrada también se ejecutaron ambos guiones Tk: `PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 uv run python scripts/verificar_semana7.py` y `PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 uv run python scripts/verificar_semanas8_9.py`; ambos terminaron con código 0. Los diálogos se interceptaron y falta inspección visual. La app usa listas en memoria: cerrar el proceso descarta los datos. Esta fase no necesita base de datos ni variables secretas.
