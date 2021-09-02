# finance-api
A personal finance REST API. This application is able to manage accounts, categories and transactions to register personal finances.

## Tech Stack Used
* Python 3.8.6
* Django 3.2.5
* Django Rest Framework (DRF) 3.12.4
* Docker
* Poetry 1.1.6
* Pytest
* GitHub Actions


## Initialization

### Using Docker Compose
Create an `.env` file
```
make copy/local/envs
```

In root project, run:
```
docker-compose up --build
```


### Running manually
Create a new Poetry Shell
```
make activate
```

Install all dependencies
```
make install/python
```

Create an `.env` file
```
make copy/local/envs
```

Apply migrations
```
make run/migrate
```

Start the project
```
make run/django
```


## Docs
Check the API documentation in:
- [http://localhost:8000/docs/](http://localhost:8000/docs/)


## Testing
With Poetry environment active, run:
```
make run/tests
```


## Developing and contributing
Before start coding, enable the git hooks:
```
pre-commit install
```
