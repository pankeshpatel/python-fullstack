








#### Project structure

```
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

```

### Endpoints FrontEnd and Backend

```
admin.py
(BE) GET         /admin/user              -  Read all Users
(BE) DELETE      /admin/{username}        - delete a user by username
(BE) GET         /admin/todo              - delete all todo

auth.py
(BE) GET        /login                   - Get a token of an existing user

todos.py
(BE) GET /todos/                         - Read all Todos of a user
(BE) GET /todos/{todo_id}                - Read Todo by ID of a user
(BE) POST /todos/todos                   - Create a new todos of a user
(BE) PUT  /todos/todo/{todo_id}          - Update an existing todo of a user
(BE) DELETE /todos/todo/{todo_id}        - Delete an existing todo of a user

users.py
(BE) GET   /user/                         -  get user
(BE) POST /user/register                  - register a user
(BE) PUT /user/password                   - change password
(BE) PUT /user/phonenumber/{phone_number} - change phone number

health.py
(BE) GET         /health                  - check system status
```