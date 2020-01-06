
## Install

Before running shell commands, set the `CONDUIT_SECRET`, `FLASK_APP` and `FLASK_DEBUG` environment variables :
```bash
export CONDUIT_SECRET='something-really-secret'
export FLASK_APP=/path/to/autoapp.py
export FLASK_DEBUG=1
```

- be sure to have python 3+
- have postgresql installed on your machine
- `pip install -r requirements/dev.txt --user`


## Applying db schema :
```bash
flask db init
flask db migrate
flask db upgrade
```


Whenever a database migration needs to be made. Run the following commands

`flask db migrate`

This will generate a new migration script. Then run `flask db` upgrade

To apply the migration.

For a full migration command reference, run `flask db --help`.

## Running tests with docker : 

```bash
docker container run --name flask_db_test -e POSTGRES_PASSWORD=somePwd -e POSTGRES_USER=myUsr -p 5432:5432 -d postgres
sleep 1
export DATABASE_URL=postgresql://myUsr:somePwd@localhost:5432/myUsr
flask db upgrade
flask test
docker container stop flask_db_test
docker container rm flask_db_test
unset DATABASE_URL
```

## Usage in prod :

```
gunicorn autoapp:app -b 0.0.0.0:$PORT -w 3
```

## Shell

To open the interactive shell, run `flask shell`.

By default, you will have access to the flask ``app`` and models.

## Dev

In your production environment, make sure the `FLASK_DEBUG` environment
variable is unset or is set to ``0``, so that `ProdConfig` is used, and
set `DATABASE_URL` which is your postgresql URI for example
`postgresql://localhost/example`
