# Proyecto Data Engineering: Pipeline ETL de ventas

Proyecto de nivel intermedio para practicar Python, Pandas, SQL, pruebas, VS Code, Git Bash y GitHub.

## Qué hace
1. Lee `data/raw/ventas.csv`.
2. Valida y limpia los datos.
3. Calcula `importe_total = cantidad * precio_unitario`.
4. Guarda los datos transformados en `data/processed/ventas_limpias.csv`.
5. Carga los resultados en una base SQLite (`data/warehouse/ventas.db`).
6. Genera logs y ejecuta pruebas automáticas.

## Requisitos
- Python 3.10 o superior
- VS Code
- Git para Windows (incluye Git Bash)

## 1. Abrir el proyecto
Descomprime la carpeta y ábrela en VS Code: **File > Open Folder**.

En VS Code abre un terminal y selecciona **Git Bash**.

## 2. Crear entorno virtual (Git Bash)
```bash
python -m venv .venv
source .venv/Scripts/activate
```
Si `python` no funciona en Windows, prueba `py -m venv .venv` y luego activa el entorno con `source .venv/Scripts/activate`.

## 3. Instalar dependencias
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Ejecutar el pipeline
Desde la carpeta raíz del proyecto:
```bash
python -m src.pipeline
```

Al terminar se crearán:
- `data/processed/ventas_limpias.csv`
- `data/warehouse/ventas.db`
- `logs/pipeline.log`

Consulta la tabla cargada:
```bash
python -c "import sqlite3; c=sqlite3.connect('data/warehouse/ventas.db'); print(c.execute('SELECT * FROM ventas LIMIT 10').fetchall()); c.close()"
```

## 5. Ejecutar las pruebas
```bash
python -m unittest discover -s tests -v
```

## 6. Subirlo a GitHub con Git Bash
Crea primero un repositorio vacío en GitHub, por ejemplo `proyecto-data-engineer-etl`. No añadas README ni `.gitignore` desde GitHub porque ya existen localmente.

Desde la raíz del proyecto:
```bash
git init
git add .
git commit -m "Initial commit: ETL sales pipeline"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/proyecto-data-engineer-etl.git
git push -u origin main
```
Sustituye `TU-USUARIO` por tu usuario de GitHub. GitHub puede pedir autenticación en el navegador. No guardes tokens ni contraseñas dentro del código.

## Estructura
```text
proyecto_data_engineer_etl/
├── .vscode/
│   └── settings.json
├── data/
│   ├── raw/ventas.csv
│   ├── processed/.gitkeep
│   └── warehouse/.gitkeep
├── logs/.gitkeep
├── src/
│   ├── __init__.py
│   └── pipeline.py
├── tests/
│   └── test_pipeline.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Decisiones del ejercicio
- Se descartan filas con campos obligatorios vacíos, cantidades no positivas o precios negativos.
- Se eliminan duplicados exactos.
- SQLite hace de pequeño data warehouse local.
- En un proyecto real se añadirían configuración por entorno, control de calidad más completo, orquestación (Airflow/Control-M) y almacenamiento cloud.
