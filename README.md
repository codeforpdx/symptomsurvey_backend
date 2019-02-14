# symptomsurvey_backend ![travisci badge](https://travis-ci.org/CodeForPortland/symptomsurvey_backend.svg?branch=master)

This repository is the API for a website for use by Clackamas County.  These are developer notes.

## setting up your development environment

### Installing Docker

Download Docker for your system at https://www.docker.com/ and install.

If your OS does not support native docker, you can install docker-toolbox at https://docs.docker.com/toolbox/toolbox_install_windows/. In this case, all commands will be run from the docker-toolbox command line, access to the site is done through `192.168.99.100` instead of `localhost`.

If you are running a version of Windows other than Windows 10 Professional or Enterprise, follow the instructions [here](https://github.com/CodeForPortland/symptomsurvey_backend/wiki/How-to-set-up-docker-on-windows)

### Cloning the repository

Navigate to a repository where you would like to store the source code.  Then run

```bash
git clone https://github.com/codeforportland/symptomsurvey_backend.git
cd symptomsurvey_backend
```

### Private key

The private key is intentionally not checked into version control so that it will remain a secret.

Get the private key for the app from me and create a file to contain it at `WEB/keys/token`.

### Building the container

From the cloned repo directory and with docker running, run

```bash
docker-compose build
```

This may take a while. If it seems to freeze on windows, pressing enter seems to cause the output to update.

### Running / Updating the site locally

From the cloned repo directory and with docker running, run

```bash
docker-compose up -d --build
```

This will build all services on the site, as well as launch them. If the site is already running, it will rebuild any services who's source has changed, as well as relaunch it.

### Stopping the site

From the cloned repo directory and with docker running, run

```bash
docker-compose down
```

## Updating the project

### Adding migrations

While the project is running, you can manage mongodb through the MANAGE service, which runs idle with the appropriate node files. You can access this via
```bash
docker-compose exec manage sh
```
which will open a shell running in the container.

You can then run migrations with either
```bash
npm run up
npm run down
npm run create <migration-name>
```

which will perform migrations as per usual.
The migrations folder is synced between the repo and container, so any new migrations will be duplicated either way. This allows you to create a migration in the container, edit it locally, and sync it to mongo without starting and stopping any containers.

### Code Structure

#### Adding Controllers and Routes

If you want to add a Create, Read, Update, or Delete (CRUD) endpoint for a resource, then it should be added to the controllers directory. To add a new resource create a python file with the resource name, expose a method from it called `add_routes`, and call that method in the `add_routes` method in controllers/routes.

### Testing

#### Running the tests

You will need to have python 3 installed along with all of the project dependencies listed in the Pipfile to run these tests locally.

All tests should be run from the WEB/ directory. They can be run all together with `python -m pytest` or you can run a single test by specifying the file (eg `python -m pytest tests/login_test.py`).

#### Adding new tests

New pytest tests should be added to the WEB/tests/ directory using file names that look like "test_" followed by the topic of the test (eg "test_login.py"). This naming convention will keep our code organized and will allow pytest to discover our test files.

You should start all test files with

```
from test_app import client
```

which will provide a version of the app with all database calls and rsa keys mocked.
