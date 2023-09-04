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

a number of example should be available [under this link](https://github.com/wassef911/env_should_be/tree/master/examples)

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

# TODOs:

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
