# symptomsurvey_backend

This repository is the API for a website for use by Clackamas County.  These are developer notes.

## setting up your development environment

### Installing Docker

Download Docker for your system at https://www.docker.com/ and install.

### Cloning the repository

Navigate to a repository where you would like to store the source code.  Then run

```bash
git clone https://github.com/codeforportland/symptomsurvey_backend.git
cd symptomsurvey_backend
```

### Private key

The private key is intentionally not checked into version control so that it will remain a secret.

Get the private key for the app from me and create a file to contain it at `keys/token`.

### Building the container

From the cloned repo, run

```bash
docker-compose build
```

This may take a while.

### Running the site locally

From the cloned repo, run

```bash
docker-compose up
```

## Updating the project

### Adding migrations

Currently migrations are not properly supported by the docker setup. In the future, management will be an independently launched service, with tools for cloning its migrations to and from a docker container running node.

### Code Structure

#### Adding Controllers and Routes

If you want to add a Create, Read, Update, or Delete (CRUD) endpoint for a resource, then it should be added to the controllers directory. To add a new resource create a python file with the resource name, expose a method from it called `add_routes`, and call that method in the `add_routes` method in controllers/routes.
