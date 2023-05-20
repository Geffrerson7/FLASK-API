# PROJECTS-API

## Description

It is an API for creating personal portfolio projects.

## Local Installation

First clone the repository from Github and switch to the new directory:
```bash
  $ clone git https://github.com/Geffrerson7/PROJECTS-API.git
```

```bash
  $ cd PROJECTS-API
```

Activate the virtualenv for your project.

```sh
$ virtualenv venv
# windows
$ source venv/Scripts/activate
# Linux
$ source venv/bin/activate
```

Install project dependencies:
```sh
(env)$ pip install -r requirements.txt
```

Create the following environment variables in the .env file

`FLASK_APP`

`FLASK_DEBUG`

`FLASK_ENV`

`SECRET_KEY`

`SQLALCHEMY_DATABASE_URI`

Execute the migrations:

```sh
(env)$ flask db init
```

```sh
(env)$ flask db migrate
```

```sh
(env)$ flask db upgrade
```

You can now run the development server:
```sh
(env)$ flask run
```

And navigate to
```sh
http://127.0.0.1:5000/
```

## Technologies and programming languages 

* **Python** (v. 3.11.2) [Source](https://www.python.org/)
* **Flask** (v. 2.3.2)  [Source](https://flask.palletsprojects.com/en/2.2.x/)
* **Flask-SQLAlchemy** (v. 3.0.3) [Source](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/)
* **Flask-Cors** (v. 3.0.10) [Source](https://flask-cors.readthedocs.io/en/latest/)
* **flask-marshmallow** (v. 0.15.0) [Source](https://flask-marshmallow.readthedocs.io/en/latest/)
* **python-dotenv** (v. 1.0.0) [Source](https://pypi.org/project/python-dotenv/)
* **PyJWT** [Source](https://pyjwt.readthedocs.io/en/latest/)
* **flask-smorest** (v. 0.42.0) [Source](https://flask-smorest.readthedocs.io/en/latest/)
* **bcrypt** (v. 4.0.1) [Source](https://pypi.org/project/bcrypt/)

## API documentation

[Postman documentation link](https://documenter.getpostman.com/view/24256278/2s93m1aPui)

## Author

- [Gefferson Max Casasola Huamancusi](https://www.github.com/Geffrerson7)