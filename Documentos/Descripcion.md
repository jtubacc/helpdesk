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
``
convierte la carpeta en un repositorio. La opción -b main crea la rama principal con el nombre moderno usado por Github.

## 2.3 crear archivos base
``bash
touch README.md .gitignore pyproject.toml 
mkdir -p app/models app/services app/repositories app/schemas app/core tsts Documentos
``

### 2.3.1 Estructura del proyecto
helpldesk
/--app/
  /
  /--core/
  /--models/
  /-- repositories/
  /--shcemas/
  /--services/
/--Documentacion/
/--test/
/-- .gitignore
/-- pyproject.toml
/-- README.md

## 2.4 .gitignore
Este archivo oculto de git, ignora archivos que no son necesarios en el repositorio remoto.

.venv/
__pycache__
*.pyc
.env
*.db
.pytest_cache/
.coverage
.DS_Store

** Por qué: Git debe guardar código fuente y documentos importantes, no entonrnos virtuales, bases locales, cachés ni secretos.**

## 2.5 pyproject.toml inicial
[project]
name = "helpdesk-edu"
version = 0.1.0"
descripcion = "A HelpDesk EDU application"
requires-python = "≥3.11"
dependencies =[]

[dependencies-groups]
dev = ["pytest≥8.3"]

[tool.pytest.ini_options]
testpath = ["tests"]
pythonpath = ["."]

## 2.6 Primer commit
git status
git add.
git commit -m "chore: inicializando estructura de proyecto"

explicación: este commit no agrega funcionalidad. Por  eso usa chore:. Guarda la estructura inicial del proyecto.

## 2.7 Crear repositorio remoto y subir main
Si se usara GitHub CLI:
``bash
gh repo creat TU_USUARIO/HelpDesk_EDU --public --source=. --remote=origin --push
Si el repositorio ya fue creado en GitHub:
``bash
git remote add origin https://github.com/TU_USURAIO/HellpDesk_EDU.gitgit 
git push -u origin main

## 2.8 Crear y subir developer
``bash
git checkout -b developer
git push -u origin developer

por qué. developer será la rama de integración del curso. Cada avance semanal entra primero alli. Solo cuando una etapa esté validada se prepera un PR hacia main.

## 2.9 Valicación de la etapa 0
``bash
git branch
git remote -v
git status
``
Debe observarse:
 -- Rama local main creada.
 -- Rama local developer creada.
 -- Remoto origin configurado.
 -- Árbol limpio: workin tree clean.

## 2.10 Commit/PR de etapa 0
Normalmente el primer push de main no requiere PR si el repo estaba vacio. A partir de aqui, si trabajaremos con PRs.

## 3. Desarrollo semana por semana
-- Semana 7 - Encapsulamiento, listas y primer dominio
-- Version objetivo: v.0.1
-- Incremento: Crear las primeras clases del dominio y trabajar en moemoria.

Resultado esperado
Al finalizar, el proyecto tendrá modelos base User y Ticket, servicio en memoria, prueba minima y primer PR funcional hacia developer.

## Flujo Git de la semana
``bash
git checkout developer
git pull origin developer
git checkout -b feature/week-7-encapsulamiento-listas-y-primer-dominio
``

Desarrollo paso a paso
1.
Crear vocabulario del dominio: roles, estados, categorias y prioridades.
2.
Crear entidades simples User y Ticket.
3.
Crear un servicio en memoria para registrar tickets.
4.
Escribir una prueba minima.
5.
Confirmar que la prueba pasa.

