# 1. flujo git/Github que se usara todo el curso
## 1.1 Ramas principales

Rama = main (version estable,, aprobada y demostrable para producción) Quién debe tocar esta rama mediante Pull aprobados.

Rama = developer (Integración de trabajo semanal, antes de pasar a la rama estable), quien lo hace? = Todo el equipo developers.

## Feauture/week
feature/week-07-08-inicio de proyecto.

# 1.2 Por qué no trabajar directo en main
main representa lo que se puede presentar, evaluar o desplegar. Si se trabaja directo ahi, cualquir error queda mezcaldo con la version estable. La rama developer permite integrar avances sin romper la linea estable. Las ramas feature/* permiten revisar cambios peueños y claros.

## 1.3 ciclo semanal recomendado
``bash
git checkout developer
git pull origin developer
git checkout -b feature/week-07-models
``
# trabajar código de la semana
``bash
git status
git add .
git commit -m "feat(models): add initial user and ticket domain"
git push -u origin feature/week-07-models
``
## Luego se crea un PR (Pull Request):
``bash
gh pr create --base developer --head feature/week-07-models --title "feat(models): add initial domain" --body "Adds User and Ticket models for week 7. Includes basic validation evidence."
``

## Después de aprobar y fusionar el PR en GitHub:
``bash
git checkout developer
git pull origin developer
``
## Ese pull es importante: actualiza la rama local con lo que GitHub ya fusionó. Si el estudiante no lo hace, la siguiente semana empieza desde una copia atrasada.

# 2. Etapa 0 - Crear carpeta, inicalizar Git y subir developer
Esta etapa prepara el terrno. Todavia no estamos programando el sistema; estamos creando una base ordenada para que el proyecto pueda crecer sin convertirse en un desorden.
## 2.1 Crear carpeta del proyecto
``bash
mkdir HelpDesk_EDU
cd HelpDesk_EDU
``
Explicación para clase: una carpeta de proyecto no es solo un lugar para guardar archivos. Es el límite del sistema: aquí vivirán el código, pruebas, documentación, configuración y control de versiones.

## 2.2 Inicializar Git con main
``bash
git init -b main
git init
```
convierte la carpeta en un repositorio. La opción -b main crea la rama principal con el nombre moderno usado por Github.

##