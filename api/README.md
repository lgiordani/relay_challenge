## Development

Create a virtual environment and install the requirements

```
pip install -r requirements/development.txt
```

If you want to run the application locally use

```
./manage.py compose up -d
```

The development application mounts the application code inside the container, so it can be developed live.

## Test

To test the application run

```
./manage.py test
```

This runs unit tests locally to speed up the process, so Docker is not involved.

## Linters

To run the linters flake8 and black use

```
./manage.py tidy
```

## End to end tests

To run end to end tests against a development server run

```
./manage.py e2e-test
```

The test suite contains the end-to-end integration tests in `tests/e2e` that simulate the whole workflow.

This suite runs Docker Compose automatically to create a local server and destroys it after the tests.

If you want to run the server manually follow these steps

1. Open a terminal and run `./manage.py compose up`
2. In another terminal run `./manage.py e2e-test-nocompose`
3. Stop Docker Compose.

Since integration tests can taint the database, a failed test might make the rest of the suite unusable. There is no reset function in the current datastore objects, so the only solution at the moment is to turn it off an on again, stopping Docker Compose and running it again. IT Crowd style!

## Structure

The application structure from the filesystem point of view is the following

* `config/` JSON configuration files, used to pass environment variables to the application
* `docker/` Dockerfiles and Docker Compose configurations
* `requirements/` Python requirements files
* `src/` Application source files
* `tests/` Application tests
* `app.py` AWS Lambda entry point
* `manage.py` Management script
* `wsgi.py` WSGI server entry point

During development and testing the main tool you should use is `manage.py`. When you run the application in live this script is not used.

The environment variables begin with `RELAY_API`. One of them is used by `manage.py`, one is used to configure Flask, and the rest is specific to the application

* `RELAY_API_ENVIRONMENT` - Used by `manage.py`, see the section "Application configuration"
* `RELAY_API_CONFIG` - Used by Flask, see the section "Application configuration"

Datastore configuration. The Datastore holds information about users.

* `RELAY_API_DATASTORE_TYPE` - The type of datastore to use. Can be either `MEMORY` or `DYNAMODB`. `MEMORY` creates a database in memory that is deleted when the application stops, while `DYNAMODB` tries to connect to DynamoDB using Boto3 (see https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#using-environment-variables). If you set this to `DYNAMODB` you have to set also `RELAY_API_DATASTORE_TABLE`.
* `RELAY_API_DATASTORE_TABLE` - The name of the DynamoDB table that the application should connect to. There is no default.

Vault configuration. The Vault contains the API keys.

* `RELAY_API_KEYS_VAULT_TYPE` - The type of vault to use for the API key. Can be either `MEMORY` or `SECRETSMANAGER`. `MEMORY` creates a vault in memory that contains only the key specified through `RELAY_API_KEY`, while `SECRETSMANAGER` tries to connect to the AWS Secrets Manager using Boto3 (see https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#using-environment-variables). If you set this to `SECRETSMANAGER` you have to set also `RELAY_API_KEYS_VAULT_NAME`.
* `RELAY_API_KEYS_VAULT_NAME` - The name of the AWS Secrets Manager secret the application should connect to. There is no default.
* `RELAY_API_KEY` - The development API key that you want to set if you use the `MEMORY` vault. Defaults to `development-key`.

## Application configuration

There are three separate Flask configurations in `src/application/config.py`, namely `LiveConfig`, `DevelopmentConfig`, and `TestingConfig`. They correspond to the values `live`, `development`, and `testing` of the environment variable `RELAY_API_CONFIG`.

The variable is read from the environment by `wsgi.py` and converted into an object name by the function `src/application/app.py::create_app`. This is the only mandatory environment variable you have to set.

When you are developing or testing, you should use the management script `manage.py`. This script uses the environment variable `RELAY_API_ENVIRONMENT` to read default values for all other environment variables like `RELAY_API_CONFIG`, `RELAY_API_DEVELOPMENT_KEY`, `RELAY_API_DATASTORE_TYPE`, and `RELAY_API_VAULT_TYPE`.

The default `RELAY_API_ENVIRONMENT` value is `development`, but this can be changed specifying the value on the command line.

The JSON configuration files can host environments variables intended for the application or for Flask. There are many variables that can be set for Flask, see https://flask.palletsprojects.com/en/2.2.x/config/.

The reason behind this is to provide defaults allowing the developer to use different values from the command line.

### Use cases

If you want to understand better how the configuration works, have a look at the following use cases.

* **Run tests**: the command `./manage.py test` configures the environment variables using `config/testing.json`, which in turn makes Flask use the object `TestingConfig` (that sets `TESTING = True`).
* **Run end to end tests**: the command `./manage.py e2e-test` configures the environment variables using `config/development.json`, which in turn makes Flask use the object `DevelopmentConfig`. It runs Docker Compose through the file `docker/development.yml`.
* **Run a Docker container for development**: the command `./manage.py compose ARGS` configures the environment variables using `config/development.json` that sets `FLASK_CONFIG=development`. Then it runs Docker Compose using `ARGS` and the file `docker/development.yml` which runs Flask.
* **Run Flask locally**: the command `./manage.py flask ARGS` configures the environment variables using `config/development.json` that sets `FLASK_CONFIG=development`. Then it runs Flask with the given `ARGS`.

## Live setup

To run a live setup make sure you follow these steps

* build the Docker image using `docker/Dockerfile.live`.
* set the environment variable `FLASK_CONFIG` to `live`.
* set the environment variable `RELAY_API_DATASTORE_TYPE` to `DYNAMODB`.
* set the environment variable `RELAY_API_DATASTORE_TABLE` to the name of the DynamoDB table that you want to use.
* set the environment variable `RELAY_API_KEYS_VAULT_TYPE` to `SECRETSMANAGER`.
* set the environment variable `RELAY_API_KEYS_VAULT_NAME` to the name of the AWS Secret Manager secret that you want to use.
* in the Docker image, run the command `gunicorn -w WORKERS -b 0.0.0.0:PORT wsgi:app`, setting the number of workers (`WORKERS`) and the TCP port (`PORT`). E.g. `gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app`.

An example for Docker Compose can be found in `docker/live.yml`. This can be used only if the current machine can access DynamoDB and AWS Secrets Manager.

## Run in an AWS Lambda

To run the application in an AWS Lambda you need to use a different `Dockerfile` and you don't need to run `gunicorn`

* build the Docker image using `docker/Dockerfile.lambda`.
* set the environment variable `FLASK_CONFIG` to `live`.
* set the environment variable `RELAY_API_DATASTORE_TYPE` to `DYNAMODB`.
* set the environment variable `RELAY_API_DATASTORE_TABLE` to the name of the DynamoDB table that you want to use.
* set the environment variable `RELAY_API_KEYS_VAULT_TYPE` to `SECRETSMANAGER`.
* set the environment variable `RELAY_API_KEYS_VAULT_NAME` to the name of the AWS Secret Manager secret that you want to use.

## Requirements

Requirements are split into files that are linked to each other. The file `requirements/testing.txt` installs also `requirements/live.txt`, and the file `requirements/development.txt` installs also `requirements/testing.txt`. The purpose is to minimise the number of packages installed in a specific environment.

The two files `requirements/gunicorn.txt` and `requirements/lambda.txt` install `live.txt` and add packages specific to the execution environment with the same name.

If you change the requirements run

```
pip install -U -r requirements/development.txt
./manage.py compose build app
```

to update the development image.

