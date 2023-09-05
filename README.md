![cover](https://raw.githubusercontent.com/wassef911/env_should_be/master/cover.png)

[click to read first article about this package](https://dev.to/wassef911/ship-slightly-better-microservices-4i1m)

[latest version on pypi](https://pypi.org/project/env-should-be/)

a more efficient, automated, and developer-friendly approach, allowing them to define deployment environment requirements using simple JSON or YAML descriptions.

Specify the exact conditions under which a container can run, mitigating compatibility issues and enforcing security standards seamlessly…

This environment description can either be one or multiple files and can also be a combination for each type of environment…

```sh
$ pip install env_should_be

env_should_be -fs --description /path/to/description/db.yml /path/to/description/app.json --env-file /path/to/.env --callback ./notify_admin.bash
```

# examples

a number of examples should be available [under this link](https://github.com/wassef911/env_should_be/tree/master/examples)

Imagine you have a flask microservice that relies on a database and cache, and you want to ensure that certain environment variables meet specific criteria each time before the app starts, Here's an example YAML description:

```yaml
DB_USER:
  length: 8
  regex: "^[a-zA-Z0-9]+$"
DB_PASSWORD:
  length: 12
  regex: "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\\$%\\^&\\*])(?=.{8,})"
DB_HOST:
  option:
    - localhost
    - 127.0.0.1
DB_PORT:
  length: 4
  regex: "^[0-9]+$"
  is_int: True
  is_float: False
CACHE: # sure that it has the same value across whatever env?
  constant: "redis://container_name:6379/1"
APP_ENV:
  option:
    - dev
    - prod
  required: false # only get's validated if it is set (not None)
```

then a compose file:

```yaml
version: '3'
services:
  app:
    build:
      context: .
    expose:
      - 5000
    environment:
    command: >
      sh -c '
        env_should_be -d "/app/descriptions/app.json" && \
        flask run --host=0.0.0.0 --port 5000'
```

env_should_be will check these conditions before allowing the container to run. If any condition is not met, it can either block the container from running or using the **-fs** argument, let it start and log the errors, depending on your preference…

or just do a

```sh

env_should_be --help

env_should_be [-h] -d DESCRIPTION [DESCRIPTION ...] [-fs FAIL_SILENTLY] [-e ENV_FILE] [-cb CALLBACK]

How should your environment be?

options:
  -d DESCRIPTION [DESCRIPTION ...], --description DESCRIPTION [DESCRIPTION ...]
                        <Required> either one or multiple paths for description files. (json/yml)

  -fs FAIL_SILENTLY, --fail-silently FAIL_SILENTLY
                        <Optional> will return an exit status of 0 even if the description(s) fail to match the current env (still triggers the callback).

  -e ENV_FILE, --env-file ENV_FILE
                        <Optional> not specifying a path to a specific env file to validate description(s) against, environment variables in the current shell will be loaded instead.

  -cb CALLBACK, --callback CALLBACK
                        <Optional> a callback script to be executed an environment fails to match the a description. (still triggered on fail-silently)
```

## full list of possible descriptions:

```py
(
  "boolean",
  "length",
  "min_length",
  "max_length",
  "regex",
  "option",
  "constant",
  "is_int",
  "is_str",
  "is_float",
  "is_number",
  "is_greater_than_eq",
  "is_lower_than_eq",
  "is_http",
  "is_https",
  "is_ipv4",
  "is_ipv6",
  "is_email",
  "is_uuid",
)
```

### TODOs:

- [x] better exceptions
- [x] support required arg
- [x] support callbacks
- [x] example Dockerfiles for different base images (only flask for now)
- [x] a more helpful readme
- [ ] collect/open issues
- [x] support older python versions
- [x] support different/more complex descriptions
- [ ] support setting default values
- [ ] ship a single executable ?
