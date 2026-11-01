# Pruebas y evidencias

En la rama de integración se ejecutó:

```sh
PYTHONDONTWRITEBYTECODE=1 uv run pytest -q -p no:cacheprovider
```

Resultado observado: **21 passed in 0.03s**, código 0. Cubre también relaciones de categoría, asignación y comentarios, junto con registro/actualización de usuario, correo y rol inválidos, creación de ticket y solicitante ausente, estado inicial, filtros, cambio de estado/prioridad y asignación a técnico ausente o de otro rol. La misma suite se ejecutó tras `uv sync --locked` en una copia limpia del commit e5d8c02, con 21 pruebas aprobadas y código 0.

En la versión integrada, `PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 uv run python scripts/verificar_semana7.py` y `PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 uv run python scripts/verificar_semanas8_9.py` terminaron con código 0. Invocaron controles Tk con cinco usuarios y diez tickets ficticios, asignación, comentarios, filtros y errores. Los diálogos se interceptaron; no se inspeccionó visualmente la ventana ni se generaron capturas. La aplicación se arrancó también con `uv run python main.py` y se cerró tras la prueba.

Las soluciones de cuadernillos revisadas se verificaron en carpetas aisladas: 6 pruebas agrupadas para II y 11 pruebas para III. Las pruebas no garantizan calificación académica ni equivalen a llenar los PDFs originales. No se ejecutaron las prácticas SQL del aula ni se configuró un servidor PostgreSQL para el alcance de esta fase.
