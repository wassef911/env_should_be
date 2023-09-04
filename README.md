# ENV_SHOULD_BE

< THIS READMEME is under construction 🤫🤫🤫 >

```sh
usage: env_should_be [-h] -d DESCRIPTION [DESCRIPTION ...] [-fs FAIL_SILENTLY] [-e ENV_FILE]

How should your environment be?

options:
  -h, --help            show this help message and exit

  -d DESCRIPTION [DESCRIPTION ...], --description DESCRIPTION [DESCRIPTION ...]
                        <Required> either one or multiple paths for description files. (json/yml)

  -fs FAIL_SILENTLY, --fail-silently FAIL_SILENTLY
                        <Optional> will return an exit status of 0 even if the description(s) fail to match the current env (still triggers the fail_callback).

  -e ENV_FILE, --env-file ENV_FILE
                        <Optional> not specifying a path to a specific env file to valid description(s) against, environment variables in the current shell will be loaded instead.
```

# TODOs:

- [x] better exceptions
- [x] support required arg
- [x] support callbacks
- [x] example Dockerfiles for different base images (only flask for now)
- [] a more helpful readme
