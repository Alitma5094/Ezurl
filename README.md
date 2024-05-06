# EZUrl

EZUrl is an easy to use url shortener that was built from the ground up to respect the privacy of you and your users.
We are a 10% open source platform for those who want compleat control over what data is (or isn't) collected.

## Features

- 🎭 No user data collected by default
- 🔒 Built-in safety tools
- 🎨 Complete control over how the site looks and behaves when you self-host

## Setting up EZUrl

1. Make sure [Docker](https://docs.docker.com/get-docker/) is installed

2. Clone the repo

```shell
git clone https://github.com/Alitma5094/Ezurl.git
```

3. Replace the default environment variables in `docker-compose.example.yml` with your own
4. Rename `docker-compose.example.yml` to `docker-compose.yml`
5. Start Docker

```shell
docker compose up
```

6. In the Docker container, run the following commands to initialize the django project

```shell
python manage.py migrate
python manage.py createsuperuser
```

## Built With

- [Django](https://www.djangoproject.com/) &mdash; The back end that renders and servers the site
- [PostgreSQL](https://www.postgresql.org/) &mdash; The main data store
- [HTMX](https://htmx.org/) &mdash; Adds some nice front-end reactivity

Plus *lots* of python packages, a complete list of which is in
the [requirements.txt](https://github.com/Alitma5094/Ezurl/blob/main/requirements.txt).

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any
contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also
simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

