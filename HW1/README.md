# Table of Contents

* [Start Development](#start-development)
    * [Start the Database](#start-the-database)
    * [Activate Enviroment](#activate-enviroment)
    * [Start the Server](#start-the-server)
    * [Stop the Database](#stop-the-database-when-you-are-finished)
* [Problems](#problems)


## Start Development

In this section I will explain how you can set up the development environment and run the application.

### Start the Database

Run the following command in the root directory of the project

```
docker compose up -d
```

This will start a postgres db which will listen on port 5432.

### Activate Enviroment

Activate the python virtual enviroment by running the following commands in the root directory of the project

```
virtualenv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

### Start the Server

Run the following command in the root directory of the project

```
flask run
```

### Stop the Database (when you are finished)

Run the following command in the root directory of the project

```
docker compose down
```
