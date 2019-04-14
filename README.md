# symptomsurvey_backend ![travisci badge](https://travis-ci.org/CodeForPortland/symptomsurvey_backend.svg?branch=master)

This repository is the API for a website for use by Clackamas County.  These are developer notes.

## setting up your development environment

### Installing Docker

Download Docker for your system at <https://www.docker.com/> and install.

If your OS does not support native docker, you can install docker-toolbox at <https://docs.docker.com/toolbox/toolbox_install_windows/.> In this case, all commands will be run from the docker-toolbox command line, access to the site is done through `192.168.99.100` instead of `localhost`.

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

### Environment Variables

There are two environment variables that are required for access to Twitter. TWITTER_API_KEY and TWITTER_API_ACCESS_KEY are defined in the docker-compose.yml file. An easy platform-agnostic way to ensure the variables are set appropriately is to add a .env file at the project root with the variables defined on separate lines like so: TWITTER_API_ACCESS_KEY=value. The actual values can be provided by David H.

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

If you want to add a Create, Read, Update, or Delete (CRUD) endp())`).

#### Adding new tests

New pytest tests should be added to the WEB/tests/ directory using file names that look like "test_" followed by the topic of the test (eg "test_login.py"). This naming convention will keep our code organized and will allow pytest to discover our test files.

You should start all test files with

```python
from test_app import client
```

which will provide a version of the app with all database calls and rsa keys mocked.
