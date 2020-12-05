# dialogs

Clone this repository:

```
git clone git@github.com:san4ezy/dialogs.git
```

Build the containers and run them (please, be sure you have installed docker and docker-compose):

```
docker-compose build && docker-compose up -d
```

or use make commant:

```
make build && make up
```

Previous commands will build the application container and a PostgreSQL container for serving the data.

Migrate database:
```
docker-compose exec app python manage.py migrate
```

or use make command:

```
make migrate
```

Run test with the following command:

```
docker-compose exec app python manage.py test
```

You also can test all endpoints with the prepared request examples from [this file](https://github.com/san4ezy/dialogs/blob/main/http/test.http).
