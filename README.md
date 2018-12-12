# symptomsurvey_backend

This repository is the API for a website for use by Clackamas County.  These are developer notes.
Be aware that these notes assume the reader is using a Mac OSX or Linux command line.

## setting up your development environment

### Installing node

This app uses migrate-mongo for database migrations so you will need NodeJS (verson 7.10.1) installed on your computer to complete setup. You can install the node version manager (nvm) with the following command.

```bash
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash
```

The program `nvm` will be available from your command line once you source the project from your shell. To source your profile from your shell run `. ~/.bash_profile` or open a new terminal window.

Now that `nvm` is installed you can install node and set a default node version:

```bash
nvm install 7.10.1 && nvm alias default 7.10.1
```

You will see that you have a successful install of node if you check the versions of `node` & `npm` and see

```bash
$ node -v
v7.10.1
$ npm -v
4.2.0
```

### Installing mongo

You can use Homebrew to install mongodb and run it from your computer.  If you don't yet have Homebrew installed, you can follow [these notes](https://brew.sh/).

Once Homebrew is installed on your computer, you should be able to run `brew install mongodb`. If mongo was installed successfully, you should be able to ask for the brew info on mongodb and see something similar to the following.

```
$ brew info mongodb
...
To have launchd start mongodb now and restart at login:
  brew services start mongodb
...
```

Whatever command you see along the lines of `brew services start mongodb` in this info is what you should run. This will start a mongo database on the default port when your computer starts. Once it is running you should be able to run `mongo` from the command line and see a mongo shell open.

```
$ mongo
MongoDB shell version v3.6.2
connecting to: mongodb://127.0.0.1:27017
MongoDB server version: 3.6.2
...
```

If the value that you see for "connecting to:..." matches what's present here, then you're ready to set up your app.

## Cloning the repository

Navigate to a repository where you would like to store the source code.  Then run

```bash
git clone https://github.com/codeforportland/symptomsurvey_backend.git
cd symptomsurvey_backend
```

## Running the site locally

You will first need to set up the basic data that the app needs to run in the database.  This is done via that node commands within the project.  First install the node dependencies with `npm install` and then run the available migrations using the command `npm run up`.

To start the application just run `flask run` from the command line.  The site should start and connect to your local mongo database.

## Adding migrations

Migrations may be added with the `npm run create <migration name>` script. This command will add a file to the "migrations" directory with all of the boilerplate for `migrate-mongo` in place. You just need to add any relevant mongo database operations to the `up` method within `module.exports`. Be sure that you add appropriate database operations to the `down` method that undo whatever your `up` operations do.
