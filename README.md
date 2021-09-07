# tweetspect

This app serves as a proxy to fetch Twitter posts & user feed.

## Stack

- Python 3.8+
- aiohttp
- gunicorn
- pydantic

## Dev dependencies

- aioresponses
- pip-licenses
- pylint
- pytest
- pytest-aiohttp
- pytest-asyncio
- pytest-cov
- radon

## Requirements

- Docker & docker-compose - for building & running the application
- Python 3.8+ - for testing & code style validation

## Prerequisites

Create `.env` file with the following content:

```sh
export TWITTER_API_KEY=YOUR_TWITTER_API_KEY
export TWITTER_API_SECRET_KEY=YOUR_TWITTER_API_SECRET_KEY
```

## Running

```sh
# This step requires Docker & docker-compose.

make run
# ...
curl 127.0.0.1:8000/hashtags/python
curl 127.0.0.1:8000/users/andunai?limit=10
```

## Testing

```sh
# These steps require dev dependencies.

# Initialize virtualenv & install dependencies
make init

# Run all checks
make check

# Test coverage information is written to ./htmlcov/index.html

# Alternatively:
# Check code style
make lint
# Check cyclomatic complexity & code maintability
make metrics
# Run unit tests
make test
```

## License

This application is licensed under GNU GPLv3.
