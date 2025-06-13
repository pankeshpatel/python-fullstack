








#### Project structure

Root-dir
|- `requirements.txt` (file)
|- `README.md` (file)
|-  `main.py` (file, entry point)
|-  `database` (dir)
      |- `local.db` (local testing)
      |- `.py`  (database connection file)
      |- `prod.db`(`prod testing`)
|- `models` (dir)
|-  `test`  (dir)
|- `routers` (dir)
     |_ `*.py` (all endpoints)
|- `static` (Frontend dir)
      - `css` (dir)
      - `js`   (dir)
          |_ `*.js` ()
|-  `templates` (frontend dir)
      |_ `*.html` 
|-  `alembic` (for data migration)
|-  `.venv` (python virtual environment)
|-   `.gitignore`
